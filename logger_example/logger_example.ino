#include <Arduino.h>
#include "logger.h"
// On Arduino Mega, HC-06 wired to Serial3 (RX3=15, TX3=14)

logger btlog(Serial3, "car");
logger copylog(btlog, "copy");

void setup()
{
  Serial.begin(115200);
  Serial3.begin(9600); // HC-06 default
  btlog.setLevel(LOG_DEBUG);
  // tag is assigned in constructor
  btlog.setMirror(&Serial); // also echo formatted frames over USB for debug

  btlog.info("btlog is alive");
  copylog.info("copylog is alive");
}

void loop()
{
  if (Serial.available())
  {
    String s = Serial.readString();
    btlog.info("serial said: %s", s.c_str());
    Serial3.println(s.c_str());
  }
  if (Serial3.available())
  {
    String s = Serial3.readString();
    Serial.println(s.c_str());
  }
}
