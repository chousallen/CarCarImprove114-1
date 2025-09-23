#include "fsm.hpp"
#include "ir.hpp"
#include <Arduino.h>

uint16_t ir_data[N_IR];

FSM::FSM(): state(STATE_NODE)
{
}

void FSM::doRoutine()
{
    // Placeholder for FSM routine logic
    readIR(ir_data);
    for (int i = 0; i < N_IR; ++i) {
        Serial.print(ir_data[i]);
        Serial.print(", ");
    }
    Serial.println();
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