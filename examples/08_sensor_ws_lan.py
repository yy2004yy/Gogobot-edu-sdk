"""Example 08 — IMU/TOF over LAN via Dev PC WebSocket (text frames).

Requires:
- Firmware with ``DEV_PC_AUDIO_WS_ENABLE`` and ``DEV_PC_AUDIO_WS_URL`` pointing to this PC.
- Robot Wi‑Fi connected; same subnet as this computer.
- Optional BLE: connect first if you need to change IMU/TOF stream rates or disable streams.

Run: pip install websockets
     python examples/08_sensor_ws_lan.py --bind 0.0.0.0 --port 8765
     python examples/08_sensor_ws_lan.py --ble --imu-hz 40 --tof-hz 40
"""

from __future__ import annotations

import argparse
import time

from aidog_sdk import AiDog, DevPcWebSocketHost


def main() -> None:
    p = argparse.ArgumentParser(description="AiDog IMU/TOF via Dev PC WebSocket (LAN)")
    p.add_argument("--bind", default="0.0.0.0", help="listen address (default 0.0.0.0)")
    p.add_argument("--port", type=int, default=8765, help="port (match firmware URL)")
    p.add_argument(
        "--ble",
        action="store_true",
        help="also connect BLE to call request_imu_stream / request_tof_stream",
    )
    p.add_argument("--name-prefix", default="Changba-Ai-Dog", help="BLE scan prefix if --ble")
    p.add_argument(
        "--imu-hz",
        type=int,
        default=50,
        metavar="N",
        help="BLE request_imu_stream hz (1–200, default 50); only used with --ble",
    )
    p.add_argument(
        "--tof-hz",
        type=int,
        default=50,
        metavar="N",
        help="BLE request_tof_stream hz (1–200, default 50); only used with --ble",
    )
    args = p.parse_args()

    dog = AiDog(imu_only_notify=True)

    def on_imu(imu: dict) -> None:
        y, p, r = imu.get("yaw_deg"), imu.get("pitch_deg"), imu.get("roll_deg")
        if all(isinstance(v, (int, float)) for v in (y, p, r)):
            print(f"[LAN IMU] yaw={float(y):8.3f} pitch={float(p):8.3f} roll={float(r):8.3f} deg")
        else:
            print("[LAN IMU]", imu)

    def on_tof(tof: dict) -> None:
        print(f"[LAN TOF] front={tof.get('front_mm')}mm oblique={tof.get('oblique_mm')}mm")

    host = DevPcWebSocketHost(
        host=args.bind,
        port=args.port,
        dog=dog,
        on_imu=on_imu,
        on_tof=on_tof,
    )
    host.start()
    print(f"[host] WebSocket ws://{args.bind}:{args.port} — waiting for robot...")

    if args.ble:
        imu_hz = max(1, min(200, int(args.imu_hz)))
        tof_hz = max(1, min(200, int(args.tof_hz)))
        dog.connect(args.name_prefix)
        dog.request_imu_stream(True, hz=imu_hz)
        dog.request_tof_stream(True, hz=tof_hz)
        print(
            f"[BLE] connected; request_imu_stream hz={imu_hz}, request_tof_stream hz={tof_hz} "
            "(LAN text frames follow firmware timer; see README)"
        )

    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n[host] exit")
    finally:
        host.stop()
        if args.ble:
            dog.disconnect()
        dog.shutdown()


if __name__ == "__main__":
    main()
