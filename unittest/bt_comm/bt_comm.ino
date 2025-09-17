void setup() {
  Serial.begin(115200);
  Serial3.begin(9600);
  Serial.println("Arduino Mega Starts");
  Serial3.println("Arduino Mega Starts");
}

void loop() {
  if(Serial.available())
  {
    Serial3.println(Serial.readString());
  }
  if(Serial3.available())
  {
    Serial.println(Serial3.readString());
  }

}
