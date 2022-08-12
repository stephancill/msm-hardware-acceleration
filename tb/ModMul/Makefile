# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

# Makefile

SRC = $(PWD)

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/../../src/ModMul/ModMul.v
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = ModMul

# MODULE is the basename of the Python test file
MODULE = test_modmul
COCOTB_CONFIG = $(shell cocotb-config --makefiles)

# include cocotb's make rules to take care of the simulator setup
include $(COCOTB_CONFIG)/Makefile.sim