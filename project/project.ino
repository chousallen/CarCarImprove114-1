#include "fsm.hpp"

// control loop period in milliseconds
#define CTL_LOOP_PERIOD 10 // 100 Hz

// time in milliseconds since power on for managing control loop
uint64_t poweron_time;
// finite state machine instance
FSM fsm;

void setup()
{
    poweron_time = millis();
    Serial.begin(115200);
}

void loop()
{
    if (millis() - poweron_time >= CTL_LOOP_PERIOD) {
        // Control loop code here

        if(millis() - poweron_time >= CTL_LOOP_PERIOD)
        {
            Serial.print("Control loop overrun!");
            Serial.print(uint32_t(millis() - poweron_time));
            Serial.println(" ms");
        }
        poweron_time = millis();
    }
}