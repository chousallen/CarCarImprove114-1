/***************************************************************************/
// File			  [node.h]
// Author		  [Erik Kuo, Joshua Lin]
// Synopsis		[Code for managing car movement when encounter a node]
// Functions  [/* add on your own! */]
// Modify		  [2020/03/027 Erik Kuo]
/***************************************************************************/

/*===========================import variable===========================*/
int extern _Tp;
/*===========================import variable===========================*/
#include "track.h"
// TODO: add some function to control your car when encounter a node
// here are something you can try: left_turn, right_turn... etc.
double x = 2;  //time constant for motor speed
double adj_R = 1, adj_L = 0.9;  //motor speed correction coefficient

void car_front(){
    MotorWriting(adj_L*_Tp*x, adj_R*_Tp*x);
    // delay(700);
}

void car_back(){
    MotorWriting(adj_L*_Tp*x, -adj_R*_Tp*x*1.3);
    // delay(700);
}

void car_right(){
    // MotorWriting(adj_L*_Tp * x,adj_R*_Tp*x);
    // delay(100);
    MotorWriting(adj_L*_Tp*x,0);
    // delay(500);
}

void car_left(){
    // MotorWriting(adj_L*_Tp*x, adj_R*_Tp*x);
    // delay(100);
    MotorWriting(0, adj_R*_Tp*x*1.2);
    // delay(500);
}

void car_start(){
    // MotorWriting(adj_L*_Tp*x*0.1, adj_R*_Tp*x*0.1);
    // delay(200);
    MotorWriting(adj_L*_Tp*x*0.5, adj_R*_Tp*x*0.5);
    // delay(500);
}

void car_end(){
    MotorWriting(0,0);
    // delay(1000);
}