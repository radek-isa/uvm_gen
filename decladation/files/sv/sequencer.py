#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class sequencer:
    """
        This class generates systemVerilog sequencer file
    """

    def __init__(self, pkg_name):
        self.pkg_name = pkg_name
        self.name = "sequencer"
    
    def name_get(self):
        return self.name

    def generate(self, file, generic):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = "sequencer.sv"), file = file)
        print (f"class sequencer{generic_decl} extends uvm_sequencer#(sequence_item{generic_assign});", file = file)
        print (f"\t`uvm_component_param_utils(uvm_{self.pkg_name}::sequencer{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tuvm_reset::sync_terminate reset_sync;", file = file);
        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.build_phase(phase);", file = file)
        print (f"\t\treset_sync = new();", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)

