#!/bin/python3

from .constant import *

class uvm_reset:
    
    """
        This class represent instantionation of reset.
    """

    def __init__(self, type_class, xml):
        # get direction
        self.dir =  agent_dir.RX
        #self.dir = xml.get("dir") 

        # load interface name
        self.type     = type_class;
        self.name = xml.get("name")

        # load copnfig
        self.cfg = {}
        for cfg in xml.find('config'):
            self.cfg[cfg.tag] = cfg.text;

    def lambda2string(self, lambda_fce, lambda_param):
        ret_str = ""
        for it in lambda_fce:
            ret_str += it(self, lambda_param)
        return ret_str

    def analysis_port(self, direction):
        return "analysis_port"

    def generic2string(self):
        return f""

    def pkg2string(self):
        return f"uvm_reset"

    def type2string(self, direction):
        return f"uvm_reset::agent"

    def sequence2string(self, direction):
        tmp_dir = agent_dir_get(self.dir, direction)
        if (tmp_dir == agent_dir.RX):
            return f"uvm_reset::sequence_start"
        else:
            return None

    def item2string(self, direction):
        return f"uvm_reset::sequence_item"

    def inf_inst2string(self, f_string, prefix, array):
        return f_string.format(
                    prefix = prefix,
                    array = array,
                    name = self.name,
                    inf = "reset_if" + self.generic2string()
                )

    def reset2string(self, f_string, prefix, array):
        return ""

    def interfaces2inst(self, cfg, f_string, name, array, clk):
        str_ret = f_string.format(
                prefix   = "",
                inf_type = "reset_if",
                inf_name = name + "_" + self.name,
                array    = array
            )
        return [ str_ret ]

    def interfaces2cmd(self, cfg, f_string, prefix, reg_name, name, array):
        str_ret = f_string.format(
                prefix   = prefix,
                inf_type = "reset_if",
                reg_name = reg_name + ", \"_" + self.name + "\"",
                inf_name = name + "_" + self.name,
                array    = array
            )
        return str_ret

