#define MotorR_I1 5     // 定義 A1 接腳（右）
#define MotorR_I2 6     // 定義 A2 接腳（右）
#define MotorR_PWMR 12  // 定義 ENA (PWM調速) 接腳
#define MotorL_I3 2     // 定義 B1 接腳（左）
#define MotorL_I4 3     // 定義 B2 接腳（左）
#define MotorL_PWML 11  // 定義 ENB (PWM調速) 接腳

#define N_IR_SEN 5

typedef int GPIO_t;
// Left to Right IR sensor GPIO pins
GPIO_t IR_sen[N_IR_SEN] = {A11, A12, A13, A14, A15};
int value[N_IR_SEN] = {0};
// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
    // TODO: use TB6612 to control motor voltage & direction
    if(vL >= 0)
    {
      digitalWrite(MotorL_I3, LOW);
      digitalWrite(MotorL_I4, HIGH);
      analogWrite(MotorL_PWML, vL);
    }
    if(vL < 0)
    {
      digitalWrite(MotorL_I3, HIGH);
      digitalWrite(MotorL_I4, LOW);
      analogWrite(MotorL_PWML, -vL);
    }
    if(vR >= 0)
    {
      digitalWrite(MotorR_I1, LOW);
      digitalWrite(MotorR_I2, HIGH);
      analogWrite(MotorR_PWMR, vR);
    }
    if(vR < 0)
    {
      digitalWrite(MotorR_I1, HIGH);
      digitalWrite(MotorR_I2, LOW);
      analogWrite(MotorR_PWMR, -vR);
    }
}  // MotorWriting

void tracking(int l2, int l1, int m0, int r1, int r2) {
    // TODO: find your own parameters!
    double _w0 = 0.0;  //
    double _w1 = 1.5;  //
    double _w2 = 2.0;  //
    double _Kp;  // p term parameter
    double _Kd;  // d term parameter (optional)
    double _Ki;  // i term parameter (optional) (Hint: 不要調太大)
    double error = l2 * _w2 + l1 * _w1 + m0 * _w0 + r1 * (-_w1) + r2 * (-_w2);
    double vR = 250 * 0.7;
    double vL = 225 * 0.7;  // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.
    double adj_R = 1, adj_L = 1;  // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。

    // TODO: complete your P/PID tracking code
    if(l2 + l1 + m0 + r1 + r2 != 0) error /= l2 + l1 + m0 + r1 + r2;
    if(error < 0)
    {
      adj_L = 1 / (-1) * error;
    }
    else if(error > 0)
    {
      adj_R = 1 / error;
    }

    // end TODO
    MotorWriting(adj_L * vL, adj_R * vR);
}  // tracking


void setup() {
  // put your setup code here, to run once:
  pinMode(MotorR_I1, OUTPUT);
  pinMode(MotorR_I2, OUTPUT);
  pinMode(MotorL_I3, OUTPUT);
  pinMode(MotorL_I4, OUTPUT);
  pinMode(MotorL_PWML, OUTPUT);
  pinMode(MotorR_PWMR, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  //  for (int i = 0; i < N_IR_SEN; i++) {
  //   value[i] = (analogRead(IR_sen[i]) >= 300);
  // }
  // if(value[0] & value[1] & value[2] & value[4])
  // {
  //   MotorWriting(45, 50);
  //   delay(100);
  //   MotorWriting(45, -50);
  //   delay(250);
  //   MotorWriting(0, 0);
  // }
  // tracking(value[0], value[1], value[2], value[3], value[4]);
  MotorWriting(225, 250);
}
