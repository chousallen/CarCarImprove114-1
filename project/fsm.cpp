#include "fsm.hpp"
#include "ir.hpp"
#include <Arduino.h>

uint8_t ir_data[N_IR];

FSM::FSM(): state(STATE_NODE)
{
}

void FSM::doRoutine()
{
    // Placeholder for FSM routine logic
    readIR(ir_data);
    switch(state) {
        case STATE_NODE:
            // Logic for NODE state
            break;
        case STATE_STRAIGHT:
            // Logic for LINE_FOLLOW state
            break;
        case STATE_R_TURN:
            // Logic for OBSTACLE_AVOIDANCE state
            break;
        case STATE_L_TURN:
            // Logic for STOP state
            break;
        default:
            // Handle unexpected state
            break;
    }
}

FSM_State FSM::getState()
{
    return state;
}

void FSM::exitState()
{
    // Placeholder for exit state logic
}

void FSM::enterState(FSM_State newState)
{
    // Placeholder for enter state logic
}