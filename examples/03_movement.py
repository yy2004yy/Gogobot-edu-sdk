"""Example 03 — Movement (directional gait).

Drives each direction in turn with settle pauses, then stops and resets the robot.

Run: python examples/03_movement.py
"""

import time

from aidog_sdk import AiDog, Movement

with AiDog() as dog:
    # choice 1: scan and connect
    dog.connect("Changba-Ai-Dog")
    # choice 2: connect with address
    # dog.connect(address="xx:xx:xx:xx:xx:xx")  # replace with your device address, eg: "87:34:63:B0:1C:D0"

    # Stop and stabilize for 1 second before each next movement.
    def stabilize_1s():
        dog.stop_movement()
        time.sleep(1.0)

    print("FORWARD 5.0s")
    # choice 1: with duration_s
    dog.send_movement(Movement.FORWARD, duration_s=5.0)
    # choice 2: without duration_s
    # dog.send_movement(Movement.FORWARD)
    # time.sleep(5.0)
    stabilize_1s()

    print("RIGHT 5.0s")
    dog.send_movement(Movement.RIGHT, duration_s=5.0)
    stabilize_1s()

    print("BACK 5.0s")
    dog.send_movement(Movement.BACK, duration_s=5.0)
    stabilize_1s()

    print("LEFT 5.0s")
    dog.send_movement(Movement.LEFT, duration_s=5.0)
    stabilize_1s()

    print("STEP 5.0s")
    dog.send_movement(Movement.STEP, duration_s=5.0)
    stabilize_1s()

    print("STOP")
    dog.stop_movement()
    time.sleep(2.0)

    dog.reset()
