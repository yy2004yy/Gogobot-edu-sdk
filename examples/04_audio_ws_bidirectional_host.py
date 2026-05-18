"""Example 04 — Bidirectional PCM WebSocket host (PC server, robot as client).

Relays live voice both ways between your PC and the dog over Wi‑Fi (16 kHz mono PCM; see script for deps and firmware settings).

Uses :class:`aidog_sdk.DevPcWebSocketHost` with ``connection_handler=...`` (same stack as ``dev_pc_ws.run_dev_pc_websocket_server``).

Run from the ``aidog_sdk/`` repo root::

    python examples/04_audio_ws_bidirectional_host.py --bind 0.0.0.0 --port 8765

The block below prepends this repository root to ``sys.path`` so ``import aidog_sdk`` uses this checkout instead of an older global ``pip install``.
"""

from __future__ import annotations

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
_inner = _repo_root / "aidog_sdk"
if _inner.is_dir() and (_inner / "__init__.py").is_file():
    rs = str(_repo_root)
    while rs in sys.path:
        sys.path.remove(rs)
    sys.path.insert(0, rs)

import argparse
import asyncio
import time

from aidog_sdk import DevPcWebSocketHost

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 320  # 20 ms @ 16 kHz; mono int16: 320 samples × 2 bytes = 640 bytes per chunk

try:
    import numpy as np
    import sounddevice as sd
except ImportError:
    sd = None
    np = None


def _resample_mono_int16(x: "np.ndarray", src_sr: int, dst_sr: int) -> "np.ndarray":
    """
    Linear resample: mono int16 -> mono int16.
    ``x``: shape (n,).
    """
    if src_sr == dst_sr or x.size == 0:
        return x
    # Common 48k -> 16k: integer ratio, decimate
    if src_sr % dst_sr == 0:
        step = src_sr // dst_sr
        return x[::step]

    # Generic linear interpolation (fine for dev/debug)
    x_f = x.astype(np.float32)
    n_src = x_f.shape[0]
    n_dst = int(round(n_src * (dst_sr / float(src_sr))))
    if n_dst <= 0:
        return x[:0]
    t_src = np.linspace(0.0, 1.0, num=n_src, endpoint=False, dtype=np.float32)
    t_dst = np.linspace(0.0, 1.0, num=n_dst, endpoint=False, dtype=np.float32)
    y = np.interp(t_dst, t_src, x_f).astype(np.int16)
    return y


