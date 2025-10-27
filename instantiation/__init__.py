#!/bin/python3

from .constant               import *
from .logic_vector_array_mfb import uvm_logic_vector_array_mfb
from .logic_vector_mvb       import uvm_logic_vector_mvb
from .reset                  import uvm_reset
from .env                    import uvm_env
from .dut                    import uvm_dut

from .block_for              import block_for

"""
Tento modul obsahuje vytváření instancí pro prostředí
"""

class lambda_param:
    def __init__(self, prefix = 0, direction = False):
        self.direction = direction
        self.prefix    = prefix
        #two items, (ITERATOR, END_OF_ITERATION)
        self.array  = []

    def print_prefix(self, inc = 0):
        ret = "";
        for it in range(0, self.prefix + inc):
            ret += "\t"
        return ret


    def print_for_start(self):
        ret = ""
        for it in self.array:
            ret += "".join(["\t" for x in range (0, self.prefix)])
            self.prefix += 1
            ret += f"for (int unsigned {it[0]} = 0; {it[0]} < {it[1]}; {it[0]}++) begin\n"
        return ret

    def print_for_end(self):
        ret = ""
        for it in self.array:
            self.prefix -= 1
            ret += "".join(["\t" for x in range (0, self.prefix)])
            ret += f"end\n"
        return ret


