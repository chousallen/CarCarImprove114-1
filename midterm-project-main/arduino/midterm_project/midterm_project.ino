/***************************************************************************/
// File       [final_project.ino]
// Author     [Erik Kuo]
// Synopsis   [Code for managing main process]
// Functions  [setup, loop, Search_Mode, Hault_Mode, SetState]
// Modify     [2020/03/27 Erik Kuo]
/***************************************************************************/

#define DEBUG // debug flag

// #include "bluetooth.h"
#include "ir.hpp"
#include "fsm.hpp"

// for bluetooth logger
#include "logger.h"
#include <SPI.h>
#include <MFRC522.h>

// RFID, 請按照自己車上的接線寫入腳位
#define RST_PIN 49                 // 讀卡機的重置腳位
#define SS_PIN 53                  // 晶片選擇腳位
#define CTL_LOOP_PERIOD 10        // 100 Hz
uint64_t poweron_time;
logger btlog(Serial, "car");
MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance
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
    mfrc522.PCD_Init();
    delay(4); // Optional delay. Some board do need more time after init to be ready

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
    if (mfrc522.PICC_IsNewCardPresent()) {
        mfrc522.PICC_ReadCardSerial();
        mfrc522.PICC_HaltA();
        int n = mfrc522.uid.size;
        mfrc522.uid.uidByte[n] = 0;
        char tmp[16] = "tmp";
        // sprintf(tmp, "%s", mfrc522.uid.uidByte);
        for(int i=0; i<n; i++)
        {
            Serial.print(mfrc522.uid.uidByte[i]);
        }
        Serial.println();
		btlog.debug("%s", mfrc522.uid.uidByte);
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
