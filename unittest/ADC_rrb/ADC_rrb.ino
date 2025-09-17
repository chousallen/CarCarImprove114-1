const uint8_t channels[5] = {A10, A11, A12, A13, A14};
uint16_t adc_val[5] = {0};

void setup() {
  Serial.begin(115200);
  Serial.println("Start ADC round robin");
}

unsigned long cnt = 0;

unsigned long last = 0;

void loop() {
  if(millis() - last > 1000)
  {  
    last = millis();
    for(int i=0; i<5; i++)
    {
      Serial.print(adc_val[i]);
      Serial.print('\t');
    }
    Serial.println();
    Serial.println(1000*(double)cnt/millis());
  }
  for(int i=0; i<5; i++)
  {
    adc_val[i] = analogRead(channels[i]);
  }
  cnt++;
}
