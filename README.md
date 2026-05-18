# Gogobot EDU SDK

Python SDK for the **Changba AI-Dog / Gogobot EDU** robot: control the quadruped over BLE from scripts, with optional Wi‑Fi audio helpers.

---

## English Guide

### 1) Installation

```bash
cd aidog_sdk
pip install -e .
```

Requirements:

- Python >= 3.9  
- `bleak >= 0.21` (pulled in as a dependency)

### 2) Quick start

```python
from aidog_sdk import AiDog, Action, EarAction, ExpressionAction, Tone, Movement

with AiDog() as dog:
    # Option A: scan by name prefix and connect the first match
    dog.connect("Changba-Ai-Dog", retries=3, retry_delay_s=1.0)

    # Option B: connect by known BLE address
    # dog.connect(address="AA:BB:CC:DD:EE:FF", retries=3, retry_delay_s=1.0)

    dog.perform_action(Action.SIT_DOWN)
    dog.perform_action("shake_hand")
    ok = dog.perform_action(Action.SHAKE_HAND, timeout_s=12.0)
    print("action_done:", ok)

    dog.send_movement(Movement.FORWARD)
    dog.stop_movement()

    dog.send_ear(EarAction.EAR_STAND_LEFT)
    dog.send_ear_percentage(80)
    dog.disable_special_detection()

    dog.send_expression(ExpressionAction.HAPPY_01)

    dog.send_audio(Tone.JEEZ)
    dog.send_audio(Tone.STOP)
```

Optional constructor flag (for IMU/TOF streaming examples): `AiDog(imu_only_notify=True)` — keeps legacy behavior where some firmware builds tie sensor streaming to notification routing; prefer handling IMU/TOF in callbacks.

### 2.1) Bidirectional PCM WebSocket host (PC server)

Run the **example script**: it uses ``DevPcWebSocketHost(..., connection_handler=...)`` (same class as LAN sensor example ``08``) for the WebSocket server and bidirectional PCM tasks.

1. In firmware `app_config.h`:

   ```c
   #define DEV_PC_AUDIO_WS_ENABLE 1
   #define DEV_PC_AUDIO_WS_URL "ws://<PC_LAN_IP>:8765"
   ```

2. On the PC (same LAN as the robot):

   (a) Install deps:
   ```bash
   pip install websockets sounddevice numpy
   ```

   (b) (Optional but recommended) Print available audio devices and pick indices:
   ```bash
   python -c "import sounddevice as sd; print(sd.query_devices())"
   ```

   (c) Start the host (single command):
   ```bash
   cd aidog_sdk
   python examples/04_audio_ws_bidirectional_host.py --bind 0.0.0.0 --port 8765 --input-device <MIC_IDX> --output-device <SPK_IDX>
   ```

3. Binary WebSocket frames are raw PCM: **16 kHz**, **16-bit signed little-endian**, **mono**. The script resamples mic input to that format for uplink.

### 2.2) IMU / TOF over LAN (Dev PC WebSocket, text frames)

On Wi‑Fi, the robot can connect to your PC using `DEV_PC_AUDIO_WS_URL` (same feature as bidirectional audio). Besides **binary** PCM frames, recent firmware also sends **text** WebSocket messages containing the same JSON as BLE characteristic `ae04` (`imu` / `tof` fields). This avoids BLE throughput limits when you only need sensor data on the LAN.

**Firmware:** enable `DEV_PC_AUDIO_WS_ENABLE` and set `DEV_PC_AUDIO_WS_URL` to `ws://<your_PC_LAN_IP>:8765` (port must match your host). You need a build that includes the sensor mirror to Dev PC WS (this repository’s `app_control_protocal.c` + `dev_pc_audio_ws`).

**Python (SDK class):**

```bash
pip install -e ".[dev_pc_ws]"
```

```python
from aidog_sdk import AiDog, DevPcWebSocketHost

dog = AiDog()

def on_imu(imu: dict):
    print("imu", imu.get("yaw_deg"), imu.get("pitch_deg"), imu.get("roll_deg"))

host = DevPcWebSocketHost(host="0.0.0.0", port=8765, dog=dog, on_imu=on_imu)
host.start()
# … robot connects; feed_sensor_stream_json runs internally → get_latest_imu() works too …
host.stop()
dog.shutdown()
```

