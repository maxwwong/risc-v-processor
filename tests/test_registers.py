import cocotb
import os
from pathlib import Path
from cocotb_tools.runner import get_runner
from cocotb.triggers import Timer, ClockCycles, RisingEdge, FallingEdge, ReadOnly, with_timeout
from cocotb.clock import Clock
from random import randint

@cocotb.test()
async def test_register_file(dut):
    """
    Basic functionality test:
    x0 reads 0
    Write and read correctly from each register
    Reset works
    """

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    await ClockCycles(dut.clk, 1)
    dut.rst.value = 1
    await ClockCycles(dut.clk, 1)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 1)

    reg_tracker = [0] * 32

    for i in range (32):
        random_num = randint(2, 100)

        dut.write_en.value = 1
        dut.write_data.value = random_num
        dut.write_addr.value = i
        reg_tracker[i] = random_num

        await ClockCycles(dut.clk, 1)

    dut.write_en.value = 0
    await ClockCycles(dut.clk, 1)

    # update zero register back to zero for comparison
    reg_tracker[0] = 0

    for i in range(31):
        dut.rs1_addr.value = i
        dut.rs2_addr.value = i + 1

        await ClockCycles(dut.clk, 1)

        assert dut.rs1_data.value == reg_tracker[i], "Incorrect value on register 1"
        assert dut.rs2_data.value == reg_tracker[i+1], "Incorrect value on reigster 2"

        await ClockCycles(dut.clk, 1)

    dut.rst.value = 1
    await ClockCycles(dut.clk, 1)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 1)

    for i in range (31):
        dut.rs1_addr.value = i
        dut.rs2_addr.value = i + 1

        await ClockCycles(dut.clk, 1)

        assert dut.rs1_data.value == 0, "Incorrect value on register 1"
        assert dut.rs2_data.value == 0, "Incorrect value on reigster 2"

        await ClockCycles(dut.clk, 1)




def register_file_test_runner():
    sim = os.getenv("SIM", "verilator")
    os.environ["CXXFLAGS"] = "-std=c++14"
    proj_path = Path(__file__).resolve().parent.parent
    sources = [
        proj_path / "rtl" / "register_file.sv"
    ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="register_file",
        always=True
    )

    runner.test(hdl_toplevel="register_file", test_module="test_registers")

if __name__ == "__main__":
    register_file_test_runner()