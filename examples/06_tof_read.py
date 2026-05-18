"""Example 06 — TOF stream (ae04 JSON tof field; same notify as IMU).

Prints live distance readings to the terminal until you stop with Ctrl+C.

Run: python examples/06_tof_read.py
"""

from __future__ import annotations

import time
from typing import Callable, Dict

from aidog_sdk import AiDog


def _build_tof_printer() -> Callable[[Dict[str, object]], None]:
    """Choose front/oblique/both TOF output at runtime."""
    print("Select TOF output type:")
    print("  1) front TOF")
    print("  2) oblique TOF")
    print("  3) front + oblique")
    mode = input("Enter 1 / 2 / 3 (default: 3): ").strip() or "3"
    if mode not in ("1", "2", "3"):
        mode = "3"

    def _print_tof(tof: Dict[str, object]) -> None:
        front = tof.get("front_mm")
        oblique = tof.get("oblique_mm")

        if mode == "1":
            print(f"[TOF] front={front}mm")
            return
        if mode == "2":
            print(f"[TOF] oblique={oblique}mm")
            return
        print(f"[TOF] front={front}mm oblique={oblique}mm")

    return _print_tof


def main() -> None:
    hz = 20
    tof_printer = _build_tof_printer()
    with AiDog(imu_only_notify=True) as dog:
        # choice 1: scan and connect
        dog.connect("Changba-Ai-Dog")
        # choice 2: connect with address
        # dog.connect(address="xx:xx:xx:xx:xx:xx")  # replace with your device address, eg: "87:34:63:B0:1C:D0"

        dog.add_tof_listener(tof_printer)

        print(f"[TOF] Stream ON: hz={hz}")
        if hasattr(dog, "request_tof_stream"):
            dog.request_tof_stream(True, hz=hz)

        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[TOF] Stream OFF")
        finally:
            if hasattr(dog, "request_tof_stream"):
                dog.request_tof_stream(False)


if __name__ == "__main__":
    main()

