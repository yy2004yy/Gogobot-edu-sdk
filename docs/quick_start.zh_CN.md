# 快速开始

本指南用于让 Gogobot EDU / Changba AI-Dog 机器狗完成第一次连接和安全动作测试。

## 1. 准备机器狗

- 将机器狗放在平整、空旷的地面。
- 运行运动示例前，确认周围有足够空间。
- 确认机器狗已开机，并且电脑在蓝牙范围内。
- 运行动作和运动示例时，确保你可以随时停止机器狗。

## 2. 安装 SDK

```bash
cd aidog_sdk
pip install -e .
```

可选依赖：

```bash
pip install -e ".[dev_pc_ws]"
pip install -e ".[bidir_audio]"
```

## 3. 扫描和连接

扫描设备：

```python
from aidog_sdk import AiDog

with AiDog() as dog:
    devices = dog.scan("Changba-Ai-Dog")
    print(devices)
```

按设备名前缀连接：

```python
from aidog_sdk import AiDog

with AiDog() as dog:
    dog.connect("Changba-Ai-Dog", retries=3, retry_delay_s=1.0)
    print("connected")
```

按已知蓝牙地址连接：

```python
dog.connect(address="AA:BB:CC:DD:EE:FF", retries=3, retry_delay_s=1.0)
```

## 4. 运行一个安全动作

```python
from aidog_sdk import AiDog, Action

with AiDog() as dog:
    dog.connect("Changba-Ai-Dog")
    ok = dog.perform_action(Action.SIT_DOWN, timeout_s=12.0)
    print("action_done:", ok)
```

## 5. 下一步示例

- `examples/01_connection/scan_and_connect.py`：BLE 扫描和连接。
- `examples/02_actions/basic_actions.py`：执行一个高级动作。
- `examples/02_actions/ears_expressions_audio.py`：耳朵、表情和提示音。
- `examples/03_movement/directional_move.py`：方向运动。
- `examples/04_sensors/imu_ble_read.py`：BLE IMU 数据流。
- `examples/04_sensors/tof_ble_read.py`：BLE TOF 数据流。

运行运动或高级姿态调节示例前，请先阅读 [安全说明](safety.md)。
