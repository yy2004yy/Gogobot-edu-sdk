"""
Action definitions for the Changba AI-Dog.

Use :class:`Action` members in application code when possible. String aliases
in ``ACTION_ALIASES`` are accepted by ``resolve_action()`` and
``AiDog.perform_action()`` for examples, scripts, and Chinese/English user
input. ``TIMER_BASED`` actions use a ``duration`` parameter in seconds,
``COUNT_BASED`` actions use a repeat ``count``, and ``ANGLE_BASED`` actions use
an ``angle`` parameter in degrees.

The integer values match the ``QRMotion_TypeDef`` enum in the firmware
(sdk/apps/ai_dog/algorithm/interaction_mode/include/interaction_mode.h).
"""

from __future__ import annotations

from enum import IntEnum
from typing import Dict, List, Set, Tuple


class Action(IntEnum):
    """All robot motions, indexed as in the firmware QRMotion_TypeDef enum."""

    IDLE                             = 0
    SLOW_UP                          = 1   # Slowly stand up on all four legs
    SLOW_DOWN                        = 2   # Slowly crouch down (ears lowered)
    SLOW_DOWN_FOR_CHARGE             = 3   # Slowly crouch down (charging posture)
    SLOW_DOWN_FOR_PROGRAM            = 4   # Timed slow crouch (for programming flow)
    UP_AND_DOWN                      = 5   # Repeated slow up-and-down motion
    EXCITED_UP_AND_DOWN              = 6   # Excited vertical bobbing motion

    SIT_DOWN                         = 7   # Sit down
    SIT_DOWN_FOR_PROGRAM             = 8   # Timed sit-down action (for programming flow)
    STAND_UP                         = 9   # Stand up from sitting posture
    SHAKE_HAND                       = 10  # Shake hand
    SHAKE_HAND_WITH_SIT_DOWN         = 11  # Sit down and shake hand directly
    NOD                              = 12  # Nod
    SHAKE_HEAD                       = 13  # Shake head
    STRETCH                          = 14  # Stretch
    PEE                              = 15  # Simulated urination motion
    TWIST                            = 16  # Twist/sway in place
    PUSH_UP                          = 17  # Push-up
    NEW_YEAR                         = 18  # New Year greeting motion
    WAG_TAIL                         = 19  # Wag tail
    STOMP                            = 20  # Stomp right front paw
    SNIFF                            = 21  # Sniff
    CELEBRATE                        = 22  # Celebrate / cheer motion
    JUMP                             = 23  # Jump
    DANCE                            = 24  # Dance
    KICK_BALL                        = 25  # Kick ball
    TOUCH_GROUND_RIGHT               = 26  # Tap ground with right paw
    TOUCH_GROUND_LEFT                = 27  # Tap ground with left paw
    PLAY_DEAD                        = 28  # Play dead

    # --- timed movement actions (duration in seconds) ---
    STEP_INTERACTION                 = 29  # Step in place (timed)
    FORWARD_INTERACTION              = 30  # Move forward (timed)
    BACK_INTERACTION                 = 31  # Move backward (timed)
    LEFT_INTERACTION                 = 32  # Turn left (timed)
    RIGHT_INTERACTION                = 33  # Turn right (timed)
    LOW_FORWARD_AND_BACKWARD         = 34  # Low posture forward/backward (timed)
    LOW_FORWARD                      = 35  # Low posture forward (timed)
    LOW_BACKWARD                     = 36  # Low posture backward (timed)
    LOW_LEFT                         = 37  # Low posture left turn (timed)
    LOW_RIGHT                        = 38  # Low posture right turn (timed)

    STOP_INTERACTION                 = 39  # Stop interaction motion
    UP_AND_DOWN_FOR_TEST             = 40  # Up-and-down test motion

    ROLLOVER_RECOVERY_RIGHT          = 41  # Recover from right-side rollover
    ROLLOVER_RECOVERY_LEFT           = 42  # Recover from left-side rollover
    FLAILING                         = 43  # Flailing motion
    STOP_FLAILING                    = 44  # Stop flailing

    LIGHT_ON                         = 45  # Turn flashlight on
    LIGHT_OFF                        = 46  # Turn flashlight off

    ACTION_SEQUENCE_1                = 47  # Action sequence 1
    ACTION_SEQUENCE_2                = 48  # Action sequence 2
    ACTION_SEQUENCE_3                = 49  # Action sequence 3
    ACTION_SEQUENCE_4                = 50  # Action sequence 4

    SWING_LEFT_AND_RIGHT             = 52  # Swing left and right
    SWING_LEFT                       = 53  # Swing left
    SWING_RIGHT                      = 54  # Swing right
    EXCITED_INSPACE                  = 55  # Excited in-place motion
    LAZY_PAT_PAT                     = 56  # Lazy pat-pat motion
    CHEEKY_PAW                       = 57  # Cheeky paw motion
    WHINING                          = 58  # Whining motion
    SNIFF_FORWARD_INTERACTION        = 59  # Sniff forward (timed)
    SPACE_BACKWARD_INTERACTION       = 60  # Space-walk backward (timed)
    SNIFF_LEFT_INTERACTION           = 61  # Sniff left turn (timed)
    SNIFF_RIGHT_INTERACTION          = 62  # Sniff right turn (timed)
    SNIFF_STEP_INTERACTION           = 63  # Sniff step in place (timed)
    LEFT_ANGLE_INTERACTION           = 64  # Turn left by angle
    RIGHT_ANGLE_INTERACTION          = 65  # Turn right by angle

    # aliases (same numeric IDs)
    KEEP_IN_INTERACTION_MODE = 51
    STEP = 29
    FORWARD = 30
    BACK = 31
    LEFT = 32
    RIGHT = 33
    LEFT_ANGLE = 64
    RIGHT_ANGLE = 65
    STOP = 39
    LIGHT_ON_INTERACTION = 45
    LIGHT_OFF_INTERACTION = 46


