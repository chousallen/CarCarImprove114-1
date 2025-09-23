/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

#define DEBUG // debug flag

// for RFID
#include <MFRC522.h>
#include <SPI.h>

// for bluetooth logger
#include "logger.h"

/*===========================define pin & create module object================================*/
// BlueTooth
// BT connect to Serial1 (Hardware Serial)
// Mega               HC05
// Pin  (Function)    Pin
// 18    TX       ->  RX
// 19    RX       <-  TX
// TB6612, 請按照自己車上的接線寫入腳位(左右不一定要跟註解寫的一樣)
// TODO: 請將腳位寫入下方
#define MotorR_I1 0   // 定義 A1 接腳（右）
#define MotorR_I2 0   // 定義 A2 接腳（右）
#define MotorR_PWMR 0 // 定義 ENA (PWM調速) 接腳
#define MotorL_I3 0   // 定義 B1 接腳（左）
#define MotorL_I4 0   // 定義 B2 接腳（左）
#define MotorL_PWML 0 // 定義 ENB (PWM調速) 接腳
// 循線模組, 請按照自己車上的接線寫入腳位
#define IRpin_LL 0
#define IRpin_L 0
#define IRpin_M 0
#define IRpin_R 0
#define IRpin_RR 0
// RFID, 請按照自己車上的接線寫入腳位
#define RST_PIN 0                 // 讀卡機的重置腳位
#define SS_PIN 0                  // 晶片選擇腳位
#define CTL_LOOP_PERIOD 10        // 100 Hz
MFRC522 mfrc522(SS_PIN, RST_PIN); // 建立MFRC522物件
uint64_t poweron_time;
logger btlog(Serial3, "car");
/*===========================define pin & create module object===========================*/

/*============setup============*/
void setup()
{
    // bluetooth initialization
    Serial3.begin(9600);
    // Serial window
    Serial.begin(115200);
    // RFID initial
    SPI.begin();
    mfrc522.PCD_Init();
    // TB6612 pin
    pinMode(MotorR_I1, OUTPUT);
    pinMode(MotorR_I2, OUTPUT);
    pinMode(MotorL_I3, OUTPUT);
    pinMode(MotorL_I4, OUTPUT);
    pinMode(MotorL_PWML, OUTPUT);
    pinMode(MotorR_PWMR, OUTPUT);
    // tracking pin
    pinMode(IRpin_LL, INPUT);
    pinMode(IRpin_L, INPUT);
    pinMode(IRpin_M, INPUT);
    pinMode(IRpin_R, INPUT);
    pinMode(IRpin_RR, INPUT);

    btlog.setLevel(LOG_DEBUG);
    btlog.setMirror(&Serial);
    poweron_time = millis();
#ifdef DEBUG
    btlog.debug("Start!");
    Serial.println("Start!");
#endif
}
/*============setup============*/

/*=====Import header files=====*/
#include "RFID.h"
#include "bluetooth.h"
#include "node.h"
#include "track.h"
#include "ir.h"
#include "fsm.h"
/*=====Import header files=====*/

/*===========================initialize variables===========================*/
int l2 = 0, l1 = 0, m0 = 0, r1 = 0, r2 = 0; // 紅外線模組的讀值(0->white,1->black)
int _Tp = 90;                               // set your own value for motor power
FSM_State state = STATE_NODE;               // set state to false to halt the car, set state to true to activate the car
FSM fsm;
/*===========================initialize variables===========================*/

/*===========================define function===========================*/
void loop()
{
    if (millis() - poweron_time >= CTL_LOOP_PERIOD)
    {
        poweron_time = millis();
        fsm.doRoutine();
        // Control loop code here
        if (millis() - poweron_time >= CTL_LOOP_PERIOD)
        {
            Serial.print("Control loop overrun!");
            Serial.print(uint32_t(millis() - poweron_time));
            Serial.println(" ms");
        }
    }
}
/*===========================define function===========================*/
