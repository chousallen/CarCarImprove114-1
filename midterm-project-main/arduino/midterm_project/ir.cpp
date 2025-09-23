#include "ir.h"

uint8_t ir_pins[N_IR] = {A10, A11, A12, A13, A14};

void readIR(uint8_t *ir_values)
{
    for (int i = 0; i < N_IR; i++)
    {
        ir_values[i] = analogRead(ir_pins[i]) > THRESHOLD;
    }
}
