import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles, Timer

@cocotb.test()
async def test_modmul(dut):
    """ Test modular multiplication """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    s = 65521

    dut.reset.value = 1
    dut.s.value = s
    dut.m.value = int(2**dut.FIELD_WIDTH.value / s)
    dut.a.value = 64111
    dut.b.value = 11195

    await ClockCycles(dut.clk, 1)

    dut.reset.value = 0

    await ClockCycles(dut.clk, 2)

    assert dut.ab.value.integer == dut.a.value.integer * dut.b.value.integer, "Full multiplication failed"



