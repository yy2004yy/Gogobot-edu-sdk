"""Example 02 — Actions, ears, expressions, tones.

Runs a short demo of scripted moves, ear poses, expression, tones, and ends with a reset.

Run: python examples/02_actions.py
"""

import time

from aidog_sdk import Action, AiDog, EarAction, ExpressionAction, Tone

with AiDog() as dog:
    # choice 1: scan and connect
    dog.connect("Changba-Ai-Dog")
    # choice 2: connect with address
    # dog.connect(address="xx:xx:xx:xx:xx:xx")  # replace with your device address, eg: "87:34:63:B0:1C:D0"

    print("\n[1] Action: Wag Tail")
    ok = dog.perform_action(Action.DANCE, duration=5)
    print(f"  -> done={ok}")

    print("[2] Action: UP_AND_DOWN")
    ok = dog.perform_action(Action.UP_AND_DOWN, count=2)
    print(f"  -> done={ok}")

    print("[3] Ear: EAR_STAND_LEFT")
    dog.send_ear(EarAction.EAR_STAND_LEFT)
    time.sleep(1.5)

    print("[4] Ear percentage: 80%")
    dog.send_ear_percentage(80)
    time.sleep(1.5)

    print("[5] Toggle special detection")
    dog.toggle_special_detection()
    time.sleep(1.0)

    print("[6] Expression: HAPPY_01")
    dog.send_expression(ExpressionAction.HAPPY_01)
    time.sleep(4.0)

    print("[7] Audio: JEEZ")
    dog.send_audio(Tone.JEEZ)
    time.sleep(2.0)

    print("[8] Audio: STOP")
    dog.send_audio(Tone.STOP)
    time.sleep(0.5)

    print("[9] Reset")
    dog.reset()
    print("Done")
