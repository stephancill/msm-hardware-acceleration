import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles, Timer

@cocotb.test()
async def test_buffer_simple(dut):
    """ Test that d propagates to q """

    for i in range(10):
        val = random.randint(0, 1)
        dut.A.value = val  # Assign the random value val to the input port d
        await Timer(250, units="ns")
        assert dut.B.value == val, "output B was incorrect on the {}th cycle".format(i)