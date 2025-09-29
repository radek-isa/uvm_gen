#!/bin/python3

import instantiation

class uvm_logic_vector_array_mfb:
    """
        This class generate predefined environment.
    """

    def __init__(self):
        print(f"init uvm_logic_vector_array_mfb")

    def create(self, xml):
        return  instantiation.uvm_logic_vector_array_mfb(self, xml)

    def gen_pkg(self, path, name):
        print(f"uvm_logic_vector_array_mfb {name} {path}")

    def module_path(self, name):
        return f"lappend COMPONENTS [ list \"{name}\"  \"$SV_UVM_BASE/logic_vector_array_mfb\"   \"FULL\"]"

