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
            int sum = ir_data[0] + ir_data[1] + ir_data[2] + ir_data[3] + ir_data[4];
            if(sum == N_IR)
            {
                exitState();
                enterState(STATE_R_TURN);
            }
            // Logic for LINE_FOLLOW state
            break;
        case STATE_R_TURN:
            // Logic for R_TURN state
            break;
        case STATE_L_TURN:
            // Logic for L_TURN state
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

    state = newState;
}