/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		[Code used for tracking]
// Functions  [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

#ifndef TRACK_H
#define TRACK_H

/*===========================import variable===========================*/
int _Tp = 60; 

#define MotorL_I1 5     // 定義 A1 接腳（左）
#define MotorL_I2 6     // 定義 A2 接腳（左）
#define MotorL_PWML 11  // 定義 ENA (PWM調速) 接腳
#define MotorR_I3 2     // 定義 B1 接腳（右）
#define MotorR_I4 3     // 定義 B2 接腳（右）
#define MotorR_PWMR 12  // 定義 ENB (PWM調速) 接腳
/*===========================import variable===========================*/

// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
    // TODO: use TB6612 to control motor voltage & direction
    if(vR >= 255) vR = 255;
    if(vL >= 255) vL = 255;
    if(vR <= -255) vR = -255;
    if(vL <= -255) vL = -255;

    if(vR < 0){
        digitalWrite(MotorR_I3, HIGH);
        digitalWrite(MotorR_I4, LOW);
        vR = -vR; 
    }
    else{
        digitalWrite(MotorR_I3, LOW);
        digitalWrite(MotorR_I4, HIGH);   
    }

    if(vL < 0){
        digitalWrite(MotorL_I1, HIGH);
        digitalWrite(MotorL_I2, LOW);
        vL = -vL; 
    }
    else{
        digitalWrite(MotorL_I1, LOW);
        digitalWrite(MotorL_I2, HIGH);
    }

    analogWrite(MotorL_PWML, vL);
    analogWrite(MotorR_PWMR, vR);
}  // MotorWriting

// Handle negative motor_PWMR value.
void MotorInverter(int motor, bool& dir) {
    // Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
}  // MotorInverter

// P/PID control Tracking
void tracking(int l2, int l1, int m0, int r1, int r2) {
    // TODO: find your own parameters!(Done)
    static double _w0 = 0;  //
    static double _w1 = 1;  //
    static double _w2 = 2;  //
    static double _Kp = 10;  // p term parameter
    static double _Kd = 5;  // d term parameter (optional)
    //double _Ki;  // i term parameter (optional) (Hint: 不要調太大)
    static double adj_R = 1; 
    static double adj_L = 0.9;  // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。
    static double x = 2;

    if((l2+l1+m0+r1+r2)!=0){
      double error = l2 * _w2 + l1 * _w1 + m0 * _w0 + r1 * (-_w1) + r2 * (-_w2);
      static double lastError;
      double dError = error - lastError;
      double vR, vL;  // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.

      // TODO: complete your P/PID tracking code (Done)
      double powerCorrection = _Kp * error + _Kd*dError;
      vR = (_Tp + powerCorrection);
      vL = (_Tp - powerCorrection);
      lastError = error;
      // end TODO
      MotorWriting(adj_L * vL * x, adj_R * vR * x);
    }
    else MotorWriting(adj_L * _Tp * x, adj_R * _Tp * x);
}  // tracking

#endif