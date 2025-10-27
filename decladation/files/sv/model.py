#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation
import base

class model:
    """
        This class generates systemVerilog model file
    """

    def __init__(self):
        self.name = "model"

    def name_get(self):
        return self.name

    @staticmethod
    def gen_decl(obj, lambda_param):
        direction = False
        prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
        array  = "".join([f"[{x[1]}]" for x in lambda_param.array])

        ret = ""
        if (obj.dir ==  base.agent_dir.RX):
            ret += f"{prefix}uvm_tlm_analysis_fifo#({obj.item2string(direction)}) fifo_{obj.name}{array};\n"
        elif (obj.dir ==  base.agent_dir.TX):
            ret += f"{prefix}uvm_analysis_port    #({obj.item2string(direction)}) port_{obj.name}{array};\n"
        return ret;

    @staticmethod
    def gen_new(obj, lambda_param):
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
        ret += lambda_param.print_for_start()
        prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
        if (obj.dir ==  base.agent_dir.RX):
            ret += f"{prefix}fifo_{obj.name}{array} = new({{\"fifo_{obj.name}\"{reg_name_arr}}}, this);\n";
        elif (obj.dir ==  base.agent_dir.TX):
            ret += f"{prefix}port_{obj.name}{array} = new({{\"port_{obj.name}\"{reg_name_arr}}}, this);\n";
        ret += lambda_param.print_for_end()
        return ret;

    @staticmethod
    def gen_used(obj, lambda_param):
        direction = False
        array  = "".join([f"[{x[0]}]" for x in lambda_param.array])

        ret = ""
        if (obj.dir ==  base.agent_dir.RX):
            ret += lambda_param.print_for_start()
            prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
            ret += f"{prefix}ret |= (fifo_{obj.name}{array}.used() != 0);\n"
            ret += lambda_param.print_for_end()
        return ret


    def generate(self, file, blocks, generic):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = "model.sv"), file = file)
        print (f"class model{generic_decl} extends uvm_component;", file = file)
        print (f"\t`uvm_component_param_utils(uvm_env_top::model{generic_assign})", file = file)
        print (f"", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(1);
            lambda_gen = [model.gen_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')

        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(1);
            lambda_gen = [model.gen_new];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\tendfunction", file = file)
        print (f"", file = file)

        print (f"\tfunction int unsigned used();", file = file)
        print (f"\t\tint unsigned ret = 0;", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(1);
            lambda_gen = [model.gen_used];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\t\treturn ret;", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)

        print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.build_phase(phase);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.connect_phase(phase);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\ttask run_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.run_phase(phase);", file = file)
        print (f"\tendtask", file = file)
        print (f"endclass", file = file)


