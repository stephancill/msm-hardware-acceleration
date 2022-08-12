import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles, Timer

@cocotb.test()
async def test_modmul_example(dut):
    """ Test modular multiplication """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    s = 65521

    dut.reset.value = 1
    dut.s.value = s
    dut.m.value = int(2**(2*dut.FIELD_WIDTH.value) / s)
    dut.a.value = 64111
    dut.b.value = 11195

    await ClockCycles(dut.clk, 1)

    dut.reset.value = 0

    await ClockCycles(dut.clk, 200)

    assert dut.ab.value.integer == dut.a.value.integer * dut.b.value.integer, "Full multiplication failed"
    assert dut.ab_msb.value.integer == 10951, "MSB of full multiplication failed"
    assert dut.ab_lsb.value.integer == 234517, "LSB of full multiplication failed"
    assert dut.l1_msb.value.integer == 10953, "MSB of l1 failed"
    assert dut.l1_s_lsb.value.integer == 163385, "LSB of l1*s failed"
    assert dut.r.value.integer == dut.ab.value.integer % dut.s.value.integer, "Modular multiplication failed"

@cocotb.test()
async def test_modmul_random(dut):
    """ Test modular multiplication with random inputs """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    s = 65521

    dut.reset.value = 1
    dut.s.value = s
    dut.m.value = int(2**(2*dut.FIELD_WIDTH.value) / s)

    for _ in range(100):

        dut.a.value = random.randrange(0, 2**dut.FIELD_WIDTH.value)
        dut.b.value = random.randrange(0, 2**dut.FIELD_WIDTH.value)

        await ClockCycles(dut.clk, 1)

        dut.reset.value = 0

        await ClockCycles(dut.clk, 200)

        print(dut.r.value.integer, dut.ab.value.integer % dut.s.value.integer)

        assert dut.ab.value.integer == dut.a.value.integer * dut.b.value.integer, "Full multiplication failed"
        assert dut.r.value.integer == dut.ab.value.integer % dut.s.value.integer, "Modular multiplication failed"


