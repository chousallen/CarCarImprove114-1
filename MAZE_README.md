# Maze Explorer - Bluetooth & RFID Integration Guide

## System Overview

The system consists of three main parts:

1. Path Planning & Command Generation
2. Bluetooth Communication
3. RFID Detection & Scoring

### Current Implementation Flow:

```
[Path Planning] -> [Bluetooth Commands] -> [Car Movement] -> [RFID Detection] -> [Score Update]
   (maze.py)         (BTinterface.py)      (Arduino)         (Arduino)          (gui_scoreboard.py)
```

## Bluetooth Integration Points

### 1. BTinterface.py

This is the main file you need to modify. Current implementation:

```python
def send_action(self, dirc):
    # Sends single character commands:
    # 'f': forward
    # 'b': u-turn
    # 'r': turn right
    # 'l': turn left
    # 's': stop
    self.bt.serial_write_string(dirc)

def get_ok(self):
    # Expects "ok" after each movement
    return self.bt.serial_read_string()

def get_UID(self):
    # Currently expects hex string format
    return self.bt.serial_read_byte()
```

### Required Modifications:

1. **Command Protocol**:

   - Current: Single character commands ('f', 'b', 'r', 'l', 's')
   - You can modify `send_action()` if you need a different command format
   - Make sure to update Arduino code accordingly

2. **Movement Confirmation**:

   - Current: Expects exactly "ok" string
   - Modify `get_ok()` if you need a different confirmation format
   - The system waits for this confirmation before sending next command

3. **RFID Reading**:
   - Current: Reads hex string format (e.g., "10BA617E")
   - Modify `get_UID()` to match your RFID output format
   - Important: Return "0" or empty string if no RFID detected

## RFID Integration

### Current RFID Flow:

1. Car detects RFID tag
2. Arduino sends UID through Bluetooth
3. `get_UID()` receives the UID
4. System updates score via `scoreboard.add_UID(uid)`

### RFID Format Requirements:

- Current format: 8-character hex string (e.g., "10BA617E")
- If you need to change format, modify:
  1. `BT.py`: `serial_read_byte()` function
  2. `gui_scoreboard.py`: `add_UID()` function's input processing

## Testing Your Changes

1. Use `test.py` to verify your modifications:

```bash
python test.py
```

- Shows complete command sequence
- Simulates Bluetooth communication
- Displays RFID detection and scoring

2. Test Bluetooth commands individually:

```python
from BTinterface import BTInterface
bt = BTInterface(port="COM3")  # Use your port
bt.send_action('f')  # Test forward command
response = bt.get_ok()  # Check response
```

## Important Files and Functions

1. **BTinterface.py**

   - Main Bluetooth communication interface
   - Key functions to modify: `send_action()`, `get_ok()`, `get_UID()`

2. **BT.py**

   - Low-level Bluetooth operations
   - Modify if you need to change communication protocol

3. **gui_scoreboard.py**
   - Handles RFID scoring
   - `add_UID()`: Processes RFID and updates score

## Command Sequence Example

```
Starting at Node 1 (facing LEFT):
1. 'f' -> Move to Node 7
2. 'l' -> Turn South
3. 'l' -> Turn East
4. 'r' -> Move to Node 3
...
```

## Notes for Arduino Implementation

1. **Movement Commands**:

   - Must send "ok" after completing each movement
   - Don't send next RFID until current movement is complete

2. **RFID Detection**:

   - Send UID immediately when detected
   - Format: 8-character hex string
   - Send "0" or empty if no RFID

3. **Error Handling**:
   - If movement fails, don't send "ok"
   - System will timeout and stop after 10 seconds without "ok"

## Testing Checklist

1. [ ] Basic movement commands (f, b, r, l, s)
2. [ ] Movement confirmation ("ok" response)
3. [ ] RFID detection and transmission
4. [ ] Error handling
5. [ ] Complete path navigation
