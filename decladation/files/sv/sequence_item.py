#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class sequence_item:
    """
        This class generates systemVerilog sequence_item file
    """

    def __init__(self, pkg_name, items, convert2string):
        self.pkg_name = pkg_name
        self.items = items
        self.convert2string = convert2string
        self.name  = "sequence_item"
    
    def name_get(self):
        return self.name

    def generate(self, file, generic, preambule_inf):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule("sequence_item.sv", preambule_inf), file = file)
        print (f"class sequence_item{generic_decl} extends uvm_common::sequence_item;", file = file) 
        print (f"\t`uvm_object_param_utils(uvm_{self.pkg_name}::sequence_item{generic_assign})\n", file = file)
        print (f"", file = file)
        for item in self.items:
            print (f"\trand {item[0]} {item[1]} {item[2]};", file = file)
        print (f"", file = file)
        print (f"\tfunction new(string name = \"uvm_{self.pkg_name}::sequence_item\");", file = file)
        print (f"\t\tsuper.new(name);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void do_copy(uvm_object rhs);", file = file)
        print (f"\t\tsequence_item{generic_assign} c_rhs;", file = file)
        print (f"", file = file)
        print (f"\t\tassert($cast(c_rhs, rhs));", file = file)
        print (f"\t\tsuper.do_copy(rhs);", file = file)
        for item in self.items:
            print (f"\t\t{item[1]} = c_rhs.{item[1]};", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction bit do_compare(uvm_object rhs,uvm_comparer comparer);", file = file)
        print (f"\t\tbit ret;", file = file)
        print (f"\t\tsequence_item{generic_assign} c_rhs;", file = file);
        print (f"", file = file)
        print (f"\t\tassert($cast(c_rhs, rhs));", file = file)
        print (f"\t\tret = super.do_compare(rhs, comparer);", file = file)
        for item in self.items:
            print (f"\t\tret &= ({item[1]} === c_rhs.{item[1]});", file = file)
        print (f"\t\treturn ret;", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction string convert2string();", file = file)
        print (f"\t\tstring ret = \"\";", file = file)
        print (f"\t\tret = this.time2string();", file = file)
        print (f"\t\t{self.convert2string}", file = file)
        print (f"\t\treturn ret;", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)
       


