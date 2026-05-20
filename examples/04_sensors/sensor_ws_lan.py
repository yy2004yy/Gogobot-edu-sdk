"""Read IMU/TOF over LAN via Dev PC WebSocket.

Purpose:
    Listen for robot WebSocket text frames containing sensor JSON.
Risk level:
    Low. This example reads sensor data and does not command movement.
Dependencies:
    pip install -e ".[dev_pc_ws]"
Firmware:
    DEV_PC_AUDIO_WS_ENABLE=1 and DEV_PC_AUDIO_WS_URL points to this PC.
Run:
    python examples/04_sensors/sensor_ws_lan.py --bind 0.0.0.0 --port 8765
    python examples/04_sensors/sensor_ws_lan.py --ble --hz 40
Expected result:
    The terminal prints LAN IMU/TOF data when the robot connects.
Exit:
    Press Ctrl+C. The script stops the WebSocket host in cleanup.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from aidog_sdk import AiDog, DevPcWebSocketHost


def main() -> int:
    parser = argparse.ArgumentParser(description="Read IMU/TOF via Dev PC WebSocket")
    parser.add_argument("--bind", default="0.0.0.0", help="listen address")
    parser.add_argument("--port", type=int, default=8765, help="listen port")
    parser.add_argument("--ble", action="store_true", help="also connect BLE to request stream rates")
    parser.add_argument("--name-prefix", default="Changba-Ai-Dog", help="BLE name prefix when --ble")
    parser.add_argument("--address", default=None, help="BLE address or platform UUID when --ble")
    parser.add_argument("--hz", type=int, default=50, help="BLE requested IMU/TOF rate when --ble")
    parser.add_argument("--timeout", type=float, default=0.0, help="auto-exit after seconds; 0 runs forever")
    args = parser.parse_args()

    dog = AiDog(imu_only_notify=True)

    def on_imu(imu: dict) -> None:
        yaw = imu.get("yaw_deg")
        pitch = imu.get("pitch_deg")
        roll = imu.get("roll_deg")
        if all(isinstance(v, (int, float)) for v in (yaw, pitch, roll)):
            print(f"[LAN IMU] yaw={float(yaw):8.3f} pitch={float(pitch):8.3f} roll={float(roll):8.3f} deg")
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

    try:
        host.start()
        print(f"[host] WebSocket listening ws://{args.bind}:{args.port}; waiting for robot")

        if args.ble:
            if args.address:
                dog.connect(address=args.address)
            else:
                dog.connect(args.name_prefix)
            hz = max(1, min(200, args.hz))
            dog.request_imu_stream(True, hz=hz)
            dog.request_tof_stream(True, hz=hz)
            print(f"[BLE] requested IMU/TOF stream hz={hz}")

        deadline = time.time() + args.timeout if args.timeout > 0 else None
        while deadline is None or time.time() < deadline:
            time.sleep(1.0)
        return 0
    except KeyboardInterrupt:
        print("\n[host] interrupted")
        return 130
    finally:
        host.stop()
        if args.ble:
            try:
                dog.request_imu_stream(False)
                dog.request_tof_stream(False)
            except Exception:
                pass
            if dog.is_connected:
                dog.disconnect()
        dog.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
