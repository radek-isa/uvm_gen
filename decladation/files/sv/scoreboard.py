#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class scoreboard:
    """
        This class generates systemVerilog sequence file
    """

    def __init__(self):
        self.name = "scoreboard"

    def name_get(self):
        return self.name

    @staticmethod
    def gen_decl(obj, lambda_param):
        prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
        array  = "".join([f"[{x[1]}]" for x in lambda_param.array])
        prefix = "\t";

        ret = "";
        if (obj.dir ==  instantiation.agent_dir.TX):
            ret += f"{prefix}uvm_common::comparer_ordered#({obj.item2string(obj.dir)}) cmp_{obj.name}{array};\n"
        return ret

    @staticmethod
    def gen_used(obj, lambda_param):
        direction = False
        array  = "".join([f"[{x[0]}]" for x in lambda_param.array])

        ret = ""
        if (obj.dir ==  instantiation.agent_dir.TX):
            ret += lambda_param.print_for_start()
            prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
            ret += f"{prefix}ret |= (cmp_{obj.name}{array}.used() != 0);\n"
            ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_success(obj, lambda_param):
        direction = False
        array  = "".join([f"[{x[0]}]" for x in lambda_param.array])

        ret = ""
        if (obj.dir ==  instantiation.agent_dir.TX):
            ret += lambda_param.print_for_start()
            prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
            ret += f"{prefix}ret &= (cmp_{obj.name}{array}.success() != 0);\n"
            ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_build_phase(obj, lambda_param):
        direction = False
        array  = "".join([f"[{x[0]}]" for x in lambda_param.array])
        reg_name_arr = ""
        if (len(lambda_param.array) > 0):
            reg_name_arr = ", $sformatf(\""
            reg_name_arr += "".join([f"_%0d" for x in lambda_param.array])
            reg_name_arr += "\""
            reg_name_arr += "".join([f", {x[0]}" for x in lambda_param.array])
            reg_name_arr += ")"

        ret = ""
        if (obj.dir ==  instantiation.agent_dir.TX):
            ret += lambda_param.print_for_start();
            prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
            ret += f"{prefix}cmp_{obj.name}{array} = uvm_common::comparer_ordered#({obj.item2string(False)})"
            ret += f"::type_id::create({{\"cmp_{obj.name}\"{reg_name_arr}}}, this);\n"
            ret += lambda_param.print_for_end();
        return ret;


    @staticmethod
    def gen_report_phase(obj, lambda_param):
        direction = False
        array  = "".join([f"[{x[0]}]" for x in lambda_param.array])
        reg_name_arr = ""
        if (len(lambda_param.array) > 0):
            reg_name_arr = ", $sformatf(\""
            reg_name_arr += "".join([f"_%0d" for x in lambda_param.array])
            reg_name_arr += "\""
            reg_name_arr += "".join([f", {x[0]}" for x in lambda_param.array])
            reg_name_arr += ")"

        ret = ""
        if (obj.dir ==  instantiation.agent_dir.TX):
            ret += lambda_param.print_for_start();
            prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
            ret += f"{prefix}msg = {{msg, cmp_{obj.name}{array}.info(failed)}};\n"
            ret += lambda_param.print_for_end();
        return ret;

    def generate(self, file, blocks, generic):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = "scoreboard.sv"), file = file)
        print (f"class scoreboard{generic_decl} extends uvm_component;", file = file)
        print (f"\t`uvm_component_param_utils(uvm_env_top::scoreboard{generic_assign})", file = file)
        print (f"", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param();
            lambda_gen = [scoreboard.gen_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')

        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction int unsigned used();", file = file)
        print (f"\t\tint unsigned ret = 0;", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [scoreboard.gen_used];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\t\treturn ret;", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction int unsigned success();", file = file)
        print (f"\t\tint unsigned ret = 1;", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [scoreboard.gen_success];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\t\treturn ret;", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.build_phase(phase);", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [scoreboard.gen_build_phase];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')

        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.connect_phase(phase);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\ttask run_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.run_phase(phase);", file = file)
        print (f"\tendtask", file = file)
        print (f"", file = file)
        print (f"\tfunction void report_phase(uvm_phase phase);", file = file)
        print (f"\t\tstring msg = \"\";", file = file)
        print (f"\t\tlogic failed = (this.success() == 0 || this.used() == 1) ? 1'b1 : 1'b0;", file = file)
        print (f"\t\tsuper.report_phase(phase);", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [scoreboard.gen_report_phase];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print ("\t\t`uvm_info(this.get_full_name(), msg, UVM_NONE);", file = file)
        print (f"\tendfunction", file = file)
        print (f"endclass", file = file)


