#!/bin/python3

from .. import instantiation

class uvm_reset:
    """
        This class generate predefined environment.
    """

    def __init__(self):
        print(f"init uvm_logic_vector_mvb")

    def create(self, xml):
        return  instantiation.uvm_reset(self, xml)

    def gen_pkg(self, path, name, cfg):
        print(f"uvm_reset {name} {path}")

    def module_path(self, name):
        return f"lappend COMPONENTS [ list \"{name}\"  \"$SV_UVM_BASE/reset\"   \"FULL\"]"


