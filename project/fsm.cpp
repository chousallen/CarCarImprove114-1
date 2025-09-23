#include "fsm.hpp"

FSM::FSM(): state(STATE_NODE)
{
}

void FSM::doRoutine()
{
    // Placeholder for FSM routine logic
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