# ---------------------------------------------------------------------------
# Interaction-type classification (mirrors firmware _get_interaction_type())
# ---------------------------------------------------------------------------

# Actions that take a *duration* parameter (seconds)
TIMER_BASED: Set[Action] = {
    Action.STEP_INTERACTION,
    Action.FORWARD_INTERACTION,
    Action.BACK_INTERACTION,
    Action.LEFT_INTERACTION,
    Action.RIGHT_INTERACTION,
    Action.LOW_FORWARD_AND_BACKWARD,
    Action.LOW_FORWARD,
    Action.LOW_BACKWARD,
    Action.LOW_LEFT,
    Action.LOW_RIGHT,
    Action.DANCE,
    Action.SLOW_DOWN_FOR_PROGRAM,
    Action.SIT_DOWN_FOR_PROGRAM,
    Action.SNIFF_FORWARD_INTERACTION,
    Action.SPACE_BACKWARD_INTERACTION,
    Action.SNIFF_LEFT_INTERACTION,
    Action.SNIFF_RIGHT_INTERACTION,
    Action.SNIFF_STEP_INTERACTION,
}

# Actions that take a *count* parameter (number of repetitions)
COUNT_BASED: Set[Action] = {
    Action.PUSH_UP,
    Action.SHAKE_HAND,
    Action.PEE,
    Action.TWIST,
    Action.NOD,
    Action.SHAKE_HEAD,
    Action.UP_AND_DOWN,
    Action.NEW_YEAR,
    Action.SHAKE_HAND_WITH_SIT_DOWN,
    Action.WAG_TAIL,
    Action.STOMP,
    Action.CELEBRATE,
    Action.FLAILING,
}

# Actions that take an *angle* parameter (degrees)
ANGLE_BASED: Set[Action] = {
    Action.LEFT_ANGLE_INTERACTION,
    Action.RIGHT_ANGLE_INTERACTION,
}

# ---------------------------------------------------------------------------
# Human-readable name lookup (supports both English and Chinese aliases)
# ---------------------------------------------------------------------------

