#include <MFRC522.h>
#include <SPI.h>

class RFID
{
public:
    RFID(uint8_t SDA, uint8_t RST); // SPI.begin() before this constructor is required.
    bool detectCard();              // Try to detect new card. Return false if no new card is detected.
    bool haveData() const;          // Check if a card has ever been detected.
    String getUid() const;          // Return the uid of last detected card.
    int getUidLen() const;          // Return the length of the uid of the last card.
    int getSak() const;             // Represents the type of the card

private:
    uint8_t RST_pin;
    uint8_t SDA_pin;
    MFRC522 *Mfrc;
};