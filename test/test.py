# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    #test for ui_in + uin_in:
    # dut.ui_in.value = 20
    # dut.uio_in.value = 30
    # Wait for one clock cycle to see the output values
    # await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    # assert dut.uo_out.value == 50

    load_value = 0x32
    dut.uio_in.value = load_value
    dut.ui_in.value = 0b11 #load enable
    await ClockCycles(dut.clk, 1)
    for _ in range(3):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == load_value, "Failed to load value"
    
    dut.ui_in.value = 0b00 #disable load
    expected = load_value
    for _ in range(4):
        await ClockCycles(dut.clk, 1)
        expected = (expected + 1) & 0xFF
        assert all(bit == "z" for bit in dut.uo_out.value.binstr.lower()), "Output not high impedance"

    dut.ui_in.value = 0b10  # enable count
    for i in range(5):
        await ClockCycles(dut.clk, 1)
        actual = int(dut.uo_out.value)
        assert actual == expected, f"Counter wrong! Expected {expected}, got {actual}"
        expected = (expected + 1) & 0xFF
        

    
    dut._log.info("Counter test passed!")

   

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
