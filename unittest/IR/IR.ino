#define N_IR_SEN 5

typedef int GPIO_t;
// Left to Right IR sensor GPIO pins
GPIO_t IR_sen[N_IR_SEN] = {A11, A12, A13, A14, A15};


void setup() {
  Serial.begin(115200);
  Serial.println("Start test IR");
}

void loop() {
  for (int i = 0; i < N_IR_SEN; i++) {
    int value = analogRead(IR_sen[i]);
    Serial.print(value);
    Serial.print(",");
  }
  Serial.println();
  delay(500); // Adjust delay as needed
}
