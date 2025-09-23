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