#!/bin/python3

from .constant import *

class uvm_env:

    """
        This class represent instantionation of uvm_env.
    """

#    def __init__(self, xml, interfaces):
    def __init__(self, type_class, xml):
        self.type     = type_class;
        self.pkg_name = xml.tag
        self.name  = xml.get("name")
        self.dir   = str2agent_dir(xml.get("dir"))
        self.reset = xml.get("reset")
        self.meta_behav = "META_NONE"

        # load generic
        self.generics = {}
        # get default value
        for generic in type_class.generics:
            self.generics[generic] =  type_class.generics[generic]["value"]
        #get set value
        for generic in xml.find('generics'):
            self.generics[generic.tag] = generic.text.strip()

        self.cfg = {}
        for cfg in xml.find('config'):
            self.cfg[cfg.tag] = cfg.text;

        #self.interfaces = interfaces

    def lambda2string(self, lambda_fce, lambda_param):
        ret_str = ""
        for it in lambda_fce:
            ret_str += it(self, lambda_param)
        return ret_str

    def analysis_port(self, direction):
        return "analysis_port"

    def reset2string(self, f_string, prefix, array):
        reset_connet = f"{self.reset}.sync_connect" if self.reset != None else "reset_sync.push_back"
        return f_string.format(
                    agent = self.name,
                    array = array,
                    prefix = prefix,
                    reset_connet = reset_connet 
                )

    def generic2string(self):
        if (len(self.generics) == 0):
            return ""

        generic = ""
        sep     = ""
        for it in self.generics:
            generic += sep + self.generics[it]
            sep = ", "
        return f"#({generic})"

    def pkg2string(self):
        return f"uvm_{self.pkg_name}"

    def type2string(self, direction):
        tmp_dir = agent_dir_get(self.dir, direction)
        if (tmp_dir == agent_dir.RX):
            return f"uvm_{self.pkg_name}::env_rx{self.generic2string()}"
        elif (tmp_dir == agent_dir.TX):
            return f"uvm_{self.pkg_name}::env_tx{self.generic2string()}"
        else:
            return f"uvm_{self.pkg_name}::{direction}{self.generic2string()}"

    def sequence2string(self, direction):
        return f"uvm_{self.pkg_name}::sequence_lib{self.generic2string()}"

    def item2string(self, direction):
        return f"uvm_{self.pkg_name}::sequence_item{self.generic2string()}"

    def interfaces2inst(self, cfg, f_string, name, array, clk):
        ret = []
        block_cfg = cfg_substitute(cfg, self.generics);
        for inf in self.type.blocks:
            ret += inf.interfaces2inst(block_cfg, f_string, name + "_" + self.name, array, clk);
        return ret
   
    def interfaces2cmd(self, cfg, f_string, prefix, reg_name, name, array):
        ret = ""
        block_cfg = cfg_substitute(cfg, self.generics);
        reg_name = reg_name + ", \"_" + self.name + "\""
        name     = name + "_" + self.name
        for inf in self.type.blocks:
            #generate configuration
            ret += inf.interfaces2cmd(block_cfg, f_string, prefix, reg_name, name, array);
        return ret

