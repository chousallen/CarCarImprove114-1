#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN   53   // RC522 SDA/SS
#define RST_PIN  49    // RC522 RST

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  while (!Serial) { ; }
  SPI.begin();
  mfrc522.PCD_Init();

  mfrc522.PCD_DumpVersionToSerial();

  Serial.println("Ready. Tap a tag to read UID.");
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  Serial.print("UID:");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) Serial.print(" 0");
    else                               Serial.print(" ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println();

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}
