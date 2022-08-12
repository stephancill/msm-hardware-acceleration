import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles, Timer

@cocotb.test()
async def test_modmul(dut):
    """ Test modular multiplication """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    dut.reset = 1
    dut.n = 16
    dut.s = 65521
    dut.m = 2**dut.n / dut.s
    dut.a = 64111
    dut.b = 11195

    await ClockCycles(dut.clk, 1)

    dut.reset = 0

    await ClockCycles(dut.clk, 20)

    print(dut.ab.value)


