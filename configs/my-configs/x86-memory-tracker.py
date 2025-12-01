# Copyright (c) 2024 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
TODO: DESCRIBE

"""

import time

import m5

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR4_2400

# from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource

# from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator

# from m5.objects import (
#     GlobalInstTracker,
#     LocalInstTracker,
# )


# from gem5.coherence_protocol import CoherenceProtocol
# from gem5.utils.requires import requires

# from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
#     MESITwoLevelCacheHierarchy,
# )

# requires(
#     isa_required=ISA.X86,
#     coherence_protocol_required=CoherenceProtocol.MESI_TWO_LEVEL,
# )

# no caching needed in atomic mode
cache_hierarchy = NoCache()

# cache_hierarchy = MESITwoLevelCacheHierarchy(
#     l1d_size="32KiB",
#     l1d_assoc=8,
#     l1i_size="32KiB",
#     l1i_assoc=8,
#     l2_size="256KiB",
#     l2_assoc=16,
#     num_l2_banks=2,
# )


memory = SingleChannelDDR4_2400("16GiB")
# memory = DualChannelDDR4_2400()

# should be # cores + 1
processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=2, isa=ISA.X86)


board = SimpleBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(
    #     binary = obtain_resource(resource_id="x86-hello64-static")
    # A simple X86 binary that prints a string a set number of times. It takes two mandatory arguments: A string to print and an integer specifying how many times the string is to be printed.
    binary=obtain_resource(resource_id="x86-print-this"),
    arguments=["print this", 100],
    # A simple binary which runs a matrix mutiply operation on two 100x100 matrixes. After multiplication it will return the print the of the multiplication.
    # binary = obtain_resource(resource_id="x86-matrix-multiply")
    #     binary = obtain_resource(resource_id="x86-bubblesort")
    # A binary that runs the llvm minisat benchmark in SE mode.
    #   binary = obtain_resource("x86-llvm-minisat")
)


simulator = Simulator(
    board=board,
)

# We maintain the wall clock time.

globalStart = time.time()

print("Running the simulation")

m5.stats.reset()

# We start the simulation
simulator.run()

print("All simulation events were successful.")

# We print the final simulation statistics.

print("Done with the simulation")
print()
# print("Performance statistics:")

# print("Simulated time in ROI: " + ((str(simulator.get_roi_ticks()[0]))))
# print(
#     "Ran a total of", simulator.get_current_tick() / 1e12, "simulated seconds"
# )
print(
    "Total wallclock time: %.2fs, %.2f min"
    % (time.time() - globalStart, (time.time() - globalStart) / 60)
)
