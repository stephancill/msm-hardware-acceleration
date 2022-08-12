import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles, Timer
import pytest 
from cocotb_test.simulator import run
import os

@cocotb.test()
async def test_modmul_example_16_bit(dut):
    """ Test modular multiplication """

    if dut.FIELD_WIDTH.value != 16:
        return

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
async def test_modmul_example_32_bit(dut):
    """ Test modular multiplication """

    if dut.FIELD_WIDTH.value != 32:
        return

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    s = 4294967291

    dut.reset.value = 1
    dut.s.value = s
    dut.m.value = 4294967301
    dut.a.value = 1152833672
    dut.b.value = 2546222476

    await ClockCycles(dut.clk, 1)

    dut.reset.value = 0

    await ClockCycles(dut.clk, 200)

    assert dut.ab.value.integer == dut.a.value.integer * dut.b.value.integer, "Full multiplication failed"
    assert dut.ab_msb.value.integer == 683444320, "MSB of full multiplication failed"
    assert dut.ab_lsb.value.integer == 3699053152, "LSB of full multiplication failed"
    assert dut.l1_msb.value.integer == 683444320, "MSB of l1 failed"
    assert dut.l1_s_lsb.value.integer == 13762647584, "LSB of l1*s failed"
    assert dut.r.value.integer == 2821307461, "Modular multiplication failed"


@cocotb.test()
async def test_modmul_random(dut):
    """ Test modular multiplication with random inputs """

    # TODO: Try pytest for parameterized tests https://github.com/themperek/cocotb-test/blob/master/tests/test_parameters.py

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    print("testing with", dut.FIELD_WIDTH.value, "bits")

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

# TODO: Fix weird errors
@pytest.mark.parametrize(
    "parameters", [{"FIELD_WIDTH": "16"}]
)
def test_modmul_testcase(parameters):
    run(
        verilog_sources=[os.path.join("..", "..", "src", "ModMul", "ModMul.v")],
        toplevel="ModMul",
        module="test_modmul",
        parameters=parameters,
        extra_env=parameters,
        sim_build="sim_build/"
        + "_".join(("{}={}".format(*i) for i in parameters.items()))
    )
