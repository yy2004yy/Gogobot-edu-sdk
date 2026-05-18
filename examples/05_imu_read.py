"""Example 05 — IMU stream (ae04 JSON imu field).

Prints live IMU data to the terminal until you stop with Ctrl+C.

Run: python examples/05_imu_read.py
"""

from __future__ import annotations

import time
from typing import Callable, Dict

from aidog_sdk import AiDog


def _build_imu_printer() -> Callable[[Dict[str, object]], None]:
    """Ask user what IMU data to print and return a printer callback."""
    print("Select IMU output type:")
    print("  1) yaw / pitch / roll (angles)")
    print("  2) accel or gyro (raw sensor)")
    mode = input("Enter 1 or 2 (default: 1): ").strip() or "1"

    sensor_choice = "accel"
    if mode == "2":
        print("Select sensor data:")
        print("  a) accel")
        print("  b) gyro")
        print("  c) both")
        sensor_choice = (input("Enter a / b / c (default: a): ").strip().lower() or "a")
        if sensor_choice not in ("a", "b", "c"):
            sensor_choice = "a"

    def _print_imu_pretty(imu: Dict[str, object]) -> None:
        if mode == "2":
            accel = imu.get("accel")
            gyro = imu.get("gyro")
            if sensor_choice == "b":
                print(f"[IMU] gyro={gyro}")
            elif sensor_choice == "c":
                print(f"[IMU] accel={accel} gyro={gyro}")
            else:
                print(f"[IMU] accel={accel}")
            return

        # Default mode 1: print orientation angles
        yaw = imu.get("yaw_deg")
        pitch = imu.get("pitch_deg")
        roll = imu.get("roll_deg")
        if all(isinstance(v, (int, float)) for v in (yaw, pitch, roll)):
            print(
                f"[IMU] yaw={float(yaw):8.3f}deg pitch={float(pitch):8.3f}deg "
                f"roll={float(roll):8.3f}deg"
            )
        else:
            print("[IMU]", imu)

    return _print_imu_pretty


def _print_imu_pretty(imu: dict) -> None:
    """Compatibility placeholder; replaced by selected callback in main()."""
    yaw = imu.get("yaw_deg")
    pitch = imu.get("pitch_deg")
    roll = imu.get("roll_deg")
    if all(isinstance(v, (int, float)) for v in (yaw, pitch, roll)):
        print(
            f"[IMU] yaw={float(yaw):8.3f}deg pitch={float(pitch):8.3f}deg "
            f"roll={float(roll):8.3f}deg"
        )
    else:
        print("[IMU]", imu)


def main() -> None:
    hz = 20
    imu_printer = _build_imu_printer()

    # Print IMU only; angle normalization is done inside SDK (*_deg).
    with AiDog(imu_only_notify=True) as dog:
        # choice 1: scan and connect
        dog.connect("Changba-Ai-Dog")
        # choice 2: connect with address
        # dog.connect(address="xx:xx:xx:xx:xx:xx")  # replace with your device address, eg: "87:34:63:B0:1C:D0"

        dog.add_imu_listener(imu_printer)

        print(f"[IMU] Stream ON: hz={hz} (IMU-only terminal output)")
        if hasattr(dog, "request_imu_stream"):
            dog.request_imu_stream(True, hz=hz)

        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[IMU] Stream OFF")
        finally:
            if hasattr(dog, "request_imu_stream"):
                dog.request_imu_stream(False)


if __name__ == "__main__":
    main()
