#pragma once
#include <stdint.h>
#include "Arduino.h"

// Define the number of IR sensors
#define N_IR 5
#define THRESHOLD 400

extern uint8_t ir_pins[N_IR];

void readIR(uint8_t* ir_values);