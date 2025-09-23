#include "fsm.hpp"
#include "ir.hpp"
#include "node.h"
#include "track.h"
#include <Arduino.h>

uint8_t ir_data[N_IR];

//temp
char temp_action[] = "grbrbrbrblblblbls";
int temp_step = 0;
//temp

FSM::FSM(): state(STATE_NODE)
{
}

void FSM::doRoutine()
{
    // Placeholder for FSM routine logic
    readIR(ir_data);
    // Serial.print("Current state value: ");
    // Serial.println((int)state);
    
    if (state == STATE_NODE) {
        // Logic for NODE state: run forward for 700 ms after entering
        // Serial.println("state node");
        if ((unsigned long)(millis() - enterStateTime) < 700UL) {
            car_front();
        } else {
            temp_step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_STRAIGHT) {
        // Serial.println("state straight");
        int sum = ir_data[0] + ir_data[1] + ir_data[2] + ir_data[3] + ir_data[4];
        if(sum >= 4)
        {
            exitState();
            if (temp_action[temp_step] == 'f') {
                enterState(STATE_NODE);
            } else if (temp_action[temp_step] == 'r') {
                enterState(STATE_R_TURN);
            } else if (temp_action[temp_step] == 'l') {
                enterState(STATE_L_TURN);
            } else if (temp_action[temp_step] == 'b') {
                enterState(STATE_U_TURN);
            } else if (temp_action[temp_step] == 's') {
                enterState(STATE_STOP);
            } else if (temp_action[temp_step] == 'g') {
                enterState(STATE_START);
            } else {
                Serial.println(temp_action[temp_step]);
                enterState(STATE_STRAIGHT);
            }
        }
        else {
            tracking(ir_data[0], ir_data[1], ir_data[2], ir_data[3], ir_data[4]);
            // exitState();
            // enterState(STATE_STRAIGHT);
        }
        // Logic for LINE_FOLLOW state
    } else if (state == STATE_R_TURN) {
        // 0-100ms forward, 100-600ms right turn
        // Serial.println("state rturn");
        if ((unsigned long)(millis() - enterStateTime) < 200UL) {
            car_front();
        } else if ((unsigned long)(millis() - enterStateTime) < 700UL) {
            car_right();
        } else {
            temp_step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_L_TURN) {
        // 0-100ms forward, 100-600ms left turn
        // Serial.println("state lturn");
        if ((unsigned long)(millis() - enterStateTime) < 200UL) {
            car_front();
        } else if ((unsigned long)(millis() - enterStateTime) < 700UL) {
            car_left();
        } else {
            temp_step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_U_TURN) {
        // Serial.println("state uturn");
        if (millis() - enterStateTime < 570UL) {
            // Serial.println("Car back");
            car_back();
        } else {
            // Serial.println("exit u turn");
            temp_step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_START) {
        // Serial.println("state start");
        if ((unsigned long)(millis() - enterStateTime) < 500UL) {
            car_back();
        } else {
            temp_step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_STOP) {
        // Serial.println("state stop");
        car_end();
    } else {
        // Handle unexpected state
        // Serial.println("Unknown state!");
    }
}

FSM_State FSM::getState()
{
    return state;
}

void FSM::exitState()
{

}

void FSM::enterState(FSM_State newState)
{
    // Placeholder for enter state logic
    state = newState;
    Serial.print("Entering state: ");
    Serial.println((int)newState);
    // reset state timer on enter
    enterStateTime = millis();
}