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

    result = int(dut.result.value)

    assert result == expected_result, f"Expected {expected_result}. Received {result}"

def to_signed(val):
    return val if val < 2**31 else val - 2**32

def sra(a, b):
    return (to_signed(a) >> (b & 0x1F)) & 0xFFFFFFFF

@cocotb.test()
async def test_add(dut):
    dut.op.value = 0

    await test_op(dut, 0, 0, lambda x, y: (x + y) & 0xFFFFFFFF)

    await test_op(dut, 0xFFFFFFFF, 0xFFFFFFFF, lambda x, y: (x + y) & 0xFFFFFFFF)

    await test_op(dut, 0xFFFFFFFF, 1, lambda x, y: (x + y) & 0xFFFFFFFF)

    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)
        await test_op(dut, a, b, lambda x, y: (x + y) & 0xFFFFFFFF)

@cocotb.test()
async def test_sub(dut):
    dut.op.value = 1

    await test_op(dut, 0, 0, lambda x, y: (x - y) & 0xFFFFFFFF)

    await test_op(dut, 0xFFFFFFFF, 0xFFFFFFFF, lambda x, y: (x - y) & 0xFFFFFFFF)

    await test_op(dut, 0, 0xFFFFFFFF, lambda x, y: (x - y) & 0xFFFFFFFF)

    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)
        await test_op(dut, a, b, lambda x, y: (x - y) & 0xFFFFFFFF)

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
        await test_op(dut, a, b, lambda x, y: x | y)

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
        await test_op(dut, a, b, lambda x, y: (x << (y & 0x1F)) & 0xFFFFFFFF)

@cocotb.test()
async def test_srl(dut):
    dut.op.value = 6
    await test_op(dut, 0x80000000, 1, lambda x, y: (x >> (y & 0x1F)) & 0xFFFFFFFF)
    await test_op(dut, 0xFFFFFFFF, 31, lambda x, y: (x >> (y & 0x1F)) & 0xFFFFFFFF)
    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)
        await test_op(dut, a, b, lambda x, y: (x >> (y & 0x1F)) & 0xFFFFFFFF)

@cocotb.test()
async def test_sra(dut):
    dut.op.value = 7
    await test_op(dut, 0x80000000, 1, lambda x, y: sra(x, y))
    await test_op(dut, 0x80000000, 31, lambda x, y: sra(x, y))
    await test_op(dut, 0x7FFFFFFF, 1, lambda x, y: sra(x, y))
    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)
        await test_op(dut, a, b, lambda x, y: sra(x, y))

@cocotb.test()
async def test_slt(dut):
    dut.op.value = 8
    await test_op(dut, 0xFFFFFFFF, 0, lambda x, y: 1 if to_signed(x) < to_signed(y) else 0)
    await test_op(dut, 0, 0xFFFFFFFF, lambda x, y: 1 if to_signed(x) < to_signed(y) else 0)
    await test_op(dut, 0, 0, lambda x, y: 1 if to_signed(x) < to_signed(y) else 0)
    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)
        await test_op(dut, a, b, lambda x, y: 1 if to_signed(x) < to_signed(y) else 0)

@cocotb.test()
async def test_sltu(dut):
    dut.op.value = 9
    await test_op(dut, 0, 0xFFFFFFFF, lambda x, y: 1 if x < y else 0)
    await test_op(dut, 0xFFFFFFFF, 0, lambda x, y: 1 if x < y else 0)
    await test_op(dut, 0, 0, lambda x, y: 1 if x < y else 0)
    for _ in range(10000):
        a = randint(0, 2**32-1)
        b = randint(0, 2**32-1)
        await test_op(dut, a, b, lambda x, y: 1 if x < y else 0)

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