# Maps lowercase English / Chinese string → Action enum value
# Developers can pass any of these strings to AiDog.perform_action().
ACTION_ALIASES: Dict[str, Action] = {
    # English names
    "idle":                       Action.IDLE,
    "slow_up":                    Action.SLOW_UP,
    "slow_down":                  Action.SLOW_DOWN,
    "sit_down":                   Action.SIT_DOWN,
    "stand_up":                   Action.STAND_UP,
    "shake_hand":                 Action.SHAKE_HAND,
    "nod":                        Action.NOD,
    "shake_head":                 Action.SHAKE_HEAD,
    "stretch":                    Action.STRETCH,
    "pee":                        Action.PEE,
    "twist":                      Action.TWIST,
    "push_up":                    Action.PUSH_UP,
    "new_year":                   Action.NEW_YEAR,
    "wag_tail":                   Action.WAG_TAIL,
    "stomp":                      Action.STOMP,
    "sniff":                      Action.SNIFF,
    "celebrate":                  Action.CELEBRATE,
    "jump":                       Action.JUMP,
    "dance":                      Action.DANCE,
    "kick_ball":                  Action.KICK_BALL,
    "touch_ground_right":         Action.TOUCH_GROUND_RIGHT,
    "touch_ground_left":          Action.TOUCH_GROUND_LEFT,
    "play_dead":                  Action.PLAY_DEAD,
    "step":                       Action.STEP_INTERACTION,
    "walk_forward":               Action.FORWARD_INTERACTION,
    "walk_back":                  Action.BACK_INTERACTION,
    "turn_left":                  Action.LEFT_INTERACTION,
    "turn_right":                 Action.RIGHT_INTERACTION,
    "turn_left_angle":            Action.LEFT_ANGLE_INTERACTION,
    "turn_right_angle":           Action.RIGHT_ANGLE_INTERACTION,
    "left_angle":                 Action.LEFT_ANGLE_INTERACTION,
    "right_angle":                Action.RIGHT_ANGLE_INTERACTION,
    "low_forward":                Action.LOW_FORWARD,
    "low_backward":               Action.LOW_BACKWARD,
    "low_left":                   Action.LOW_LEFT,
    "low_right":                  Action.LOW_RIGHT,
    "stop":                       Action.STOP_INTERACTION,
    "light_on":                   Action.LIGHT_ON,
    "light_off":                  Action.LIGHT_OFF,
    "rollover_recovery_right":    Action.ROLLOVER_RECOVERY_RIGHT,
    "rollover_recovery_left":     Action.ROLLOVER_RECOVERY_LEFT,
    "light_on_interaction":       Action.LIGHT_ON_INTERACTION,
    "light_off_interaction":      Action.LIGHT_OFF_INTERACTION,
    "swing_left_and_right":       Action.SWING_LEFT_AND_RIGHT,
    "swing_left":                 Action.SWING_LEFT,
    "swing_right":                Action.SWING_RIGHT,
    "excited_inspace":            Action.EXCITED_INSPACE,
    "lazy_pat_pat":               Action.LAZY_PAT_PAT,
    "cheeky_paw":                 Action.CHEEKY_PAW,
    "whining":                    Action.WHINING,
    "sniff_forward":              Action.SNIFF_FORWARD_INTERACTION,
    "space_backward":             Action.SPACE_BACKWARD_INTERACTION,
    "sniff_left":                 Action.SNIFF_LEFT_INTERACTION,
    "sniff_right":                Action.SNIFF_RIGHT_INTERACTION,
    "sniff_step":                 Action.SNIFF_STEP_INTERACTION,
    "sniff_forward_interaction":  Action.SNIFF_FORWARD_INTERACTION,
    "space_backward_interaction": Action.SPACE_BACKWARD_INTERACTION,
    "sniff_left_interaction":     Action.SNIFF_LEFT_INTERACTION,
    "sniff_right_interaction":    Action.SNIFF_RIGHT_INTERACTION,
    "sniff_step_interaction":     Action.SNIFF_STEP_INTERACTION,
    # Chinese names
    "坐下":   Action.SIT_DOWN,
    "站起":   Action.STAND_UP,
    "握手":   Action.SHAKE_HAND,
    "点头":   Action.NOD,
    "摇头":   Action.SHAKE_HEAD,
    "伸懒腰": Action.STRETCH,
    "撒尿":   Action.PEE,
    "俯卧撑": Action.PUSH_UP,
    "拜年":   Action.NEW_YEAR,
    "摇尾巴": Action.WAG_TAIL,
    "跺脚":   Action.STOMP,
    "嗅探":   Action.SNIFF,
    "庆祝":   Action.CELEBRATE,
    "跳跃":   Action.JUMP,
    "跳舞":   Action.DANCE,
    "踢球":   Action.KICK_BALL,
    "装死":   Action.PLAY_DEAD,
    "原地踏步": Action.STEP_INTERACTION,
    "前进":   Action.FORWARD_INTERACTION,
    "后退":   Action.BACK_INTERACTION,
    "左转":   Action.LEFT_INTERACTION,
    "右转":   Action.RIGHT_INTERACTION,
    "左转指定角度": Action.LEFT_ANGLE_INTERACTION,
    "右转指定角度": Action.RIGHT_ANGLE_INTERACTION,
    "停止":   Action.STOP_INTERACTION,
    "开灯":   Action.LIGHT_ON,
    "关灯":   Action.LIGHT_OFF,
    "左右摇摆": Action.SWING_LEFT_AND_RIGHT,
    "左摇摆": Action.SWING_LEFT,
    "右摇摆": Action.SWING_RIGHT,
    "太空步后退": Action.SPACE_BACKWARD_INTERACTION,
    "撒娇拍桌面": Action.LAZY_PAT_PAT,
    "脸颊招财": Action.CHEEKY_PAW,
    "撒泼打滚": Action.WHINING,
    "嗅探前进": Action.SNIFF_FORWARD_INTERACTION,
    "嗅探左转": Action.SNIFF_LEFT_INTERACTION,
    "嗅探右转": Action.SNIFF_RIGHT_INTERACTION,
    "嗅探踏步": Action.SNIFF_STEP_INTERACTION,
}

