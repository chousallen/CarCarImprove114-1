#pragma once

#include <stdint.h>

enum FSM_State
{
    STATE_NODE,
    STATE_STRAIGHT,
    STATE_R_TURN,
    STATE_L_TURN,
    STATE_U_TURN,
    STATE_STOP,
    STATE_START
};

class FSM
{
    public:
        FSM();
        void doRoutine();
        FSM_State getState();
    private:
        FSM_State state;
        unsigned long enterStateTime;
        void exitState();
        void enterState(FSM_State newState);
};