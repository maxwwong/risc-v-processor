import cocotb
import os
from pathlib import Path

from cocotb_tools.runner import get_runner
from cocotb.triggers import Timer
from random import randint

@cocotb.test()
async def test_add(dut):
    async def run_add_test(a,b):
        dut.a.value = a
        dut.b.value = b
        expected_result = (a+b) & 0xFFFFFFFF

        await Timer(1, unit="ns")

        result = dut.result.value

        assert result == expected_result, f"Expected {expected_result}. Received {result}"


    # Test 0 + 0
    await run_add_test(0, 0)

    # Test max input + max input
    
    await run_add_test(0xFFFFFFFF, 0xFFFFFFFF)

    await Timer(1, unit="ns")

    # Test random numbers
    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

        await run_add_test(a, b)

@cocotb.test()
async def test_sub(dut):
    async def run_sub_test(a, b):
        dut.a.value = a
        dut.b.value = b
        expected_result = (a-b) & 0xFFFFFFFF

        await Timer(1, unit="ns")

        result = dut.result.value

        assert result == expected_result, f"Expected {expected_result}. Received {result}"
    
    dut.op.value = 1

    # Test 0 - 0

    await run_sub_test(0, 0)

    # Test max_input - max_input

    await run_sub_test(0xFFFFFFFF, 0xFFFFFFFF)

    # Test 0 - max_input 

    await run_sub_test(0, 0xFFFFFFFF)

    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

        await run_sub_test(a, b)




@cocotb.test()
async def test_and(dut):
    pass

@cocotb.test()
async def test_or(dut):
    pass

@cocotb.test()
async def test_xor(dut):
    pass

@cocotb.test()
async def test_sll(dut):
    pass

@cocotb.test()
async def test_sra(dut):
    pass

@cocotb.test()
async def test_srl(dut):
    pass

@cocotb.test()
async def test_slt(dut):
    pass

@cocotb.test()
async def test_sltu(dut):
    pass



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