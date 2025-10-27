#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class testbench:
    """
        This class generates systemVerilog testbench file
    """

    def __init__(self, dut):
        self.name = "testbench"
        self.dut  = dut

    def name_get(self):
        return self.name


    def generate(self, file, blocks, generic):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = "tetbench.sv"), file = file)
        print (f"", file = file)
        print (f"import uvm_pkg::*;", file = file)
        print (f"`include \"uvm_macros.svh\"", file = file)
        print (f"import generic_pkg::*;", file = file)
        print (f"", file = file)
        print (f"module testbench;", file = file)
        print (f"", file = file)
        print (f"\ttypedef test::base{generic_assign} base;", file = file)
        print (f"", file = file)
        print (f"\t//generate clock", file = file)
        print (f"\tlogic CLK = 1'b1;", file = file)
        print (f"\talways #(CLK_PERIOD) CLK = ~CLK;", file = file)
        print (f"", file = file)
        print (f"\t//generat interface", file = file)
        #self.block
        for block in blocks:
            f_string = "\t{prefix}{inf_type} inf{inf_name} {array} (CLK);"
            for inf in block.interfaces2inst({}, f_string, "", "", "CLK"):
                print (f"{inf}", file = file)

        #print("", file = file)
        print("\tinitial begin", file = file)
        for block in blocks:
            f_string = "\t\t{prefix}automatic virtual {inf_type} vif{inf_name} {array} = inf{inf_name};"
            for inf in block.interfaces2inst({}, f_string, "", "", "CLK"):
                print (f"{inf}", file = file)
        print("", file = file)

        for block in blocks:
            f_string = "{prefix}uvm_config_db#(virtual {inf_type})::set(null, \"\", {{\"vif\" {reg_name} }}, vif{inf_name}{array});\n"
            inf = block.interfaces2cmd({}, f_string, "\t\t", "", "", "")
            print (f"{inf}", file = file)
        print("\tend\n", file = file)
        print (f"", file = file)
        dut = self.dut.inst2string("!!!")
        print (f"", file = file)
        print (f"{dut}", file = file)
        print (f"", file = file)
        print (f"\tinitial begin", file = file)
        print (f"\t\tuvm_root m_root;", file = file)
        print (f"\t\t//add interfaces", file = file)
        print (f"", file = file)
        print (f"\t\tm_root = uvm_root::get();", file = file)
        print (f"\t\tm_root.finish_on_completion = 0;", file = file)
        print (f"\t\tm_root.set_report_id_action_hier(\"ILLEGALNAME\", UVM_NO_ACTION);", file = file)
        print (f"", file = file)
        print (f"\t\tuvm_config_db #(int)            ::set(null, \"\", \"recording_detail\", 0);", file = file)
        print (f"\t\tuvm_config_db #(uvm_bitstream_t)::set(null, \"\", \"recording_detail\", 0);", file = file)
        print (f"", file = file)
        print (f"\t\trun_test();", file = file)
        print (f"\t\t$stop(2);", file = file)
        print (f"\tend", file = file)
        print (f"endmodule", file = file)