INTERACTION_ACTION_NAMES: List[str] = [
    "IDLE", "SLOW_UP", "SLOW_DOWN", "SLOW_DOWN_FOR_CHARGE", "SLOW_DOWN_FOR_PROGRAM", "UP_AND_DOWN",
    "EXCITED_UP_AND_DOWN", "SIT_DOWN", "SIT_DOWN_FOR_PROGRAM", "STAND_UP", "SHAKE_HAND",
    "SHAKE_HAND_WITH_SIT_DOWN", "NOD", "SHAKE_HEAD", "STRETCH", "PEE", "TWIST", "PUSH_UP", "NEW_YEAR",
    "WAG_TAIL", "STOMP", "SNIFF", "CELEBRATE", "JUMP", "DANCE", "KICK_BALL", "TOUCH_GROUND_RIGHT",
    "TOUCH_GROUND_LEFT", "PLAY_DEAD", "STEP", "FORWARD", "BACK", "LEFT", "RIGHT", "LOW_FORWARD_AND_BACKWARD",
    "LOW_FORWARD", "LOW_BACKWARD", "LOW_LEFT", "LOW_RIGHT", "STOP", "UP_AND_DOWN_FOR_TEST",
    "ROLLOVER_RECOVERY_RIGHT", "ROLLOVER_RECOVERY_LEFT", "FLAILING", "STOP_FLAILING",
    "LIGHT_ON_INTERACTION", "LIGHT_OFF_INTERACTION", "ACTION_SEQUENCE_1", "ACTION_SEQUENCE_2",
    "ACTION_SEQUENCE_3", "ACTION_SEQUENCE_4",
    "KEEP_IN_INTERACTION_MODE", "SWING_LEFT_AND_RIGHT", "SWING_LEFT", "SWING_RIGHT",
    "EXCITED_INSPACE", "LAZY_PAT_PAT", "CHEEKY_PAW", "WHINING",
    "SNIFF_FORWARD_INTERACTION", "SPACE_BACKWARD_INTERACTION", "SNIFF_LEFT_INTERACTION",
    "SNIFF_RIGHT_INTERACTION", "SNIFF_STEP_INTERACTION", "LEFT_ANGLE_INTERACTION",
    "RIGHT_ANGLE_INTERACTION",
]


