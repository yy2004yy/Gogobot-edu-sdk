# Demo Asset Guide

Demo videos help users understand what each SDK example does on the real robot.

## Current Image Assets

| Asset | Preview |
|---|---|
| `../images/gogo-readme.jpg` | ![Gogobot EDU robot](../images/gogo-readme.jpg) |
| `../images/logo-text.png` | ![Gogobot EDU text logo](../images/logo-text.png) |
| `../images/logo2.png` | ![Gogobot EDU icon logo](../images/logo2.png) |

## Recommended Assets

| File | Content | Related Example | Recommended Length |
|---|---|---|---|
| `quick_start_actions.gif` | Sit, shake hand, expression, sound | `examples/02_actions/basic_actions.py` | 10-20 seconds |
| `movement_demo.gif` | Forward, back, left, right, stop | `examples/03_movement/timed_move.py` | 10-15 seconds |
| `imu_tof_stream.gif` | Terminal IMU/TOF stream with robot pose or distance change | `examples/04_sensors/imu_read.py`, `examples/04_sensors/tof_read.py` | 15-25 seconds |
| `dev_pc_websocket_demo.gif` | LAN WebSocket receiving sensor JSON | `examples/04_sensors/sensor_ws_lan.py` | 15-25 seconds |
| `bidirectional_audio_demo.gif` | PC microphone/speaker audio loop | `examples/05_audio/bidirectional_pcm_ws_host.py` | 15-25 seconds |
| `robot_adjust_demo.gif` | Low-amplitude body/foot/joint adjustment | `examples/06_robot_adjust/safe_pose_adjust.py` | 10-15 seconds |

## Guidelines

- Prefer real robot footage.
- Show terminal command/output when it helps users map code to behavior.
- Keep GIF/WebP previews small enough for GitHub README loading.
- Store large MP4 files in release assets, CDN, or an official video account, then link them from the docs.
- Keep file names lowercase and descriptive.
