"""
Performance script: stretch -> wag tail -> forward gait + BEAT1
-> kick ball -> IMU right turn 180 deg -> forward gait + BEAT2
-> slow crouch -> COMFORT -> light tail wag finale.

Flow options in this version: forward movement uses gait mode
(`send_movement + sleep`); wag tail repeats 3 times; crouch uses slow-down;
audio is played after crouching; with optional extra effects
(expression/ears/lights/return beat changes).

Run::
    python examples/demo_1_performance.py
"""

from __future__ import annotations

import sys
import time
from typing import Optional

from aidog_sdk import Action, AiDog, EarAction, ExpressionAction, Movement, Tone


# ---------------------------------------------------------------------------
# Configuration (edit as needed)
# ---------------------------------------------------------------------------
IMU_STREAM_HZ = 20
# If 180 deg right-turn direction is interpreted opposite, set to True
# (target heading uses start + 180 deg).
IMU_TURN_INVERT = False

# Extra effects: expression/ears/lights, return beat, final tail wag
ENABLE_EXTRAS = True


def _heading_distance_deg(a: float, b: float) -> float:
    """Minimum angular distance between two headings in degrees: [0, 180]."""
    d = abs((a - b + 180.0) % 360.0 - 180.0)
    return d


def _read_yaw_deg(dog: AiDog) -> Optional[float]:
    imu = dog.get_latest_imu()
    if imu is None:
        return None
    y = imu.get("yaw_deg")
    if isinstance(y, (int, float)):
        return float(y)
    return None


def _wait_yaw(dog: AiDog, timeout_s: float = 5.0) -> Optional[float]:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        y = _read_yaw_deg(dog)
        if y is not None:
            return y
        time.sleep(0.05)
    return None


def turn_right_180_with_imu(
    dog: AiDog,
    *,
    invert_target: bool = False,
    tol_deg: float = 15.0,
    poll_s: float = 0.05,
    max_turn_s: float = 45.0,
) -> None:
    """
    Turn right in gait mode until IMU yaw is close to 180 deg from start
    heading (geometrically opposite direction).
    If ``invert_target=True``, use ``start + 180`` as target (for opposite
    coordinate conventions).
    """
    start = _wait_yaw(dog, timeout_s=5.0)
    if start is None:
        print("[Show] No IMU yaw; fallback to fixed right turn ~5s (calibrate on device)")
        dog.send_movement(Movement.RIGHT)
        time.sleep(5.0)
        dog.stop_movement()
        return

    target = (start + 180.0) if invert_target else (start - 180.0)

    dog.send_movement(Movement.RIGHT)
    t0 = time.time()
    try:
        while time.time() - t0 < max_turn_s:
            cur = _read_yaw_deg(dog)
            if cur is not None and _heading_distance_deg(cur, target) <= tol_deg:
                break
            time.sleep(poll_s)
    finally:
        dog.stop_movement()
        time.sleep(0.3)


def forward_seconds_beat(
    dog: AiDog,
    seconds: float,
    tone: Tone,
    *,
    stop_tone_after: bool = True,
) -> None:
    """Move forward in gait mode for N seconds with tone playback."""
    dog.send_audio(tone)
    time.sleep(0.05)
    dog.send_movement(Movement.FORWARD)
    try:
        time.sleep(float(seconds))
    finally:
        dog.stop_movement()
        time.sleep(0.2)
        if stop_tone_after:
            dog.send_audio(Tone.STOP)


def main() -> int:
    print("[Show] Connecting to robot...")
    with AiDog() as dog:
        # choice 1: scan and connect
        dog.connect("Changba-Ai-Dog")
        # choice 2: connect with address
        # dog.connect(address="xx:xx:xx:xx:xx:xx")  # replace with your device address, eg: "28:3B:8A:6B:A5:42"

        dog.set_special_detection(False)

        hz = max(1, min(200, int(IMU_STREAM_HZ)))
        dog.request_imu_stream(True, hz=hz)
        _wait_yaw(dog, timeout_s=3.0)

        if ENABLE_EXTRAS:
            print("[Show] Ears up")
            dog.send_ear(EarAction.EAR_STAND)
            time.sleep(0.3)
            dog.send_expression(ExpressionAction.YAWN)
            time.sleep(5)

        print("[Show] Shake hand")
        dog.perform_action(Action.SHAKE_HAND, count=3)

        print("[Show] Nod")
        dog.perform_action(Action.NOD, count=2)

        time.sleep(0.3)

        print("[Show] Forward 2s + BEAT1")
        forward_seconds_beat(dog, 2, Tone.BEAT1)

        print("[Show] Jump")
        dog.perform_action(Action.JUMP)

        if ENABLE_EXTRAS:
            dog.send_interaction(int(Action.LIGHT_OFF))
            time.sleep(0.2)

        time.sleep(0.3)

        print("[Show] IMU right turn 180 deg")
        turn_right_180_with_imu(dog, invert_target=IMU_TURN_INVERT)

        print("[Show] Forward again 2s + BEAT3")
        forward_seconds_beat(dog, 2, Tone.BEAT3)

        print("[Show] Slow crouch")
        slow_down_s = 20.0
        # Send non-blocking interaction so audio can be triggered during crouch.
        dog.send_interaction(int(Action.SLOW_DOWN_FOR_PROGRAM), int(slow_down_s))
        time.sleep(1.0)

        if ENABLE_EXTRAS:
            print("[Show] Sleepy expression")
            dog.send_expression(ExpressionAction.SLEEPY)

        # Wait for remaining crouch time before entering next stage.
        time.sleep(max(0.0, slow_down_s - 1.0))

        print("[Show] Stretch")
        dog.perform_action(Action.STRETCH)

        if ENABLE_EXTRAS:
            print("[Show] Finalize: light tail wag x3")
            dog.perform_action(Action.WAG_TAIL, count=3)

        dog.send_audio(Tone.STOP)
        dog.reset()
        dog.request_imu_stream(False)

        dog.set_special_detection(True)
        time.sleep(0.3)

    print("[Show] Finished.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n[Show] Interrupted.", file=sys.stderr)
        raise SystemExit(130)