class EarAction(IntEnum):
    IDLE = 0
    EAR_SHAKE_ASYN_1_3 = 1
    EAR_SHAKE_ASYN_1_2 = 2
    EAR_SHAKE_SYN = 3
    EAR_SHAKE_SYN_FOR_BLE = 4
    EAR_PEAR1 = 5
    EAR_PEAR2 = 6
    EAR_PEAR3 = 7
    EAR_STAND = 8
    EAR_STAND_LEFT = 9
    EAR_STAND_RIGHT = 10
    EAR_STAND_LEFT_AND_RIGHT = 11
    EAR_FOR_WINK = 12
    EAR_FOR_VIDEO = 13
    EAR_PERCENTAGE_BASIC = 14
    SPECIAL_DETECTION_AND_NOT_OPERATED_TOGGLE_BASIC = 15
    EAR_FLICK_EXCITED = 16
    EAR_FLICK_LEFT_QUICK = 17
    EAR_FLICK_RIGHT_QUICK = 18
    EAR_FLICK_ALTERNATE = 19
    EAR_FLICK_LEFT_AND_RIGHT_UP = 20
    EAR_FLICK_RANDOM = 21
    EAR_WIGGLE_SUBTLE_SELF_STABLE = 22
    EAR_FLICK_RANDOM_NEGATIVE = 23
    EAR_FLICK_RANDOM_POSITIVE = 24
    EAR_BREATHE = 25
    EAR_DOWN = 26

EAR_ACTION_NAMES: List[str] = [
    "EAR_IDLE",
    "EAR_SHAKE_ASYN_1_3", "EAR_SHAKE_ASYN_1_2", "EAR_SHAKE_SYN", "EAR_SHAKE_SYN_FOR_BLE",
    "EAR_PEAR1", "EAR_PEAR2", "EAR_PEAR3",
    "EAR_STAND", "EAR_STAND_LEFT", "EAR_STAND_RIGHT", "EAR_STAND_LEFT_AND_RIGHT",
    "EAR_FOR_WINK", "EAR_FOR_VIDEO",
    "EAR_PERCENTAGE_BASIC", "SPECIAL_DETECTION_AND_NOT_OPERATED_TOGGLE_BASIC",
    "EAR_FLICK_EXCITED", "EAR_FLICK_LEFT_QUICK", "EAR_FLICK_RIGHT_QUICK", "EAR_FLICK_ALTERNATE",
    "EAR_FLICK_LEFT_AND_RIGHT_UP", "EAR_FLICK_RANDOM", "EAR_WIGGLE_SUBTLE_SELF_STABLE",
    "EAR_FLICK_RANDOM_NEGATIVE", "EAR_FLICK_RANDOM_POSITIVE", "EAR_BREATHE", "EAR_DOWN",
]


class ExpressionAction(IntEnum):
    IDLE = 0
    HAPPY_01 = 1
    HAPPY_02 = 2
    HAPPY_03 = 3
    HAPPY_04 = 4
    SMILE_01 = 5
    SMILE_02 = 6
    SMILE_03 = 7
    LOVE_01 = 8
    LOVE_02 = 9
    ANGER_01 = 10
    ANGER_02 = 11
    ANGER_03 = 12
    ANGER_04 = 13
    SAD_01 = 14
    SAD_02 = 15
    SAD_03 = 16
    DOUBLE_SAD_03 = 17
    SAD_04 = 18
    SCARED_01 = 19
    SCARED_02 = 20
    COMFORTABLE_01 = 21
    COMFORTABLE_02 = 22
    DOUBT_01 = 23
    DOUBT_02 = 24
    DOUBT_03 = 25
    NERVOUS = 26
    NERVOUS_COMPLETE = 27
    TIRED = 28
    TIRED_COMPLETE = 29
    SLEEPY = 30
    SLEEPY_COMPLETE = 31
    WINK_FAST = 32
    WINK_NORMAL = 33
    LOOK_RIGHT = 34
    LOOK_LEFT = 35
    LOOK_LEFT_AND_RIGHT = 36
    NOTE_PARTICLE_CIRCLE = 37
    MUSIC = 38
    BASKETBALL = 39
    PINGPONG = 40
    FOOTBALL = 41
    SOUND_0 = 42
    SOUND_25 = 43
    SOUND_50 = 44
    SOUND_75 = 45
    SOUND_100 = 46
    SOUND_CIRCLE = 47
    GET_UP = 48
    EAT_SNACK = 49
    CHARGING = 50
    SUNGLASSES = 51
    EYES_FIGHTING = 52
    TURN_OFF = 53
    CARING = 54
    SHY = 55
    DRINK = 56
    ALERT = 57
    BORING = 58
    NO_WIFI = 59
    SHAME = 60
    SHAME_02 = 61
    SNIFF_EXPRESSION = 62
    DEAD = 63
    PRIDE = 64
    YAWN = 65
    LIGHT_ON = 66
    LIGHT_OFF = 67

    # Backward-compatible alias
    SNIFF = SNIFF_EXPRESSION


