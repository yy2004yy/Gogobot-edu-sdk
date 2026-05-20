"""
Foot-end control example that reproduces the firmware sniff motion
using MODE_ROBOT_ADJUST.
Flow: shift weight backward -> lift front legs with X fine-tuning
-> hold -> reverse to recover.
"""

from __future__ import annotations

import time

from aidog_sdk import AiDog, ExpressionAction, Movement, Tone


def run_sniff_motion(dog: AiDog) -> None:
    # Start from BASIC_MODE for a consistent initial posture.
    dog.request_basic_mode()
    time.sleep(0.4)

    dog.default_pose_output(0.0, 0.0, 5.0, 110.0)
    time.sleep(0.4)

    # 1) Shift weight backward with all four feet (same X direction).
    dog.syn_foot_adjust(
        [
            ("foot_0_x", 35.0),  # right front
            ("foot_2_x", 35.0),  # left front
            ("foot_1_x", 35.0),  # right rear
            ("foot_3_x", 35.0),  # left rear
        ],
        duration_ms=600,
    )
    time.sleep(0.8)


    # 2) Lift front legs and apply X-direction fine-tuning.
    dog.syn_foot_adjust(
        [
            ("foot_0_z", 60.0),   # lift right front
            ("foot_2_z", 60.0),   # lift left front
            ("foot_0_x", -30.0),  # pull right front back
            ("foot_2_x", -30.0),  # pull left front back
        ],
        duration_ms=600,
    )
    time.sleep(0.7)


    # 3) Hold expression + voice effect.
    dog.send_expression(ExpressionAction.EAT_SNACK)
    dog.send_audio(Tone.EATING)
    time.sleep(8.0)
    dog.send_audio(Tone.STOP)


    # 4) Revert front-leg lift and X fine-tuning.
    dog.syn_foot_adjust(
        [
            ("foot_0_z", -60.0),
            ("foot_2_z", -60.0),
            ("foot_0_x", 30.0),
            ("foot_2_x", 30.0),
        ],
        duration_ms=600,
    )
    time.sleep(0.8)


    # 5) Revert backward weight shift.
    dog.syn_foot_adjust(
        [
            ("foot_0_x", -35.0),
            ("foot_2_x", -35.0),
            ("foot_1_x", -35.0),
            ("foot_3_x", -35.0),
        ],
        duration_ms=600,
    )
    time.sleep(0.8)

    dog.request_basic_mode()
    time.sleep(0.2)


def main() -> None:
    with AiDog() as dog:
        # choice 1: scan and connect
        dog.connect("Changba-Ai-Dog")
        # choice 2: connect with address
        # dog.connect(address="xx:xx:xx:xx:xx:xx")  # replace with your device address, eg: "28:3B:8A:6B:A5:42"

        # Move forward first, then perform sniff motion.
        dog.send_movement(Movement.FORWARD, duration_s=2.0)
        time.sleep(0.3)
        dog.stop_movement()
        time.sleep(0.3)

        # Disable special detection during syn_* adjustments to avoid interruptions.
        dog.disable_special_detection()

        run_sniff_motion(dog)

        dog.enable_special_detection()
        dog.reset()
        print("sniff motion completed")


if __name__ == "__main__":
    main()
