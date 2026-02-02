#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class pkg:
    """
        This class generates systemVerilog testbench file
    """

    def __init__(self, name):
        self.name = name 
        self.parameters = {}
        self.files      = []

    def add_parameter(self, name, value, p_type = None):
        self.parameters[name] = (p_type if p_type != None else  "     ", value) 

    def add_file(self, name):
        self.files.append(name)

    def name_get(self):
        return self.name


    def generate(self, file, blocks, generic, preambule_inf):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule(f"{self.name}.sv", preambule_inf), file = file)
        print (f"package {self.name};", file = file)
        print (f"", file = file);
        print (f"\timport uvm_pkg::*;", file = file)
        print (f"\t`include \"uvm_macros.svh\"", file = file);
        print (f"", file = file);
        for param in self.parameters:
            (generic_type, generic_value) = self.parameters[param];
            print (f"\tparameter {generic_type} {param} = {generic_value};", file = file);
        print (f"", file = file);
        for it in self.files:
            print (f"\t`include \"{it}\";", file = file);
        print (f"endpackage", file = file);


