"""Bidirectional PCM WebSocket host.

Purpose:
    Relay live PCM audio between the PC and robot over LAN WebSocket.
Risk level:
    Low. This example does not command robot movement.
Dependencies:
    pip install -e ".[bidir_audio]"
Firmware:
    DEV_PC_AUDIO_WS_ENABLE=1 and DEV_PC_AUDIO_WS_URL points to this PC.
Run:
    python examples/05_audio/bidirectional_pcm_ws_host.py --bind 0.0.0.0 --port 8765
    python examples/05_audio/bidirectional_pcm_ws_host.py --no-audio
Expected result:
    The terminal reports the robot WebSocket connection and audio frame flow.
Exit:
    Press Ctrl+C. The script stops the WebSocket host in cleanup.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from aidog_sdk import DevPcWebSocketHost

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 320

try:
    import numpy as np
    import sounddevice as sd
except ImportError:
    np = None
    sd = None


def resample_mono_int16(x: "np.ndarray", src_sr: int, dst_sr: int) -> "np.ndarray":
    if src_sr == dst_sr or x.size == 0:
        return x
    if src_sr % dst_sr == 0:
        return x[:: src_sr // dst_sr]

    x_f = x.astype(np.float32)
    n_src = x_f.shape[0]
    n_dst = int(round(n_src * (dst_sr / float(src_sr))))
    if n_dst <= 0:
        return x[:0]
    t_src = np.linspace(0.0, 1.0, num=n_src, endpoint=False, dtype=np.float32)
    t_dst = np.linspace(0.0, 1.0, num=n_dst, endpoint=False, dtype=np.float32)
    return np.interp(t_dst, t_src, x_f).astype(np.int16)


async def handle_client(
    ws,
    no_audio: bool,
    input_device: int | None,
    output_device: int | None,
) -> None:
    peer = getattr(ws, "remote_address", None)
    print(f"[host] connected: {peer}")
    stop = asyncio.Event()
    play_q: asyncio.Queue[bytes] = asyncio.Queue(maxsize=100)

    async def from_robot() -> None:
        try:
            async for msg in ws:
                if isinstance(msg, str):
                    continue
                if isinstance(msg, (bytes, bytearray)):
                    data = bytes(msg)
                    if no_audio:
                        print(f"[uplink] bytes={len(data)}")
                    else:
                        await play_q.put(data)
        except Exception as exc:
            print(f"[host] receive ended: {exc}")
        finally:
            stop.set()

    async def to_robot() -> None:
        if no_audio or sd is None or np is None:
            await stop.wait()
            return
        loop = asyncio.get_event_loop()
        try:
            mic_channels = CHANNELS
            mic_sr = SAMPLE_RATE
            if input_device is not None:
                dev = sd.query_devices(input_device)
                mic_channels = int(dev.get("max_input_channels", CHANNELS)) or CHANNELS
                mic_sr = int(float(dev.get("default_samplerate", SAMPLE_RATE)))

            kwargs = {
                "samplerate": mic_sr,
                "channels": mic_channels,
                "dtype": "int16",
                "blocksize": max(1, int(round(mic_sr * 0.02))),
            }
            if input_device is not None:
                kwargs["device"] = input_device

            bytes_per_chunk = CHUNK * 2
            mono_buf = bytearray()
            mic_send_q: asyncio.Queue[bytes] = asyncio.Queue(maxsize=200)

            def callback(indata, frames, time_info, status) -> None:
                _ = frames, time_info, status
                nonlocal mono_buf
                try:
                    mono_16k = resample_mono_int16(indata[:, 0], mic_sr, SAMPLE_RATE)
                    mono_buf.extend(mono_16k.tobytes())
                    while len(mono_buf) >= bytes_per_chunk:
                        chunk = bytes(mono_buf[:bytes_per_chunk])
                        del mono_buf[:bytes_per_chunk]
                        loop.call_soon_threadsafe(mic_send_q.put_nowait, chunk)
                except Exception:
                    return

            kwargs["callback"] = callback
            with sd.InputStream(**kwargs):
                while not stop.is_set():
                    chunk = await mic_send_q.get()
                    await ws.send(chunk)
        except Exception as exc:
            print(f"[host] microphone capture failed: {exc}")

    async def play_from_robot() -> None:
        if no_audio or sd is None or np is None:
            await stop.wait()
            return
        loop = asyncio.get_event_loop()
        try:
            kwargs = {
                "samplerate": SAMPLE_RATE,
                "channels": CHANNELS,
                "dtype": "int16",
                "blocksize": CHUNK,
            }
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
        except Exception as exc:
            print(f"[host] playback failed: {exc}")

    tasks = [
        asyncio.create_task(from_robot()),
        asyncio.create_task(to_robot()),
        asyncio.create_task(play_from_robot()),
    ]
    await stop.wait()
    for task in tasks:
        task.cancel()
    print("[host] connection closed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Gogobot EDU bidirectional PCM WebSocket host")
    parser.add_argument("--bind", default="0.0.0.0", help="bind address")
    parser.add_argument("--port", type=int, default=8765, help="bind port")
    parser.add_argument("--timeout", type=float, default=0.0, help="auto-exit after seconds; 0 runs forever")
    parser.add_argument("--no-audio", action="store_true", help="print uplink byte counts only")
    parser.add_argument("--input-device", type=int, default=None, help="sounddevice input device index")
    parser.add_argument("--output-device", type=int, default=None, help="sounddevice output device index")
    args = parser.parse_args()

    no_audio = args.no_audio or sd is None or np is None
    if sd is None or np is None:
        print("[host] sounddevice/numpy missing; using --no-audio", file=sys.stderr)

    async def connection_handler(ws) -> None:
        await handle_client(ws, no_audio, args.input_device, args.output_device)

    host = DevPcWebSocketHost(host=args.bind, port=args.port, connection_handler=connection_handler)
    try:
        host.start()
        print(f"[host] WebSocket listening ws://{args.bind}:{args.port}")
        print("[host] waiting for robot")

        deadline = time.time() + args.timeout if args.timeout > 0 else None
        while deadline is None or time.time() < deadline:
            time.sleep(1.0)
        return 0
    except KeyboardInterrupt:
        print("\n[host] interrupted")
        return 130
    finally:
        host.stop()


if __name__ == "__main__":
    raise SystemExit(main())
