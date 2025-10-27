#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class config:
    """
        This class generates systemVerilog config file
    """

    def __init__(self, pkg_name, cfg = {}):
        self.name = "config"
        self.pkg_name = pkg_name
        self.config  = cfg
    
    def name_get(self):
        return self.name

    def generate(self, file, blocks, generic):
        #(generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = "config.sv"), file = file)
        print (f"class config_sequence extends uvm_object;", file = file)
        print (f"\t`uvm_object_utils(uvm_{self.pkg_name}::config_sequence)", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name = \"uvm_{self.pkg_name}::config_sequence\");", file = file)
        print (f"\t\tsuper.new(name);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)
        print (f"", file = file)
        print (f"", file = file)
        print (f"class config_item extends uvm_object;", file = file)
        print (f"\t`uvm_object_utils(uvm_{self.pkg_name}::config_item)", file = file)
        print (f"\tstring interface_name;", file = file)
        for cfg in self.config:
            print (f"\t{self.config[cfg]} {cfg};", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name = \"\");\n\t\tsuper.new(name);", file = file)
        print (f"\t\tinterface_name = \"vif\";", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)

