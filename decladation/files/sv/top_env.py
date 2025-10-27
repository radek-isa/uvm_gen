#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class top_env:
    """
        This class generates systemVerilog environment file
    """
    def __init__(self):
        self.name = "env"

    def name_get(self):
        return self.name

    @staticmethod
    def gen_build_phase(obj, lambda_param):
        direction = False
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);

        reg_name_arr = ""
        if (len(lambda_param.array) > 0):
            reg_name_arr = ", $sformatf(\""
            reg_name_arr += "".join([f"_%0d" for x in lambda_param.array])
            reg_name_arr += "\""
            reg_name_arr += "".join([f", {x[0]}" for x in lambda_param.array])
            reg_name_arr += ")"

        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}begin\n"
        ret += f"{prefix}\t{obj.pkg2string()}::config_item cfg;\n"
        ret += f"{prefix}\tcfg = new();\n"
        ret += f"{prefix}\tcfg.interface_name = {{m_config.interface_name{reg_name_arr}, \"_{obj.name}\"}};\n"
        for cfg in obj.cfg:
            ret += f"{prefix}\tcfg.{cfg} = {obj.cfg[cfg]};\n";
        ret += "\n"
        ret += f"{prefix}\tuvm_config_db#({obj.pkg2string()}::config_item)::set(this, {{\"{obj.name}\"{reg_name_arr}}}, \"m_config\", cfg);\n"
        ret += f"{prefix}\t{obj.name}{array} = {obj.type2string(direction)}::type_id::create({{\"{obj.name}\"{reg_name_arr}}}, this);\n"
        ret += f"{prefix}end\n"
        ret += lambda_param.print_for_end()

        return ret

    @staticmethod
    def gen_reset_connect(obj, lambda_param):
        direction = False
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);
        f_string = "{prefix}{reset_connet}({agent}{array}.reset_sync);\n"

        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()
        ret += obj.reset2string(f_string, prefix, array)
        ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_connect_phase(obj, lambda_param):
        direction = False
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);

        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()
        if (obj.dir ==  instantiation.agent_dir.RX):
            ret += f"{prefix}{obj.name}{array}.{obj.analysis_port(direction)}.connect("
            ret += f"m_model.fifo_{obj.name}{array}.analysis_export);\n"
        elif (obj.dir ==  instantiation.agent_dir.TX):
            ret += f"{prefix}{obj.name}{array}.{obj.analysis_port(direction)}.connect("
            ret += f"m_scoreboard.cmp_{obj.name}{array}.analysis_imp_dut);\n"

            ret += f"{prefix}m_model.port_{obj.name}{array}.connect("
            ret += f"m_scoreboard.cmp_{obj.name}{array}.analysis_imp_model);\n"
        else:
            ret += ""
        ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_decl(obj, lambda_param):
        array   = "".join([f"[{x[1]}]" for x in lambda_param.array])
        prefix  = lambda_param.print_prefix()

        ret = ""
        ret += f"{prefix}protected {obj.type2string(False)} {obj.name} {array};\n"
        return ret

    def generate(self, file, blocks, generic):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = "env.sv"), file = file)
        print (f"class env_top{generic_decl} extends uvm_env;", file = file)
        print (f"\t`uvm_component_param_utils(uvm_env_top::env_top{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tsequencer{generic_assign} m_sequencer;", file = file)
        print (f"", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(1);
            lambda_gen = [top_env.gen_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')

        print (f"\tprotected model{generic_assign}       m_model;", file = file)
        print (f"\tprotected scoreboard{generic_assign}  m_scoreboard;", file = file)
        print (f"\tprotected config_item m_config;", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction int unsigned success();", file = file)
        print (f"\t\tint unsigned ret = 1;", file = file)
        print (f"\t\tret &= (m_scoreboard.success() != 0);", file = file)
        print (f"\t\treturn ret;", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"", file = file)
        print (f"\tfunction int unsigned used();", file = file)
        print (f"\t\tint unsigned ret = 0;", file = file)
        print (f"\t\tret |= (m_model.used() != 0);", file = file)
        print (f"\t\tret |= (m_scoreboard.used() != 0);", file = file)
        print (f"\t\treturn ret;", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)

        print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
        print (f"\t\tm_config = new(); // Just hotfix for now", file = file)
        print (f"\t\tsuper.build_phase(phase);", file = file)
        print (f"", file = file)
        #self.block
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [top_env.gen_build_phase ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')

        print (f"", file = file)
        print (f"\t\tm_model      = model{generic_assign}::type_id::create(\"m_model\", this);", file = file)
        print (f"\t\tm_scoreboard = scoreboard{generic_assign}::type_id::create(\"m_scoreboard\", this);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.connect_phase(phase);", file = file)
        print (f"", file = file)
        #self.reset
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [top_env.gen_reset_connect ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [top_env.gen_connect_phase];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\tendfunction", file = file)
        print (f"endclass", file = file)

