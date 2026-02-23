import cocotb
import os
from pathlib import Path

from cocotb_tools.runner import get_runner
from cocotb.triggers import Timer
from random import randint

@cocotb.test()
async def test_add(dut):
    """Test Add"""

    # Test 0 + 0
    dut.op.value = 0
    dut.a.value = 0x00000000
    dut.b.value = 0x00000000

    await Timer(1, unit="ns")

    assert dut.result.value == 0, f"Expected 0, got {dut.result.value}"

    # Test max input + max input
    await Timer(1, unit="ns")

    dut.a.value = 0xFFFFFFFF
    dut.b.value = 0xFFFFFFFF

    await Timer(1, unit="ns")

    assert int(dut.result.value) == int(0x1FFFFFFE), f"Expected 4294967294, got {int(dut.result.value)}"

    await Timer(1, unit="ns")

    # Test random numbers
    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

        dut.a.value = a
        dut.b.value = b

        await Timer(1, unit="ns")

        exp_result = (a + b) & 0xFFFFFFFF
        act_result = dut.result.value

        assert int(exp_result) == int(act_result), f"Expected {exp_result}, got {act_result}"






def alu_test_runner():
    sim = os.getenv("SIM", "verilator")
    os.environ["CXXFLAGS"] = "-std=c++14"
    proj_path = Path(__file__).resolve().parent.parent
    sources = [
        proj_path / "rtl" / "types.sv",
        proj_path / "rtl" / "alu.sv"
    ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="alu",
        always=True
    )

    runner.test(hdl_toplevel="alu", test_module="test_alu")

if __name__ == "__main__":
    alu_test_runner()