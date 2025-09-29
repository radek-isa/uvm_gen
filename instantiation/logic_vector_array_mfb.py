#!/bin/python3

from .constant import *

class uvm_logic_vector_array_mfb:

    """
        This class represent instantionation of uvm_logic_vector_array_mfb. 
    """

    def __init__(self, type_class, xml):
        # get direction
        self.type     = type_class;
        self.name  = xml.get("name")
        self.dir   = str2agent_dir(xml.get("dir"))
        self.reset = xml.get("reset")
        self.meta_behav = "META_NONE"

        # load generic
        self.generics = {}
        self.generics["REGIONS"]      = xml.find("generics/regions").text
        self.generics["REGION_SIZE"]  = xml.find("generics/region_size").text
        self.generics["BLOCK_SIZE"]   = xml.find("generics/block_size").text
        self.generics["ITEM_WIDTH"]   = xml.find("generics/item_width").text
        self.generics["META_WIDTH"]   = "0";

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
        return "analysis_port_data"

    # this generate cmd string
    # semicolon is added by last agent
    # f_string containst variable {agent} {item} {prefix}
    #def cmd2string(self, f_string, direction, prefix = ""):
    #    ret_str = ""
    #    ret_str +=  f_string.format(agent = self.name, item = self.item2string(direction), prefix = prefix)
    #    ret_str += ";"
    #    return ret_str;

    def generic2string(self):
        generic = self.generics["REGIONS"]
        generic += "," + self.generics["REGION_SIZE"]
        generic += "," + self.generics["BLOCK_SIZE"]
        generic += "," + self.generics["ITEM_WIDTH"]
        generic += "," + self.generics["META_WIDTH"]
        return f"#({generic})"

    def pkg2string(self):
        return f"uvm_logic_vector_array_mfb"

    def type2string(self, direction):
        tmp_dir = agent_dir_get(self.dir, direction)
        if (tmp_dir == agent_dir.RX):
            return f"uvm_logic_vector_array_mfb::env_rx{self.generic2string()}"
        elif (tmp_dir == agent_dir.TX):
            return f"uvm_logic_vector_array_mfb::env_tx{self.generic2string()}"
        else:
            return f"uvm_logic_vector_array_mfb::{direction}{self.generic2string()}"

    def item2string(self, direction):
        generic = self.generics["ITEM_WIDTH"]
        return f"uvm_logic_vector_array::sequence_item#({generic})"

    def cmd2string(self, f_string, direction, prefix):
        config =""
        for cfg in self.cfg:
            config += f"{prefix}cfg.{cfg} = {self.cfg[cfg]};\n"

        return f_string.format(
                    prefix = prefix,
                    item = self.item2string(direction),
                    array = "",
                    reg_array = "",
                    br_left    = "{",
                    br_right   = "}",
                    agent = self.name,
                    type_name = self.type2string(direction),
                    generic_assign = self.generic2string(),
                    cfg = config,
                    analysis_port = self.analysis_port(direction),
                    pkg = self.pkg2string()
                )

    def cmd_inst2string(self, f_string, direction, prefix, array):
        #config =""
        #for cfg in self.cfg:
        #    config += f"{prefix}cfg.{cfg} = {self.cfg[cfg]};\n"

        return f_string.format(
                    prefix = prefix,
                    item = self.item2string(direction),
                    array = array,
                    agent = self.name,
                    type_name = self.type2string(direction),
                    generic_assign = self.generic2string(),
                    #cfg = config,
                    analysis_port = self.analysis_port(direction),
                    pkg = self.pkg2string()
                )

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
        block_generic = cfg_substitute(cfg, self.generics);
        generic = "#("
        generic += f"\n{prefix}\t"  + block_generic["REGIONS"]
        generic += f"\n{prefix}\t," + block_generic["REGION_SIZE"]
        generic += f"\n{prefix}\t," + block_generic["BLOCK_SIZE"]
        generic += f"\n{prefix}\t," + block_generic["ITEM_WIDTH"]
        generic += f"\n{prefix}\t," + block_generic["META_WIDTH"]
        generic += f"\n{prefix})"

        str_ret = f_string.format(
                prefix   = "",
                inf_type = f"mfb_if {generic}",
                inf_name = name + "_" + self.name,
                array    = array
            )
        return [ str_ret ]

    def interfaces2cmd(self, cfg, f_string, prefix, reg_name, name, array):
        block_generic = cfg_substitute(cfg, self.generics);
        generic = "#("
        generic += f"\n{prefix}\t"  + block_generic["REGIONS"]
        generic += f"\n{prefix}\t," + block_generic["REGION_SIZE"]
        generic += f"\n{prefix}\t," + block_generic["BLOCK_SIZE"]
        generic += f"\n{prefix}\t," + block_generic["ITEM_WIDTH"]
        generic += f"\n{prefix}\t," + block_generic["META_WIDTH"]
        generic += f"\n{prefix})" 

        str_ret = f_string.format(
                prefix   = prefix,
                inf_type = f"mfb_if {generic}",
                reg_name = reg_name + ", \"_" + self.name + "\"",
                inf_name = name + "_" + self.name,
                array    = array
            )
        return str_ret