async def _handle_client(
    ws,
    no_audio: bool,
    input_device: int | None,
    output_device: int | None,
) -> None:
    peer = getattr(ws, "remote_address", None)
    print(f"[host] connected: {peer}")

    stop = asyncio.Event()
    play_q: asyncio.Queue[bytes] = asyncio.Queue(maxsize=100)

    async def from_dog() -> None:
        try:
            async for msg in ws:
                if isinstance(msg, str):
                    continue
                if isinstance(msg, (bytes, bytearray)):
                    b = bytes(msg)
                    if no_audio:
                        print(f"[uplink] bytes={len(b)}")
                    else:
                        await play_q.put(b)
        except Exception as e:
            print(f"[host] receive ended: {e}")
        finally:
            stop.set()

    async def to_dog() -> None:
        if no_audio or sd is None or np is None:
            await stop.wait()
            return
        loop = asyncio.get_event_loop()
        try:
            # Some devices report more than 1 input channel (e.g. stereo mic).
            # Open with max_input_channels and downmix to mono for uplink.
            mic_channels = CHANNELS
            mic_sr = SAMPLE_RATE
            if input_device is not None:
                dev = sd.query_devices(input_device)
                mic_channels = int(dev.get("max_input_channels", CHANNELS)) or CHANNELS
                # Prefer device default sample rate for compatibility
                try:
                    mic_sr = int(float(dev.get("default_samplerate", SAMPLE_RATE)))
                except Exception:
                    mic_sr = SAMPLE_RATE

            kwargs = dict(
                samplerate=mic_sr,
                channels=mic_channels,
                dtype="int16",
                blocksize=max(1, int(round(mic_sr * 0.02))),  # ~20 ms blocks
            )
            if input_device is not None:
                kwargs["device"] = input_device

            print(f"[host] input device channels={mic_channels}, sr={mic_sr} (downmix+resample -> 16k mono)")

            # Some WDM-KS drivers lack blocking read; use callback capture instead of stream.read.
            # Callback thread batches mono int16 into CHUNK frames and sends via ws.send.
            bytes_per_chunk = CHUNK * 2  # 16k mono int16: 2 bytes per sample
            mono_buf = bytearray()
            mic_send_q: asyncio.Queue[bytes] = asyncio.Queue(maxsize=200)

            def _cb(indata, frames, time_info, status) -> None:
                nonlocal mono_buf
                if status:
                    pass  # avoid spamming logs
                try:
                    # indata: (frames, mic_channels) int16
                    mono_in = indata[:, 0]  # first channel
                    # Resample to 16 kHz
                    mono_16k = _resample_mono_int16(mono_in, mic_sr, SAMPLE_RATE)
                    mono_buf.extend(mono_16k.tobytes())
                    while len(mono_buf) >= bytes_per_chunk:
                        chunk = bytes(mono_buf[:bytes_per_chunk])
                        del mono_buf[:bytes_per_chunk]
                        loop.call_soon_threadsafe(mic_send_q.put_nowait, chunk)
                except Exception:
                    # Do not raise from audio callback
                    return

            kwargs_cb = dict(kwargs)
            kwargs_cb["callback"] = _cb

            with sd.InputStream(**kwargs_cb):
                while not stop.is_set():
                    chunk = await mic_send_q.get()
                    try:
                        await ws.send(chunk)
                    except Exception:
                        break
        except Exception as e:
            print(f"[host] microphone capture failed: {e}")

    async def play_from_queue() -> None:
        if no_audio or sd is None or np is None:
            await stop.wait()
            return
        loop = asyncio.get_event_loop()
        try:
            kwargs = dict(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype="int16",
                blocksize=CHUNK,
            )
            if output_device is not None:
                kwargs["device"] = output_device
            with sd.OutputStream(**kwargs) as stream:
                while not stop.is_set():
                    try:
                        chunk = await asyncio.wait_for(play_q.get(), timeout=0.15)
                    except asyncio.TimeoutError:
                        continue
                    if len(chunk) < 2:
                        continue
                    if len(chunk) % 2:
                        chunk = chunk[:-1]
                    arr = np.frombuffer(chunk, dtype=np.int16).reshape(-1, CHANNELS)
                    await loop.run_in_executor(None, stream.write, arr)
        except Exception as e:
            print(f"[host] playback failed: {e}")

    t1 = asyncio.create_task(from_dog())
    t2 = asyncio.create_task(to_dog())
    t3 = asyncio.create_task(play_from_queue())
    await stop.wait()
    for t in (t1, t2, t3):
        t.cancel()
    print("[host] connection closed")


def main() -> None:
    p = argparse.ArgumentParser(description="AiDog bidirectional PCM WebSocket host")
    p.add_argument("--bind", default="0.0.0.0", help="bind address (default 0.0.0.0)")
    p.add_argument("--port", type=int, default=8765, help="port (default 8765)")
    p.add_argument(
        "--no-audio",
        action="store_true",
        help="no play/capture; print uplink byte counts only (useful without sounddevice)",
    )
    p.add_argument(
        "--input-device",
        type=int,
        default=None,
        help="sounddevice input device index if default mic fails (e.g. 1)",
    )
    p.add_argument(
        "--output-device",
        type=int,
        default=None,
        help="sounddevice output device index if default speaker fails",
    )
    args = p.parse_args()

    no_audio = args.no_audio or sd is None or np is None
    if sd is None or np is None:
        print("[host] sounddevice/numpy missing; using --no-audio (debug only)", file=sys.stderr)

    async def connection_handler(ws) -> None:
        await _handle_client(ws, no_audio, args.input_device, args.output_device)

    host = DevPcWebSocketHost(
        host=args.bind,
        port=args.port,
        connection_handler=connection_handler,
    )
    host.start()
    print(f"[host] WebSocket listening ws://{args.bind}:{args.port}")
    print("[host] waiting for robot (check firmware DEV_PC_AUDIO_WS_URL points here)")

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n[host] exit")
    finally:
        host.stop()


if __name__ == "__main__":
    main()
