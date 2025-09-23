#include "fsm.hpp"
#include "ir.hpp"
#include "node.h"
#include "track.h"
#include "logger.h"
#include <Arduino.h>

uint8_t ir_data[N_IR];

char action[128];
int step = 0, n_action = 0;
logger fsm_logger(Serial, "fsm");

FSM::FSM(): state(STATE_NODE)
{
}

void FSM::doRoutine()
{
    // Placeholder for FSM routine logic
    if(Serial3.available())
    {
        action[n_action] = Serial3.read();
        fsm_logger.info("%c got", action[n_action]);
        if(action[n_action] == 10)
            return;
        n_action++;
    }
    if(n_action == step)
    {
        enterStateTime = millis();
        return;}
    readIR(ir_data);

    // fsm_logger.info("n_action: %d, step: %d, curr_state: %d", n_action, step, state);
    
    if (state == STATE_NODE) {
        // Logic for NODE state: run forward for 700 ms after entering
        // Serial.println("state node");
        if ((unsigned long)(millis() - enterStateTime) < 700UL) {
            car_front();
        } else {
            step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_STRAIGHT) {
        // Serial.println("state straight");
        int sum = ir_data[0] + ir_data[1] + ir_data[2] + ir_data[3] + ir_data[4];
        if(sum >= 4)
        {
            exitState();
            if (action[step] == 'f') {
                enterState(STATE_NODE);
            } else if (action[step] == 'r') {
                enterState(STATE_R_TURN);
            } else if (action[step] == 'l') {
                enterState(STATE_L_TURN);
            } else if (action[step] == 'b') {
                enterState(STATE_U_TURN);
            } else if (action[step] == 's') {
                enterState(STATE_STOP);
            } else if (action[step] == 'g') {
                enterState(STATE_START);
            } else {
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
            step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_L_TURN) {
        // 0-100ms forward, 100-600ms left turn
        // Serial.println("state lturn");
        if ((unsigned long)(millis() - enterStateTime) < 200UL) {
            car_front();
        } else if ((unsigned long)(millis() - enterStateTime) < 600UL) {
            car_left();
        } else {
            step++;
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
            step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_START) {
        // Serial.println("state start");
        if ((unsigned long)(millis() - enterStateTime) < 500UL) {
            car_back();
        } else {
            step++;
            exitState();
            enterState(STATE_STRAIGHT);
        }
    } else if (state == STATE_STOP) {
        car_end();
        step++;
        exitState();
        if (action[step] == 'f') {
            enterState(STATE_NODE);
        } else if (action[step] == 'r') {
            enterState(STATE_R_TURN);
        } else if (action[step] == 'l') {
            enterState(STATE_L_TURN);
        } else if (action[step] == 'b') {
            enterState(STATE_U_TURN);
        } else if (action[step] == 's') {
            enterState(STATE_STOP);
        } else if (action[step] == 'g') {
            enterState(STATE_START);
        } else {
            enterState(STATE_STRAIGHT);
        }
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
    fsm_logger.info("Enter state: %d", newState);
    // reset state timer on enter
    enterStateTime = millis();
}