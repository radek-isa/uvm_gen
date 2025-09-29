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
    def __init__(self, prefix = 0):
        self.prefix     = prefix;
        self.array_decl = ""

    

