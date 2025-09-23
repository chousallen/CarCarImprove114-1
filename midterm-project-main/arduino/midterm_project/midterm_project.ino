/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

#define DEBUG // debug flag

#include "RFID.h"
#include "bluetooth.h"
#include "ir.hpp"
#include "fsm.hpp"

// for bluetooth logger
#include "logger.h"

// RFID, 請按照自己車上的接線寫入腳位
#define RST_PIN 49                 // 讀卡機的重置腳位
#define SS_PIN 53                  // 晶片選擇腳位
#define CTL_LOOP_PERIOD 10        // 100 Hz
RFID RFID(SS_PIN, RST_PIN); // 建立MFRC522物件
uint64_t poweron_time;
logger btlog(Serial, "car");
/*===========================define pin & create module object===========================*/

/*============setup============*/
void setup()
{
    // bluetooth initialization
    Serial3.begin(9600);
    // Serial window
    Serial.begin(115200);
    Serial.println("Start!");
    // RFID initial
    SPI.begin();

    btlog.setLevel(LOG_DEBUG);
    btlog.setMirror(&Serial);
    poweron_time = millis();
    btlog.debug("Start!");
}
/*============setup============*/

FSM fsm;
/*===========================initialize variables===========================*/

/*===========================define function===========================*/
void loop()
{
    if(RFID.detectCard())
    {
        Serial.println(RFID.getUid());
    }
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
