#include "RFID.h"
#include <MFRC522.h>
#include <SPI.h>

RFID::RFID(uint8_t _SDA, uint8_t _RST) : SDA_pin(_SDA), RST_pin(_RST), Mfrc(new MFRC522(_SDA, _RST))
{
  Mfrc->PCD_Init();
}

bool RFID::detectCard()
{
  if (!Mfrc->PICC_IsNewCardPresent())
  {
    return false;
  }
  Mfrc->PICC_ReadCardSerial();
  Mfrc->PICC_HaltA();
  return true;
}

bool RFID::haveData() const
{
  return (Mfrc->uid.size > 0);
}

String RFID::getUid() const
{
  String uidstr = "";
  int len = Mfrc->uid.size;

  for (int i = 0; i < len; i++)
    uidstr += String(Mfrc->uid.uidByte[i], HEX);

  return uidstr;
}

int RFID::getUidLen() const
{
  return Mfrc->uid.size;
}

int RFID::getSak() const
{
  return Mfrc->uid.sak;
}