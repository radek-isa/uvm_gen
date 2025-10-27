#!/bin/python3

from .. import instantiation

class uvm_logic_vector_mvb:
    """
        This class generate predefined environment. 
    """

    def __init__(self):
        print(f"init uvm_logic_vector_mvb")

    def create(self, xml):
        return  instantiation.uvm_logic_vector_mvb(self, xml)

    def gen_pkg(self, path, name):
        print(f"uvm_logic_vector_mvb {name} {path}")

    def module_path(self, name):
        return f"lappend COMPONENTS [ list \"{name}\"  \"$SV_UVM_BASE/logic_vector_mvb\"   \"FULL\"]"


