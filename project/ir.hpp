#pragma once
#include <stdint.h>
#include "Arduino.h"

// Define the number of IR sensors
#define N_IR 5

extern uint8_t ir_pins[N_IR];

void readIR(uint16_t* ir_values);