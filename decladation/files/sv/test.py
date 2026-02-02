#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class test:
    """
        This class generates systemVerilog config file
    """

    def __init__(self, name):
        self.name = name
    
    def name_get(self):
        return self.name

    def generate(self, file, blocks, generic, preambule_inf):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule("base.sv", preambule_inf), file = file)
        print (f"class {self.name}{generic_decl} extends uvm_test;", file = file)
        print (f"\ttypedef uvm_component_registry #(test::base{generic_assign}, \"test::{self.name}\") type_id;", file = file)
        print (f"//change to something more generic.", file = file)
        print (f"", file = file)
        print (f"\tuvm_env_top::env_top{generic_assign} m_env;", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tstatic function type_id get_type();", file = file)
        print (f"\t\treturn type_id::get();", file = file)
        print (f"\tendfunction", file = file)
        print (f"\tfunction string get_type_name();", file = file)
        print (f"\t\treturn get_type().get_type_name();", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void build_phase (uvm_phase phase);\n\t\tsuper.build_phase(phase);", file = file)
        print (f"\t\tm_env = uvm_env_top::env_top{generic_assign}::type_id::create(\"m_env\", this);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\ttask run_phase (uvm_phase phase);", file = file)
        print (f"\t\tuvm_env_top::sequence_base{generic_assign} seq;", file = file)
        print (f"\t\ttime time_start;", file = file)
        print (f"", file = file)
        print (f"\t\tseq = uvm_env_top::sequence_base{generic_assign}::type_id::create(\"seq\", m_env.m_sequencer);", file = file)
        print (f"\t\tphase.raise_objection(this);", file = file)
        print (f"", file = file)
        print (f"\t\t//RUN SEQUENCES", file = file)
        print (f"", file = file)
        print ("\t\tassert(seq.randomize()) else `uvm_fatal(this.get_full_name(), \"\\t\\nCannot randomize sequence\")", file = file)
        print ("\t\t//seq.start(m_env.m_sequencer)", file = file)
        print (f"", file = file)
        print (f"\t\t//WAIT FOR REST OF OUTPUT TRANSACTIONS", file = file)
        print (f"\t\ttime_start = $time;", file = file)
        print (f"\t\twhile(m_env.used() != 0 && (time_start + 500us) > $time) begin", file = file)
        print (f"\t\t\t#(300ns);", file = file)
        print (f"\t\tend", file = file)
        print (f"\t\tphase.drop_objection(this);", file = file)
        print (f"\tendtask", file = file)
        print (f"", file = file)
        print (f"\tfunction void report_phase(uvm_phase phase);", file = file)
        print ("\t\tstring msg = \"\";", file = file)
        print ("\t\tmsg = {\"\\n\\tTEST : \", this.get_type_name()};", file = file)
        print (f"", file = file)
        print ("\t\tmsg = {msg, $sformatf(\"\\n\\tSuccess %0d Used %0d\", m_env.success(), m_env.used())};", file = file)
        print (f"\t\tif (m_env.success() == 1 && m_env.used() == 0) begin", file = file)
        print ("\t\t\t`uvm_info(this.get_full_name(), {msg, \"\\n\\n\\t---------------------------------------\\n\\t----     VERIFICATION SUCCESS       ----\\n\\t---------------------------------------\"}, UVM_NONE);", file = file)
        print (f"\t\tend else begin", file = file)
        print ("\t\t\t`uvm_info(this.get_full_name(), {msg, \"\\n\\n\\t---------------------------------------\\n\\t----     VERIFICATION FAILED        ----\\n\\t---------------------------------------\"}, UVM_NONE);", file = file)
        print (f"\t\tend", file = file)
        print (f"\tendfunction", file = file)
        print (f"endclass", file = file)

