#include <Arduino.h>
#include "logger.h"

// On Arduino Mega, HC-06 wired to Serial3 (RX3=15, TX3=14)

BluetoothLogger btlog(Serial3);

void setup()
{
  Serial.begin(115200);
  Serial3.begin(9600); // HC-06 default
  btlog.setLevel(BTLOG_DEBUG);
  btlog.setTag("car");
  btlog.setMirror(&Serial); // also echo formatted frames over USB for debug

  btlog.info("Booting firmware v%s", "1.0.0");
}

void loop()
{
  static unsigned long last = 0;
  unsigned long now = millis();
  if (now - last >= 1000)
  {
    last = now;
    int rpm = 1234;
    float temp = 36.5;
    btlog.debug("tick=%lu rpm=%d temp=%.1fC", now, rpm, temp);
  }

  // Simulate a warning
  if (now > 5000 && (now % 5000) < 20)
  {
    btlog.warn("Battery low: %d%%", 19);
  }
}
