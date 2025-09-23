#pragma once

#include <stdint.h>

enum FSM_State
{
    STATE_NODE,
    STATE_STRAIGHT,
    STATE_R_TURN,
    STATE_L_TURN,
    STATE_U_TURN,
};

class FSM
{
public:
    FSM();
    FSM_State doRoutine();
    FSM_State getState();

private:
    FSM_State state;
    void exitState();
    void enterState(FSM_State newState);
};