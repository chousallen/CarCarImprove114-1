#include "fsm.hpp"

// control loop period in milliseconds
#define CTL_LOOP_PERIOD 10 // 100 Hz

#define MotorL_I1 5     // 定義 A1 接腳（左）
#define MotorL_I2 6     // 定義 A2 接腳（左）
#define MotorL_PWML 11  // 定義 ENA (PWM調速) 接腳
#define MotorR_I3 2     // 定義 B1 接腳（右）
#define MotorR_I4 3     // 定義 B2 接腳（右）
#define MotorR_PWMR 12  // 定義 ENB (PWM調速) 接腳

// time in milliseconds since power on for managing control loop
uint64_t poweron_time;
// finite state machine instance
FSM fsm;

void setup()
{
    poweron_time = millis();
    Serial.begin(115200);
      // TB6612 pin
    pinMode(MotorL_I1, OUTPUT);
    pinMode(MotorL_I2, OUTPUT);
    pinMode(MotorR_I3, OUTPUT);
    pinMode(MotorR_I4, OUTPUT);
    pinMode(MotorR_PWMR, OUTPUT);
    pinMode(MotorL_PWML, OUTPUT);

}

void loop()
{
    if (millis() - poweron_time >= CTL_LOOP_PERIOD) {
        poweron_time = millis();
        fsm.doRoutine();
        // Control loop code here
        if(millis() - poweron_time >= CTL_LOOP_PERIOD)
        {
            Serial.print("Control loop overrun!");
            Serial.print(uint32_t(millis() - poweron_time));
            Serial.println(" ms");
        }
    }
}