EXPRESSION_ACTION_NAMES: List[str] = [
    "IDLE",
    "HAPPY_01", "HAPPY_02", "HAPPY_03", "HAPPY_04",
    "SMILE_01", "SMILE_02", "SMILE_03",
    "LOVE_01", "LOVE_02",
    "ANGER_01", "ANGER_02", "ANGER_03", "ANGER_04",
    "SAD_01", "SAD_02", "SAD_03", "DOUBLE_SAD_03", "SAD_04",
    "SCARED_01", "SCARED_02",
    "COMFORTABLE_01", "COMFORTABLE_02",
    "DOUBT_01", "DOUBT_02", "DOUBT_03",
    "NERVOUS", "NERVOUS_COMPLETE",
    "TIRED", "TIRED_COMPLETE",
    "SLEEPY", "SLEEPY_COMPLETE",
    "WINK_FAST", "WINK_NORMAL",
    "LOOK_RIGHT", "LOOK_LEFT", "LOOK_LEFT_AND_RIGHT",
    "NOTE_PARTICLE_CIRCLE", "MUSIC",
    "BASKETBALL", "PINGPONG", "FOOTBALL",
    "SOUND_0", "SOUND_25", "SOUND_50", "SOUND_75", "SOUND_100", "SOUND_CIRCLE",
    "GET_UP", "EAT_SNACK", "CHARGING", "SUNGLASSES", "EYES_FIGHTING", "TURN_OFF",
    "CARING", "SHY", "DRINK", "ALERT", "BORING", "NO_WIFI", "SHAME", "SHAME_02", "SNIFF_EXPRESSION", "DEAD",
    "PRIDE", "YAWN", "LIGHT_ON", "LIGHT_OFF",
]


TONE_LIST: List[Tuple[int, str]] = [
    (1, "JEEZ"),
    (2, "UH"),
    (3, "EATING"),
    (4, "CHARGING"),
    (5, "CURIOUS"),
    (6, "SLEEPY"),
    (7, "HENG"),
    (8, "SAD"),
    (9, "ANGRY"),
    (10, "DOUBT"),
    (11, "AGREE"),
    (12, "ENHENG"),
    (13, "ALERT"),
    (14, "WAKE_UP"),
    (15, "COMFORT"),
    (16, "SIGH"),
    (17, "SNORE"),
    (18, "SNIFF"),
    (19, "BEAT1"),
    (20, "BEAT2"),
    (21, "BEAT3"),
    (22, "BEAT4"),
    (23, "BEAT5"),
    (24, "BEAT6"),
    (25, "BEAT7"),
]


class Tone(IntEnum):
    STOP = 0
    JEEZ = 1
    UH = 2
    EATING = 3
    CHARGING = 4
    CURIOUS = 5
    SLEEPY = 6
    HENG = 7
    SAD = 8
    ANGRY = 9
    DOUBT = 10
    AGREE = 11
    ENHENG = 12
    ALERT = 13
    WAKE_UP = 14
    COMFORT = 15
    SIGH = 16
    SNORE = 17
    SNIFF = 18
    BEAT1 = 19
    BEAT2 = 20
    BEAT3 = 21
    BEAT4 = 22
    BEAT5 = 23
    BEAT6 = 24
    BEAT7 = 25


def resolve_action(name_or_id) -> Action:
    """
    Convert a string name or integer to an :class:`Action`.

    Accepts:
    - An :class:`Action` enum member (returned as-is).
    - An integer matching a valid Action value.
    - A string key from :data:`ACTION_ALIASES` (case-insensitive for ASCII names).

    Raises :class:`ValueError` for unrecognised inputs.
    """
    if isinstance(name_or_id, Action):
        return name_or_id
    if isinstance(name_or_id, int):
        return Action(name_or_id)
    if isinstance(name_or_id, str):
        key = name_or_id.lower()
        if key in ACTION_ALIASES:
            return ACTION_ALIASES[key]
        # Try original casing (for Chinese strings that are already lowercase)
        if name_or_id in ACTION_ALIASES:
            return ACTION_ALIASES[name_or_id]
    raise ValueError(
        f"Unknown action {name_or_id!r}. "
        f"Use an Action enum member, an integer ID, or a name from ACTION_ALIASES."
    )
