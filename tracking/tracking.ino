#define MotorL_I1 2     // 定義 A1 接腳（左）
#define MotorL_I2 3     // 定義 A2 接腳（左）
#define MotorL_PWML 11  // 定義 ENA (PWM調速) 接腳
#define MotorR_I3 5     // 定義 B1 接腳（右）
#define MotorR_I4 6     // 定義 B2 接腳（右）
#define MotorR_PWMR 12  // 定義 ENB (PWM調速) 接腳

// 循線模組, 請按照自己車上的接線寫入腳位
#define IRpin_LL 40
#define IRpin_L 38
#define IRpin_M 36
#define IRpin_R 34
#define IRpin_RR 32

/*===========================initialize variables===========================*/
int l2 = 0, l1 = 0, m0 = 0, r1 = 0, r2 = 0;  // 紅外線模組的讀值(0->white,1->black)
int _Tp = 100;                                // set your own value for motor power
bool state = true;     // set state to false to halt the car, set state to true to activate the car
char cmd[] = "rrrruuullll"
/*===========================initialize variables===========================*/

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600)

  // TB6612 pin
  pinMode(MotorL_I1, OUTPUT);
  pinMode(MotorL_I2, OUTPUT);
  pinMode(MotorR_I3, OUTPUT);
  pinMode(MotorR_I4, OUTPUT);
  pinMode(MotorR_PWMR, OUTPUT);
  pinMode(MotorL_PWML, OUTPUT);

  // tracking pin
  pinMode(IRpin_LL, INPUT);
  pinMode(IRpin_L, INPUT);
  pinMode(IRpin_M, INPUT);
  pinMode(IRpin_R, INPUT);
  pinMode(IRpin_RR, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

}
