import cocotb
import os
from pathlib import Path

from cocotb_tools.runner import get_runner
from cocotb.triggers import Timer
from random import randint

async def test_op(dut, a, b, op_func):
    dut.a.value = a
    dut.b.value = b
    expected_result = op_func(a, b)

    await Timer(1, unit="ns")

    result = dut.result.value

    assert result == expected_result, f"Expected {expected_result}. Received {result}"

@cocotb.test()
async def test_add(dut):
    dut.op.value = 0

    # Test 0 + 0
    await test_op(dut, 0, 0, lambda x, y: (x + y) & 0xFFFFFFFF)

    # Test max input + max input
    
    await test_op(dut, 0xFFFFFFFF, 0xFFFFFFFF, lambda x, y: (x + y) & 0xFFFFFFFF)

    await Timer(1, unit="ns")

    # Test random numbers
    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

        await test_op(dut, a, b, lambda x, y: (x + y) & 0xFFFFFFFF)

@cocotb.test()
async def test_sub(dut):    
    dut.op.value = 1

    # Test 0 - 0

    await test_op(dut, 0, 0, lambda x, y: (x - y) & 0xFFFFFFFF)

    # Test max_input - max_input

    await test_op(dut, 0xFFFFFFFF, 0xFFFFFFFF, lambda x, y: (x - y) & 0xFFFFFFFF)

    # Test 0 - max_input 

    await test_op(dut, 0, 0xFFFFFFFF, lambda x, y: (x - y) & 0xFFFFFFFF)

    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

        await test_op(dut, 0, 0, lambda x, y: (x - y) & 0xFFFFFFFF)




@cocotb.test()
async def test_and(dut):
    dut.op.value = 2

    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

        await test_op(dut, a, b, lambda x, y: x & y)

@cocotb.test()
async def test_or(dut):
    dut.op.value = 3


    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

        await test_op(dut, a, b, lambda x, y: (x | y))

@cocotb.test()
async def test_xor(dut):
    dut.op.value = 4
    
    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

        await test_op(dut, a, b, lambda x, y: x ^ y)

@cocotb.test()
async def test_sll(dut):
    dut.op.value = 5

    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)

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