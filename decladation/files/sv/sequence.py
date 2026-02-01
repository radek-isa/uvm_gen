#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class sequence:
    """
        This class generates systemVerilog sequencer file
    """

    def __init__(self, pkg_name):
        self.pkg_name = pkg_name
        self.name = "sequence"
    
    def name_get(self):
        return self.name

    def generate(self, file, generic, preambule_inf):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule("sequence.sv", preambule_inf), file = file)
        print (f"class sequence_base{generic_decl} extends uvm_common::sequence_base#(config_sequence, sequence_item{generic_assign});", file = file)
        print (f"\t`uvm_object_param_utils(uvm_{self.pkg_name}::sequence_base{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tint unsigned transaction_count_min = 10;", file = file)
        print (f"\tint unsigned transaction_count_max = 200;", file = file)
        print (f"\trand int unsigned transaction_count;", file = file)
        print ("\tconstraint c1 {transaction_count inside {[transaction_count_min : transaction_count_max]};}", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name = \"{self.pkg_name}::{self.name}\");\n\t\tsuper.new(name);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\ttask body ();", file = file)
        print (f"\t\tint unsigned it;", file = file)
        print (f"\t\tuvm_common::sequence_cfg state;", file = file)
        print (f"", file = file)
        print (f"\t\tif(!uvm_config_db#(uvm_common::sequence_cfg)::get(m_sequencer, \"\", \"state\", state)) begin", file = file)
        print (f"\t\t\tstate = null;", file = file)
        print (f"\t\tend", file = file)
        print (f"", file = file)
        print (f"\t\t`uvm_info(m_sequencer.get_full_name(), \"\\n\\tsequence_simple is running\", UVM_DEBUG);", file = file)
        print (f"", file = file)
        print (f"\t\tit = 0;", file = file)
        print (f"\t\twhile(it < transaction_count && (state == null || state.next())) begin", file = file)
        print (f"\t\t\treq = sequence_item{generic_assign}::type_id::create(\"req\", m_sequencer);", file = file)
        print (f"\t\t\tstart_item(req);", file = file)
        print (f"\t\t\tassert(req.randomize());", file = file)
        print (f"\t\t\tfinish_item(req);", file = file)
        print (f"\t\tend", file = file);
        print (f"\tendtask", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)
        print (f"", file = file)
        print (f"", file = file)
        print (f"/////////////////////////////////////////////////////////////////////////", file = file)
        print (f"// SEQUENCE LIBRARY", file = file)
        print (f"class sequence_lib{generic_decl}  extends uvm_common::sequence_library#(config_sequence, sequence_item{generic_assign});", file = file)
        print (f"\t`uvm_object_param_utils(uvm_{self.pkg_name}::sequence_lib{generic_assign})", file = file)
        print (f"\t`uvm_sequence_library_utils(uvm_{self.pkg_name}::sequence_lib{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name = \"{self.pkg_name}::{self.name}_lib\");\n\t\tsuper.new(name);", file = file)
        print (f"\t\tinit_sequence_library();", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tvirtual function void init_sequence(config_sequence param_cfg = null);", file = file)
        print (f"\t\tuvm_common::sequence_library::init_sequence(param_cfg);", file = file)
        print (f"\t\tthis.add_sequence(sequence_base{generic_assign}::get_type());", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)