- Pass `dog=` so `feed_sensor_stream_json` updates `get_latest_imu` / `get_latest_tof` and any `add_imu_listener` / `add_tof_listener` callbacks.
- Optional BLE: connect and call `request_imu_stream` / `request_tof_stream` if you need to change stream enable/rate from the host (defaults on many builds already stream IMU+TOF).

**Example script:** `examples/08_sensor_ws_lan.py`

### 3) Examples (`examples/`)

| File | Purpose |
|------|---------|
| `01_connect.py` | Scan, list devices, connect by address |
| `02_actions.py` | Actions, ears, expression, tones |
| `03_movement.py` | Directional movement |
| `04_audio_ws_bidirectional_host.py` | Bidirectional PCM WebSocket host (PC side) |
| `05_imu_read.py` | Subscribe to IMU JSON on `ae04`, interactive print |
| `06_tof_read.py` | Subscribe to TOF JSON on `ae04` |
| `07_Servo_Control.py` | Smooth pose / foot / joint adjustment (`MODE_ROBOT_ADJUST`) |
| `08_sensor_ws_lan.py` | IMU/TOF over LAN via Dev PC WebSocket (`DevPcWebSocketHost`) |

Custom motion design note:
- For custom choreography based on `syn_pose_adjust` / `syn_foot_adjust` / `syn_joint_adjust`, follow the same preparation pattern as `examples/07_Servo_Control.py` and `examples/demo_2_custom_action.py`.
- Recommended sequence:
  1) Enter/ensure `BASIC_MODE` (`request_basic_mode()`),
  2) disable special detection (`disable_special_detection()`),
  3) move to a known baseline pose (`default_pose_output(...)`),
  4) run your custom motion sequence,
  5) request `BASIC_MODE` again and re-enable special detection.
- This helps avoid interference from autonomous behavior and improves repeatability of designed motions.

### 4) Connection APIs

| API | Description |
|-----|-------------|
| `scan(name_prefix="Changba-Ai-Dog")` | Scan BLE devices; returns `[(name, address), ...]` |
| `connect(name_prefix="Changba-Ai-Dog", *, address=None, retries=3, retry_delay_s=1.0)` | Connect by prefix scan or direct `address` |
| `disconnect()` | Disconnect current device |
| `shutdown()` | Disconnect and stop the background BLE thread |
| `is_connected` | Property: connection state |

### 5) Control APIs

| API | Description |
|-----|-------------|
| `perform_action(action, *, duration=None, count=None, timeout_s=20.0, require_running_state=True)` | Interaction action; waits for firmware completion flag when available |
| `send_interaction(action_id, param=None)` | Send interaction action ID |
| `start_movement(direction)` / `send_movement(direction, *, duration_s=None)` | Movement by `Movement` or raw direction byte; when `duration_s` is set, auto-stops after duration |
| `send_offsets(direction="STOP")` | Full sport parameter packet |
| `move(direction_deg, velocity=1.0, *, walk=False, speed=False)` | Legacy degree-based wrapper |
| `stop_movement()` / `reset()` | Stop motion; `reset` also sends interaction STOP-style cleanup |
| `send_ear(...)` / `send_ear_percentage(...)` | Ear behavior controls |
| `enable_special_detection()` / `disable_special_detection()` / `set_special_detection(enable=...)` | Explicitly enable/disable special detection |
| `toggle_special_detection()` | Legacy toggle command |
| `send_expression(...)` / `send_audio(...)` | Expression and tone |
| `get_action_list()` | Read action list JSON from `ae10` (if firmware exposes it) |
| `send_raw(mode, data)` | Raw packet `[0xAA,0x55,0x00,mode,...]` for extensions |

Movement timing note:
- `send_movement(..., duration_s=5.0)` blocks for the given seconds and then calls `stop_movement()` automatically.
- If you need non-blocking movement, call `send_movement(direction)` without `duration_s`, then stop explicitly later.
**Sensor streams (JSON on `ae04` notify):**

