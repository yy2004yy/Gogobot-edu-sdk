"""Example 07 — Smooth pose / foot / joint adjust (BLE MODE 0x0A).

Smoothly adjusts body pose, foot positions, and leg joints, then returns to basic mode (requires matching firmware).

Run: python examples/07_Servo_Control.py
"""

from __future__ import annotations

import time

from aidog_sdk import AiDog


def main() -> None:
    dog = AiDog()
    try:
        # choice 1: scan and connect
        dog.connect("Changba-Ai-Dog")
        # choice 2: connect with address
        # dog.connect(address="xx:xx:xx:xx:xx:xx")  # replace with your device address, eg: "87:34:63:B0:1C:D0"

        # Disable special-state auto detection during servo tuning to avoid interference.
        dog.disable_special_detection()

        dog.default_pose_output(0.0, 0.0, 5.0, 110.0)
        time.sleep(0.4)

        # --- Pose: multiple axes allowed; example only adjusts COG height ---
        dog.syn_pose_adjust(
            [{"name": "cog_z", "now": 110.0, "end": 60.0}],
            duration_ms=500,
        )
        time.sleep(1.5)

        dog.syn_pose_adjust(
            [{"name": "cog_z", "now": 60.0, "end": 110.0}],
            duration_ms=500,
        )
        time.sleep(1.5)

        # --- Feet: one call can move several feet together in the same window ---
        dog.syn_foot_adjust(
            [
                ("foot_0_x", 30.0),  # RF foot X
                ("foot_1_x", 30.0),  # RH foot X
                ("foot_2_x", 30.0),  # LF foot X
                ("foot_3_x", 30.0),  # LH foot X
            ],
            duration_ms=500,
        )
        time.sleep(1.5)

        dog.syn_foot_adjust(
            [
                ("foot_0_x", -30.0),
                ("foot_1_x", -30.0),
                ("foot_2_x", -30.0),
                ("foot_3_x", -30.0),
            ],
            duration_ms=500,
        )
        time.sleep(1.5)

        # --- Joints: first argument must be a single list of items (not multiple args) ---
        dog.syn_joint_adjust(
            [
                {"name": "joint_0_1", "delta": -20.0},  # RF thigh
                {"name": "joint_0_2", "delta": 30.0},  # RF shin
                {"name": "joint_1_1", "delta": 30.0},  # RH thigh
                {"name": "joint_1_2", "delta": -30.0},  # RH shin
                {"name": "joint_2_1", "delta": -20.0},  # LF thigh
                {"name": "joint_2_2", "delta": 30.0},  # LF shin
                {"name": "joint_3_1", "delta": 30.0},  # LH thigh
                {"name": "joint_3_2", "delta": -30.0},  # LH shin
            ],
            duration_ms=500,
        )
        time.sleep(1.5)

        dog.syn_joint_adjust(
            [
                {"name": "joint_0_1", "delta": 20.0},
                {"name": "joint_0_2", "delta": -30.0},
                {"name": "joint_1_1", "delta": -30.0},
                {"name": "joint_1_2", "delta": 30.0},
                {"name": "joint_2_1", "delta": 20.0},
                {"name": "joint_2_2", "delta": -30.0},
                {"name": "joint_3_1", "delta": -30.0},
                {"name": "joint_3_2", "delta": 30.0},
            ],
            duration_ms=500,
        )
        time.sleep(1.5)

        # Explicit BASIC_MODE (new firmware may also auto-request after each syn_*)
        dog.request_basic_mode()
        dog.set_special_detection(True)
        time.sleep(0.2)

        print("All commands sent.")
    finally:
        dog.disconnect()
        dog.shutdown()


if __name__ == "__main__":
    main()
