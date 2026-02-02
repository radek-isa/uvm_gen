#!/bin/python3

import base

class uvm_logic_vector_mvb:

    """
        This class represent instantionation of uvm_logic_vector_mvb.
    """

    def __init__(self, type_class, xml):
        # get direction
        self.type     = type_class;
        self.name  = xml.get("name")
        self.dir   = base.str2agent_dir(xml.get("dir"))
        self.reset = xml.get("reset")

        # load generic
        self.generics = {}
        self.generics["ITEMS"]      = xml.find("generics/items").text
        self.generics["ITEM_WIDTH"] = xml.find("generics/item_width").text

        # load copnfig
        self.cfg = {}
        for cfg in xml.find('config'):
            self.cfg[cfg.tag] = cfg.text;

        # load interface name
        self.name = xml.get("name")

    def lambda2string(self, lambda_fce, lambda_param):
        ret_str = ""
        for it in lambda_fce:
            ret_str += it(self, lambda_param)
        return ret_str


    def analysis_port(self, direction):
        return "analysis_port"

    def generic2string(self):
        generic  =       self.generics["ITEMS"]
        generic += "," + self.generics["ITEM_WIDTH"]
        return f"#({generic})"

    def pkg2string(self):
        return f"uvm_logic_vector_mvb"

    def type2string(self, direction):
        tmp_dir = base.agent_dir_get(self.dir, direction)
        if (tmp_dir == base.agent_dir.RX):
            return f"uvm_logic_vector_mvb::env_rx{self.generic2string()}"
        elif (tmp_dir == base.agent_dir.TX):
            return f"uvm_logic_vector_mvb::env_tx{self.generic2string()}"
        else:
            return f"uvm_logic_vector_mvb::{direction}{self.generic2string()}"

    def sequence2string(self, direction):
        tmp_dir = base.agent_dir_get(self.dir, direction)
        if (tmp_dir == base.agent_dir.RX):
            item_width = self.generics["ITEM_WIDTH"];
            return f"uvm_logic_vector::sequence_simple{item_width}"
        elif (tmp_dir == base.agent_dir.TX):
            return None
        else:
            return None

    def item2string(self, direction):
        generic = self.generics["ITEM_WIDTH"]
        return f"uvm_logic_vector::sequence_item#({generic})"

    def reset2string(self, f_string, prefix, array):
        reset_connet = f"{self.reset}.sync_connect" if self.reset != None else "reset_sync.push_back"
        return f_string.format(
                    agent = self.name,
                    array = array,
                    prefix = prefix,
                    reset_connet = reset_connet
                )

    def agents_get(self, agents):
        agents.append(self)

    def interfaces2inst(self, cfg, f_string, name, array, clk):
        prefix = "\t"
        block_generic = base.cfg_substitute(cfg, self.generics);
        generic = "#("
        generic += f"\n{prefix}\t"  + block_generic["ITEMS"]
        generic += f"\n{prefix}\t," + block_generic["ITEM_WIDTH"]
        generic += f"\n{prefix})"

        str_ret = f_string.format(
                prefix   = "",
                inf_type = f"mvb_if {generic}",
                inf_name = name + "_" + self.name,
                array    = array
            )
        return [ str_ret ]

    def interfaces2cmd(self, cfg, f_string, prefix, reg_name, name, array):
        block_generic = base.cfg_substitute(cfg, self.generics);
        generic = "#("
        generic += f"\n{prefix}\t"  + block_generic["ITEMS"]     
        generic += f"\n{prefix}\t," + block_generic["ITEM_WIDTH"]
        generic += f"\n{prefix})" 

        str_ret = f_string.format(
                prefix   = prefix,
                inf_type = f"mvb_if {generic}",
                reg_name = reg_name + ", \"_" + self.name + "\"",
                inf_name = name + "_" + self.name,
                array    = array
            )
        return str_ret