| API | Description |
|-----|-------------|
| `request_imu_stream(enable=True, hz=20)` | Ask firmware to stream IMU in `ae04` JSON |
| `get_latest_imu()` | Last parsed IMU dict (`yaw_deg` / `pitch_deg` / `roll_deg`, etc.) |
| `add_imu_listener(cb)` / `remove_imu_listener(cb)` | Callbacks for each IMU payload |
| `request_tof_stream(enable=True, hz=20)` | Ask firmware to include TOF in the same `ae04` JSON |
| `get_latest_tof()` | Last parsed TOF dict |
| `add_tof_listener(cb)` / `remove_tof_listener(cb)` | Callbacks for TOF payloads |
| `parse_notify_json_text(text)` | Parse one `ae04`-style JSON line (static helper) |
| `feed_sensor_stream_json(text)` | Apply LAN/WebSocket sensor JSON like a BLE notify (updates latest + listeners) |
| `DevPcWebSocketHost` | PC-side WebSocket server for Dev PC URL; demux text sensors + binary PCM; optional `connection_handler` for custom sessions (e.g. bidirectional audio example) |

**Robot adjustment (smooth interpolation, `MODE_ROBOT_ADJUST = 0x0A`; requires matching firmware):**

| API | Description |
|-----|-------------|
| `syn_pose_adjust(items, duration_ms)` | COG / pose keys (e.g. `cog_z`) |
| `syn_foot_adjust(items, duration_ms)` | Foot X/Z targets |
| `syn_joint_adjust(items, duration_ms)` | Joint delta adjustments |
| `default_pose_output(roll, pitch, x, z)` | Move to caller-specified default pose (`roll/pitch` in deg, `x/z` in mm) |
| `request_basic_mode()` | Request return to basic mode after adjustments |

**Wi‑Fi audio helpers:**

| API | Description |
|-----|-------------|
| `run_dev_pc_websocket_server(handler, host, port, ...)` | Async helper: same `websockets.serve` defaults as Dev PC URL (used by `DevPcWebSocketHost` and `examples/04_…`) |
| `DevPcWebSocketHost(...)` | WebSocket server for `DEV_PC_AUDIO_WS_URL`; text = sensor JSON, binary = PCM |
| `microphone_start()` / `microphone_stop()` | Mic capture session (`MODE_STREAM` commands) |
| `speaker_start()` / `speaker_write_pcm()` / `speaker_stop()` | Speaker PCM push session |

### 6) Enums and name tables

Exported from `aidog_sdk`: `Action`, `EarAction`, `ExpressionAction`, `Tone`, `Movement`, `INTERACTION_ACTION_NAMES`, `EAR_ACTION_NAMES`, `EXPRESSION_ACTION_NAMES`, `TONE_LIST`, `ACTION_ALIASES`, `resolve_action`, and mode constants such as `MODE_SPORT`, `MODE_ROBOT_ADJUST`, etc.

### 7) BLE protocol reference

- Packet: `[0xAA, 0x55, 0x00, mode, ...data]`
- Modes include: `MODE_SPORT`, `MODE_INTERACTION`, `MODE_EAR`, `MODE_EXPRESSION`, `MODE_AUDIO`, `MODE_SENSOR`, `MODE_STREAM`, `MODE_ROBOT_ADJUST` (0x0A).

**Characteristics (typical):**

- `ae03`: write control packets  
- `ae02`: device → host notifications (state JSON, etc.)  
- `ae04`: sensor stream notifications (IMU/TOF JSON, depending on firmware flags)  
- `ae10`: read action definition JSON (optional)

The SDK subscribes to `ae02` and `ae04` by default; it does **not** subscribe to legacy `ae05` indicate — use `ae04` for IMU/TOF.

### 8) Reliability

- `connect(...)` supports `retries` and `retry_delay_s`.  
- BLE writes use internal retries to reduce transient failures.

### 9) Action completion field

When present in notify JSON, `interaction_task_status` drives `perform_action` waiting:

- `0` — not running / finished  
- `1` — running  
- `2` — killed / interrupted  

If the field is missing, update firmware accordingly.

Notes for scripted choreography:

- `perform_action(Action.SLOW_DOWN)` and `perform_action(Action.SIT_DOWN)` are blocking calls.
- In choreography where precise timing matters, prefer `Action.SLOW_DOWN_FOR_PROGRAM` with `duration=...` to control crouch time more predictably.
- For combinations like "action + expression/sound", send expression/sound first and trigger the action last, because `perform_action(...)` blocks until firmware reports completion.

---

## 中文说明

### 1）安装

```bash
cd aidog_sdk
pip install -e .
```

