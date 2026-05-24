# Examples

The examples are organized by feature area so users can quickly choose the right entry point. Start with connection and sensors before running movement or robot-adjustment scripts.

## Risk Levels

| Level | Meaning |
|---|---|
| Low | Reads state or opens a host service; does not command physical robot movement |
| Medium | Runs actions or movement using normal high-level APIs |
| High | Changes body, foot, or joint targets; requires matching firmware and careful supervision |

## Recommended Order

1. `01_connection/scan_and_connect.py`
2. `04_sensors/imu_ble_read.py`
3. `04_sensors/tof_ble_read.py`
4. `02_actions/basic_actions.py`
5. `02_actions/ears_expressions_audio.py`
6. `03_movement/directional_move.py`
7. `04_sensors/imu_ws_lan_read.py`
8. `04_sensors/tof_ws_lan_read.py`
9. `05_audio/bidirectional_pcm_ws_host.py`
10. `06_robot_adjust/safe_pose_adjust.py`

## Index

| Path | Purpose | Risk | Typical command |
|---|---|---|---|
| `01_connection/scan_and_connect.py` | Scan and connect to first matching BLE device | Low | `python examples/01_connection/scan_and_connect.py` |
| `01_connection/connect_by_address.py` | Connect to a known BLE address or UUID | Low | `python examples/01_connection/connect_by_address.py --address AA:BB:CC:DD:EE:FF` |
| `02_actions/basic_actions.py` | Run one high-level action | Medium | `python examples/02_actions/basic_actions.py --action sit_down` |
| `02_actions/ears_expressions_audio.py` | Control ears, expression, and tone | Low/Medium | `python examples/02_actions/ears_expressions_audio.py` |
| `02_actions/choreography.py` | Run a short scripted show | Medium | `python examples/02_actions/choreography.py --yes` |
| `03_movement/directional_move.py` | Move in one selected direction | Medium | `python examples/03_movement/directional_move.py --direction forward --duration 2 --yes` |
| `03_movement/timed_move.py` | Run a timed movement sequence | Medium | `python examples/03_movement/timed_move.py --duration 2 --yes` |
| `04_sensors/imu_ble_read.py` | Read BLE IMU stream | Low | `python examples/04_sensors/imu_ble_read.py --hz 20` |
| `04_sensors/tof_ble_read.py` | Read BLE TOF stream | Low | `python examples/04_sensors/tof_ble_read.py --hz 20 --mode both` |
| `04_sensors/imu_ws_lan_read.py` | Read LAN WebSocket IMU sensor JSON | Low | `python examples/04_sensors/imu_ws_lan_read.py --bind 0.0.0.0 --port 8766` |
| `04_sensors/tof_ws_lan_read.py` | Read LAN WebSocket TOF sensor JSON | Low | `python examples/04_sensors/tof_ws_lan_read.py --bind 0.0.0.0 --port 8766` |
| `05_audio/bidirectional_pcm_ws_host.py` | Run bidirectional PCM audio host | Low | `python examples/05_audio/bidirectional_pcm_ws_host.py --bind 0.0.0.0 --port 8766` |
| `06_robot_adjust/safe_pose_adjust.py` | Run low-amplitude body/foot adjustment | High | `python examples/06_robot_adjust/safe_pose_adjust.py --yes` |
| `06_robot_adjust/custom_action.py` | Run custom sniff-like robot-adjustment action | High | `python examples/06_robot_adjust/custom_action.py --yes` |

## Common Arguments

- `--name-prefix`: BLE advertisement prefix, default `Changba-Ai-Dog`.
- `--address`: BLE address on Windows/Linux or platform UUID on macOS.
- `--timeout`: auto-exit or operation timeout, depending on the example.
- `--hz`: requested sensor stream rate.
- `--bind`: WebSocket bind address.
- `--port`: WebSocket bind port.
- `--yes`: skip interactive confirmation for movement or high-risk examples.

Read `../docs/safety.md` before running medium or high-risk examples.
