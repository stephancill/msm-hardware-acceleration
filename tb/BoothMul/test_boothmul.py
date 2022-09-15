import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles, Timer
import pytest 
from cocotb_test.simulator import run
import os

# Warning: Do not name test methods with the prefix "test_"
# otherwise pytest will execute them as tests. 
# https://github.com/themperek/cocotb-test/issues/153

# @cocotb.test()
# async def boothmul_example_16_bit(dut):
#     """ Test booth multiplication """

#     if dut.N.value != 16:
#         return

#     clock = Clock(dut.Clk, 10, units="us")  # Create a 10us period clock on port clk
#     cocotb.start_soon(clock.start())  # Start the clock

#     A = 0b0010101010101010
#     B = 0b0101010101010101
#     AB = A * B

#     # Initialize Inputs
#     dut.Rst.value = 1
#     dut.Clk.value = 1
#     dut.Ld.value  = 0
#     dut.M.value   = 0
#     dut.R.value   = 0

#     # Wait 100 ns for global reset to finish
#     await Timer(100, units='ns')

#     # Release global reset
#     dut.Rst.value = 0

#     # Load values
#     await RisingEdge(dut.Clk)
#     await Timer(1, units='ns')
#     dut.Ld.value  = 1
#     dut.M.value   = A
#     dut.R.value   = B

#     # End load
#     await RisingEdge(dut.Clk)
#     await Timer(1, units='ns')
#     dut.Ld.value  = 0

#     # Wait for valid output
#     await RisingEdge(dut.Valid)
#     await Timer(1, units='ns')

#     # Check output
#     assert dut.P.value.integer == AB, "Full multiplication failed"

@cocotb.test()
async def boothmul_example_large_bit(dut):
    """ Test booth multiplication """

    if dut.N.value <= 16:
        return

    clock = Clock(dut.Clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    A = random.randint(0, 2**(dut.N.value-1))
    B = random.randint(0, 2**(dut.N.value-1))
    AB = A * B

    # Initialize Inputs
    dut.Rst.value = 1
    dut.Clk.value = 1
    dut.Ld.value  = 0
    dut.M.value   = 0
    dut.R.value   = 0

    # Wait 100 ns for global reset to finish
    await Timer(100, units='ns')

    # Release global reset
    dut.Rst.value = 0

    # Load values
    await RisingEdge(dut.Clk)
    await Timer(1, units='ns')
    dut.Ld.value  = 1
    dut.M.value   = A
    dut.R.value   = B

    # End load
    await RisingEdge(dut.Clk)
    await Timer(1, units='ns')
    dut.Ld.value  = 0

    # Wait for valid output
    await RisingEdge(dut.Valid)
    await Timer(1, units='ns')

    # await Timer(10000, units='ms')

    # Check output
    assert dut.P.value.integer == AB, "Full multiplication failed"

# @cocotb.test()
# async def boothmul_random(dut):
#     """ Test booth multiplication """

#     if dut.N.value != 16:
#         return

#     clock = Clock(dut.Clk, 10, units="us")  # Create a 10us period clock on port clk
#     cocotb.start_soon(clock.start())  # Start the clock

#     for _ in range(100):

#         A = random.randint(0, 2**(dut.N.value-1))
#         B = random.randint(0, 2**(dut.N.value-1))
#         AB = A * B

#         # Initialize Inputs
#         dut.Rst.value = 1
#         dut.Clk.value = 1
#         dut.Ld.value  = 0
#         dut.M.value   = 0
#         dut.R.value   = 0

#         # Wait 100 ns for global reset to finish
#         await Timer(100, units='ns')

#         # Release global reset
#         dut.Rst.value = 0

#         # Load values
#         await RisingEdge(dut.Clk)
#         await Timer(1, units='ns')
#         dut.Ld.value  = 1
#         dut.M.value   = A
#         dut.R.value   = B

#         # End load
#         await RisingEdge(dut.Clk)
#         await Timer(1, units='ns')
#         dut.Ld.value  = 0

#         # Wait for valid output
#         await RisingEdge(dut.Valid)
#         await Timer(1, units='ns')

#         # Check output
#         assert dut.P.value.integer == AB, "Full multiplication failed"

# Check WAVES environment variable
@pytest.mark.parametrize(
    "parameters", [
        # {"N": "16"},
        {"N": "31"} # This does not work for N=32
    ]
)
def test_boothmul_testcase(parameters):
    print("hello", os.getenv("WAVES"))

    run(
        verilog_sources=[
            # os.path.join("..", "..", "src", "BoothMul", "Booth_Multiplier.v"),
            os.path.join("..", "..", "src", "BoothMul", "Booth_Multiplier_1xA.v")
        ],
        parameters=parameters,
        extra_env=parameters,
        toplevel="Booth_Multiplier_1xA",
        module="test_boothmul",
        sim_build="sim_build/"
        + "_".join(("{}={}".format(*i) for i in parameters.items()))
    )