环境要求：

- Python >= 3.9  
- `bleak >= 0.21`（随依赖安装）

### 2）快速开始

```python
from aidog_sdk import AiDog, Action, EarAction, ExpressionAction, Tone, Movement

with AiDog() as dog:
    # 方式1：按设备名前缀扫描并连接第一个匹配设备
    dog.connect("Changba-Ai-Dog", retries=3, retry_delay_s=1.0)

    # 方式2：已知蓝牙地址时直连
    # dog.connect(address="AA:BB:CC:DD:EE:FF", retries=3, retry_delay_s=1.0)

    dog.perform_action(Action.SIT_DOWN)
    dog.perform_action("shake_hand")  # 也支持字符串 / 别名
    ok = dog.perform_action(Action.SHAKE_HAND, timeout_s=12.0)
    print("action_done:", ok)

    dog.send_movement(Movement.FORWARD)
    dog.stop_movement()

    dog.send_ear(EarAction.EAR_STAND_LEFT)
    dog.send_ear_percentage(80)
    dog.disable_special_detection()

    dog.send_expression(ExpressionAction.HAPPY_01)

    dog.send_audio(Tone.JEEZ)
    dog.send_audio(Tone.STOP)
```

部分固件下传感器流与 notify 路由有关，可使用 `AiDog(imu_only_notify=True)`；IMU/TOF 数据建议在回调中处理。

### 2.1）双向音频 WebSocket（上位机脚本）

运行 **`examples/04_audio_ws_bidirectional_host.py`**：与 ``08`` 相同，通过 ``DevPcWebSocketHost(..., connection_handler=...)`` 起服务并实现双向 PCM。固件中配置 `DEV_PC_AUDIO_WS_ENABLE` 与 `DEV_PC_AUDIO_WS_URL`，电脑与狗在同一局域网即可（16 kHz、16-bit 有符号小端单声道 PCM）。

启动步骤（方式 B）：
1) 在 PC 上安装依赖：
```bash
pip install websockets sounddevice numpy
```
2) （推荐）先查询声卡设备并选择索引：
```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```
3) 用一条命令启动（把 `<MIC_IDX>/<SPK_IDX>` 换成你的索引）：
```bash
python examples/04_audio_ws_bidirectional_host.py --bind 0.0.0.0 --port 8765 --input-device <MIC_IDX> --output-device <SPK_IDX>
```


### 2.2）局域网 IMU/TOF（Dev PC WebSocket 文本帧）

机器狗连上 Wi‑Fi 后，可按 ``DEV_PC_AUDIO_WS_URL`` 作为 **WebSocket 客户端**连接你的电脑（与双向音频共用一条连接）。除 **二进制** PCM 外，新固件会通过 **文本帧**推送与 BLE ``ae04`` 一致的传感器 JSON（``imu`` / ``tof``），便于在局域网下更高频、更稳定地取数。

**固件：**打开 ``DEV_PC_AUDIO_WS_ENABLE``，将 ``DEV_PC_AUDIO_WS_URL`` 设为 ``ws://<电脑局域网IP>:8765``（端口与上位机监听一致）。需编译包含「传感器 JSON 镜像到 Dev PC WS」的固件（本仓库 ``app_control_protocal.c``、``dev_pc_audio_ws`` 相关改动）。

**Python：**

```bash
pip install -e ".[dev_pc_ws]"
```

```python
from aidog_sdk import AiDog, DevPcWebSocketHost

dog = AiDog()
host = DevPcWebSocketHost(host="0.0.0.0", port=8765, dog=dog, on_imu=lambda m: print(m))
host.start()
# 狗连上后，内部会 feed_sensor_stream_json → get_latest_imu 与 listener 与 BLE 语义一致
host.stop()
dog.shutdown()
```

可选：再连 BLE 调用 ``request_imu_stream`` / ``request_tof_stream`` 调整开关与频率（不少固件默认已开启 IMU+TOF）。

**示例：** ``examples/08_sensor_ws_lan.py``

### 3）示例脚本（`examples/`）

