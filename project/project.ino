
// control loop period in milliseconds
#define CTL_LOOP_PERIOD 10 // 100 Hz

// time in milliseconds since power on for managing control loop
uint64_t poweron_time;

void setup()
{
    poweron_time = millis();
    Serial.begin(115200);
}

void loop()
{
    if (millis() - poweron_time >= CTL_LOOP_PERIOD) {
        // Control loop code here
        poweron_time = millis();
        
    }
}