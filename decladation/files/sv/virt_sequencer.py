#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class virt_sequencer:
    """
        This class generates systemVerilog sequencer file
    """

    def __init__(self):
        self.name = "sequencer"

    def name_get(self):
        return self.name

    @staticmethod
    def gen_seqr_decl(obj, lambda_param):
        ret = ""

        if (obj.sequence2string(False) != None):
            prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
            array  = "".join([f"[{x[1]}]" for x in lambda_param.array])

            ret += f"{prefix}{obj.pkg2string()}::sequencer{obj.generic2string()} {obj.name}{array};\n"
        return ret

    def generate(self, file, blocks, generic, preambule_inf):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule("sequencer.sv", preambule_inf), file = file)
        print (f"class sequencer{generic_decl} extends uvm_sequencer;", file = file)
        print (f"\t`uvm_component_param_utils(uvm_env_top::sequencer{generic_assign})", file = file)
        print (f"", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(1);
            lambda_gen = [virt_sequencer.gen_seqr_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.build_phase(phase);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)