| 文件 | 说明 |
|------|------|
| `01_connect.py` | 扫描、列出设备、按地址连接 |
| `02_actions.py` | 动作、耳朵、表情、提示音 |
| `03_movement.py` | 方向运动 |
| `04_audio_ws_bidirectional_host.py` | 双向 PCM WebSocket 上位机 |
| `05_imu_read.py` | 订阅 `ae04` 中 IMU JSON |
| `06_tof_read.py` | 订阅 `ae04` 中 TOF JSON |
| `07_Servo_Control.py` | 机身 / 足端 / 关节平滑调节（`MODE_ROBOT_ADJUST`） |
| `08_sensor_ws_lan.py` | 局域网 WebSocket 收 IMU/TOF（`DevPcWebSocketHost`） |

自定义动作设计提示：
- 如果你要基于 `syn_pose_adjust` / `syn_foot_adjust` / `syn_joint_adjust` 设计自定义动作，建议先参考 `examples/07_Servo_Control.py` 与 `examples/demo_2_custom_action.py` 的前置流程。
- 推荐顺序：
  1) 先进入/确认 `BASIC_MODE`（`request_basic_mode()`），
  2) 关闭特殊状态检测（`disable_special_detection()`），
  3) 回到可预期的基准姿态（`default_pose_output(...)`），
  4) 执行自定义动作序列，
  5) 结束后再次请求 `BASIC_MODE`，并重新开启特殊状态检测。
- 这样可以减少自主行为干扰，提升动作编排的一致性和可复现性。

### 4）连接相关接口

| 接口 | 说明 |
|------|------|
| `scan(name_prefix="Changba-Ai-Dog")` | 扫描蓝牙设备，返回 `[(name, address), ...]` |
| `connect(name_prefix="Changba-Ai-Dog", *, address=None, retries=3, retry_delay_s=1.0)` | 按前缀扫描或 `address` 直连；支持失败重试 |
| `disconnect()` | 断开当前设备 |
| `shutdown()` | 断开并关闭后台 BLE 线程 |
| `is_connected` | 是否已连接 |

### 5）核心控制接口

| 接口 | 说明 |
|------|------|
| `perform_action(action, *, duration=None, count=None, timeout_s=20.0, require_running_state=True)` | 交互动作；在固件回传完成标志时等待结束 |
| `send_interaction(action_id, param=None)` | 发送交互动作 ID |
| `start_movement(direction)` / `send_movement(direction, *, duration_s=None)` | 按 `Movement` 或方向字节运动；设置 `duration_s` 后会在指定时长后自动停止 |
| `send_offsets(direction="STOP")` | 发送完整运动参数包 |
| `move(direction_deg, velocity=1.0, *, walk=False, speed=False)` | 兼容角度接口，内部映射为方向控制 |
| `stop_movement()` / `reset()` | 停止运动；`reset` 含交互侧清理 |
| `send_ear(...)` / `send_ear_percentage(...)` | 耳朵控制 |
| `enable_special_detection()` / `disable_special_detection()` / `set_special_detection(enable=...)` | 显式开启/关闭特殊状态检测 |
| `toggle_special_detection()` | 兼容旧固件的翻转命令 |
| `send_expression(...)` / `send_audio(...)` | 表情与提示音 |
| `get_action_list()` | 从 `ae10` 读取动作列表 JSON（设备支持时） |
| `send_raw(mode, data)` | 原始扩展包 `[0xAA,0x55,0x00,mode,...]` |

运动时长说明：
- `send_movement(..., duration_s=5.0)` 会阻塞等待对应秒数，随后自动调用 `stop_movement()`。
- 若需要非阻塞控制，请不传 `duration_s`，并在后续手动调用 `stop_movement()`。
**传感器流（`ae04` JSON）：**

| 接口 | 说明 |
|------|------|
| `request_imu_stream(enable=True, hz=20)` | 请求开启/关闭 IMU 上报 |
| `get_latest_imu()` | 最近一次解析的 IMU（含 `yaw_deg` / `pitch_deg` / `roll_deg` 等） |
| `add_imu_listener(cb)` / `remove_imu_listener(cb)` | IMU 回调 |
| `request_tof_stream(enable=True, hz=20)` | 请求在同一 `ae04` JSON 中带 TOF |
| `get_latest_tof()` | 最近一次 TOF 数据 |
| `add_tof_listener(cb)` / `remove_tof_listener(cb)` | TOF 回调 |
| `parse_notify_json_text(text)` | 解析单行 ``ae04`` 风格 JSON（静态方法） |
| `feed_sensor_stream_json(text)` | 将局域网文本帧按 BLE notify 同样方式更新 latest + 监听器 |
| `DevPcWebSocketHost` | 电脑端 WebSocket 服务：文本=传感器 JSON，二进制=PCM；可选 `connection_handler` 自定义会话（如双向音频示例） |

