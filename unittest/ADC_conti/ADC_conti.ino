volatile unsigned long isr_cnt = 0;
volatile uint16_t adcValues[5];
volatile uint8_t currentChannel = 0;
const uint8_t channels[5] = {A10, A11, A12, A13, A14};

void setup() {
  Serial.begin(115200);
  Serial.println("Start continuous ADC");

  // Set first channel
  ADMUX = (ADMUX & 0xE0) | (channels[currentChannel] & 0x07);
  ADCSRB = (ADCSRB & 0xF8) | ((channels[currentChannel] >> 3) & 0x03);

  // Enable ADC, interrupt, prescaler 128 (125 kHz ADC clock at 16 MHz)
  ADCSRA = (1 << ADEN) | (1 << ADIE) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);

  // Start first conversion
  ADCSRA |= (1 << ADSC);
}

ISR(ADC_vect) {
  isr_cnt ++;
  adcValues[currentChannel] = ADC; // store result

  // Move to next channel
  currentChannel++;
  if (currentChannel >= 5) currentChannel = 0;

  // Set next channel
  ADMUX = (ADMUX & 0xE0) | (channels[currentChannel] & 0x07);
  ADCSRB = (ADCSRB & 0xF8) | ((channels[currentChannel] >> 3) & 0x03);

  // Start next conversion
  ADCSRA |= (1 << ADSC);
}

void loop() {
  // Example: print values
  for (int i = 0; i < 5; i++) {
    Serial.print(adcValues[i]);
    Serial.print("\t");
  }
  Serial.println();
  Serial.print("Sampling rate: ");
  Serial.println(1000*(double)isr_cnt / millis());
  delay(1000);
}
