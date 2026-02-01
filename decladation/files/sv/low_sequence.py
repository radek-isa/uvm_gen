#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class low_sequence:

    """
        This class generates systemVerilog low sequence file
    """
    def __init__(self, pkg_name, agent):
        self.pkg_name = pkg_name
        self.agent    = agent
        self.name     = f"{agent.name}_low_sequence"

    def name_get(self):
        return self.name

    def generate(self, file, generic, preambule_inf):
        (generic_decl, generic_assign) = generic

        agent_seq_item = self.agent.item2string("");
        print (uvm_gen_preambule(self.name + ".sv", preambule_inf), file = file)
        print (f"class {self.agent.name}_config_sequence extends uvm_object;", file = file)
        print (f"\t`uvm_object_utils(uvm_{self.pkg_name}::{self.agent.name}_config_sequence)", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name = \"uvm_{self.pkg_name}::config_sequence\");", file = file)
        print (f"\t\tsuper.new(name);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)

        print (f"", file = file)
        print (f"class {self.agent.name}_low_sequence {generic_decl} extends uvm_common::sequence_base#({self.agent.name}_config_sequence, {agent_seq_item});", file = file)
        print (f"\t`uvm_object_param_utils(uvm_{self.pkg_name}::{self.agent.name}_low_sequence{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\trand int unsigned transaction_count;", file = file)
        print (f"\t//thing about constraints", file = file)
        print ("\tconstraint c_transactions {\n\t\ttransaction_count inside {[50:200]};\n\t};", file = file)
        print (f"", file = file)
        print (f"\tfunction new(string name = \"{self.agent.name}_low_sequence\");", file = file)
        print (f"\t\tsuper.new(name);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\ttask body();", file = file)
        print (f"\t\tint unsigned it;", file = file)
        print (f"\t\tuvm_common::fifo#({agent_seq_item}) fifo;", file = file)
        print (f"\t\tassert(uvm_config_db#(uvm_common::fifo#({agent_seq_item}))::get(m_sequencer , \"\" , \"fifo\",  fifo));", file = file)
        print (f"", file = file)
        print (f"\t\tit = 0;", file = file)
        print (f"\t\t// Somewhere get sequence item and parse it", file = file)
        print (f"\t\twhile (it < transaction_count) begin", file = file)
        print (f"\t\t\tfifo.get(req);", file = file)
        print (f"\t\t\tstart_item(req);", file = file)
        print (f"\t\t\t//`uvm_fatal(m_sequencer.get_full_name, \"\\n\\tYou have to implement conversion function!!\")", file = file)
        print (f"\t\t\t//assert(req.randomize()) with {{}};", file = file)
        print (f"\t\t\tfinish_item(req);", file = file)
        print (f"\t\t\tit++;", file = file)
        print (f"\t\tend", file = file)
        print (f"", file = file)
        print (f"\tendtask", file = file)
        print (f"endclass", file = file)

        # Create sequence library library
        print (f"", file = file)
        print (f"", file = file)
        print (f"class {self.agent.name}_low_sequence_lib {generic_decl} extends uvm_common::sequence_library#({self.agent.name}_config_sequence , {agent_seq_item});", file = file)
        print (f"\t`uvm_object_param_utils     (uvm_{self.pkg_name}::{self.agent.name}_low_sequence_lib{generic_assign})", file = file)
        print (f"\t`uvm_sequence_library_utils(uvm_{self.pkg_name}::{self.agent.name}_low_sequence_lib{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tfunction new(string name = \"uvm_{self.pkg_name}::{self.agent.name}_low_sequence_lib\");", file = file)
        print (f"\t\tsuper.new(name);", file = file)
        print (f"\t\tthis.add_sequence({self.agent.name}_low_sequence {generic_assign}::get_type());", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tvirtual function void init_sequence({self.agent.name}_config_sequence param_cfg = null);", file = file)
        print (f"\t\tuvm_common::sequence_library::init_sequence(param_cfg);", file = file)
        print (f"\tendfunction", file = file)
        print (f"endclass", file = file)