**机身平滑调节（`MODE_ROBOT_ADJUST = 0x0A`，需固件支持）：**

| 接口 | 说明 |
|------|------|
| `syn_pose_adjust(items, duration_ms)` | 质心/姿态等 |
| `syn_foot_adjust(items, duration_ms)` | 足端 X/Z |
| `syn_joint_adjust(items, duration_ms)` | 关节增量 |
| `default_pose_output(roll, pitch, x, z)` | 输出到调用者指定的默认姿态（`roll/pitch` 单位度，`x/z` 单位 mm） |
| `request_basic_mode()` | 请求回到基础模式 |

**Wi‑Fi 音频：**

| 接口 | 说明 |
|------|------|
| `run_dev_pc_websocket_server(handler, host, port, ...)` | 异步工具：与 Dev PC URL 相同的 ``websockets.serve`` 约定（``DevPcWebSocketHost`` 与 ``examples/04_…`` 使用） |
| `DevPcWebSocketHost(...)` | ``DEV_PC_AUDIO_WS_URL`` 对应的上位机 WebSocket |
| `microphone_start()` / `microphone_stop()` | 麦克风采集会话控制 |
| `speaker_start()` / `speaker_write_pcm()` / `speaker_stop()` | 扬声器 PCM 推流 |

### 6）枚举与名称表

可从包根导入：`Action`、`EarAction`、`ExpressionAction`、`Tone`、`Movement`、`INTERACTION_ACTION_NAMES`、`EAR_ACTION_NAMES`、`EXPRESSION_ACTION_NAMES`、`TONE_LIST`、`ACTION_ALIASES`、`resolve_action`，以及 `MODE_SPORT`、`MODE_ROBOT_ADJUST` 等模式常量。

### 7）底层 BLE 协议

- 包格式：`[0xAA, 0x55, 0x00, mode, ...data]`
- 模式值含：`MODE_SPORT`、`MODE_INTERACTION`、`MODE_EAR`、`MODE_EXPRESSION`、`MODE_AUDIO`、`MODE_SENSOR`、`MODE_STREAM`、`MODE_ROBOT_ADJUST`（0x0A）

**特征约定：**

- `ae03`：写入控制数据  
- `ae02`：通知（设备 → 主机）  
- `ae04`：传感器流（IMU/TOF 等 JSON，视固件开关）  
- `ae10`：读取动作列表（可选）  

SDK 默认订阅 `ae02` 与 `ae04`，**不**订阅旧版 `ae05`：传感器数据以 `ae04` 为准。

### 8）稳定性与重试

- `connect(...)` 支持 `retries`、`retry_delay_s`  
- 内部对 BLE 写入有重试，减轻瞬时失败  

### 9）动作完成回传

依赖固件 notify JSON 字段 `interaction_task_status`：

- `0`：未运行 / 已结束  
- `1`：执行中  
- `2`：被中断  

若固件无该字段，请升级固件。

编排脚本提示：

- `perform_action(Action.SLOW_DOWN)` 和 `perform_action(Action.SIT_DOWN)` 都是阻塞调用。
- 如果希望精确控制趴下时长，建议优先使用 `Action.SLOW_DOWN_FOR_PROGRAM` 并传入 `duration=...`。
- 当“动作 + 表情/声音”组合时，建议先发表情/声音，再发动作（动作放后面），因为 `perform_action(...)` 会阻塞等待动作结束。

---

## Project layout

```text
aidog_sdk/
├── aidog_sdk/
│   ├── __init__.py
│   ├── _ble.py
│   ├── actions.py
│   ├── dev_pc_ws.py
│   └── dog.py
├── examples/
│   ├── 01_connect.py
│   ├── 02_actions.py
│   ├── 03_movement.py
│   ├── 04_audio_ws_bidirectional_host.py
│   ├── 05_imu_read.py
│   ├── 06_tof_read.py
│   ├── 07_Servo_Control.py
│   └── 08_sensor_ws_lan.py
├── pyproject.toml
└── README.md
```
