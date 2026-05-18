"""Example 01 — BLE scan and connect.

Finds nearby dogs by name, connects to the first match, then waits for Enter before disconnecting.

Run: python examples/01_connect.py
"""

from aidog_sdk import AiDog

dog = AiDog()

# --- Step 1: Scan devices ---
print("Scanning for AI-Dog devices...")
devices = dog.scan("Changba-Ai-Dog")

if not devices:
    print("No devices found. Make sure the robot is powered on and within BLE range.")
    dog.shutdown()
    raise SystemExit(1)

print(f"Found {len(devices)} device(s):")
for name, addr in devices:
    print(f"  {name}  [{addr}]")

# --- Step 2: Connect to the first device ---
name, addr = devices[0]
print(f"\nConnecting: {name} ({addr}) ...")
dog.connect(address=addr)

print("Connected! Press Enter to disconnect.")
input()

dog.disconnect()
dog.shutdown()
