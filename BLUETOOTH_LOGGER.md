# Arduino HC-06 Bluetooth Logger

This document explains how to use the Arduino-side `BluetoothLogger` and the Python client to get leveled, formatted logs over Bluetooth (SPP) via an HC‑06 module.

## 1) Hardware wiring (Mega2560)

- HC‑06 VCC -> 5V (most breakouts accept 3.6–6V; check yours)
- HC‑06 GND -> GND
- HC‑06 TXD -> RX3 (pin 15)
- HC‑06 RXD -> TX3 (pin 14) through a level shifter or divider (3.3V logic)
- Common ground shared with Arduino

## 2) Arduino sketch

- Include `logger.h` and construct the logger with the Stream that talks to HC‑06 (Serial3 on Mega):

  ```cpp
  #include "logger.h"

  BluetoothLogger btlog(Serial3);

  void setup() {
    Serial.begin(115200);
    Serial3.begin(9600); // HC-06 default
    btlog.setLevel(BTLOG_DEBUG);
    btlog.setTag("car");
    btlog.setMirror(&Serial); // optional: also print frames to USB Serial

    btlog.info("Booting firmware v%s", "1.0.0");
  }

  void loop() {
    btlog.debug("tick=%lu", millis());
    delay(1000);
  }
  ```

- See `bt_comm/logger_example.ino` in this repo for a complete example.

## 3) Protocol

Each log is one line with percent-encoding of special characters:

```
L|level|millis|tag|message\n
```

- `level`: 0=TRACE, 1=DEBUG, 2=INFO, 3=WARN, 4=ERROR
- `millis`: Arduino `millis()` timestamp
- `tag`: optional module/component tag
- `message`: formatted printf-style string

## 4) Python client

- Install dependency (pyserial) and run. Replace `COM7` with your Windows Bluetooth COM port.

```powershell
python -m pip install --upgrade pip; pip install pyserial
python .\server.py --port COM7 --baud 9600 --level INFO
```

- The client prints time, relative time, level, tag, and message, filtering by the minimum level.

## Notes

- Pair with the HC‑06 first (PIN 1234 or 0000). Windows will create an outgoing COM port you can select.
- IntelliSense may show `Arduino.h` missing when editing outside of the Arduino IDE/platform; compile via Arduino IDE/CLI.
- You can integrate this logger into your existing `bt_comm/bt_comm.ino` by replacing direct `Serial3.print()` calls.
