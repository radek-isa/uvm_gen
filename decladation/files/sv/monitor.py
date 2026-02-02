#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class monitor:
    """
        This class generates systemVerilog driver file
    """

    def __init__(self, pkg_name, blocks):
        self.pkg_name = pkg_name
        self.blocks   = blocks
        self.name     = "monitor"
    
    def name_get(self):
        return self.name

    @staticmethod
    def gen_decl(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[1]}]" for x in lambda_param.array]);
        ret = ""
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}uvm_tlm_analysis_fifo#({obj.item2string(direction)}) {obj.name}_fifo{array};\n\n"
        return ret

    @staticmethod
    def gen_build_phase(obj, lambda_param):
        direction = lambda_param.direction
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
        ret += f"{prefix}{obj.name}_fifo{array} = new({{\"{obj.name}_fifo\"{reg_name_arr}}}, this);\n"
        ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_run_phase_decl(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[1]}]" for x in lambda_param.array]);
        ret = ""
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}{obj.item2string(direction)} item_{obj.name}{array};\n"
        return ret

    @staticmethod
    def gen_run_phase(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);

        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}{obj.name}_fifo{array}.get(item_{obj.name}{array});\n"
        ret += f"{prefix}item.time_array_add(item_{obj.name}{array}.start);\n"
        ret += lambda_param.print_for_end()
        return ret


    def generate(self, file, generic, preambule_inf):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule("monitor.sv", preambule_inf), file = file)
        print (f"class monitor{generic_decl} extends uvm_monitor;", file = file)
        print (f"\t`uvm_component_param_utils(uvm_{self.pkg_name}::monitor{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tuvm_analysis_port #(sequence_item{generic_assign}) analysis_port;", file = file)
        print (f"\tuvm_reset::sync_terminate reset_sync;", file = file);
        print (f"\t//fifo input", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(1);
            lambda_gen = [monitor.gen_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\tprotected sequence_item{generic_assign} item;", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        print (f"\t\tanalysis_port = new(\"analysis port\", this);\n", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [monitor.gen_build_phase];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.build_phase(phase);", file = file)
        print (f"", file = file)
        print (f"\t\treset_sync = new();", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.connect_phase(phase);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\ttask run_phase (uvm_phase phase);", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [monitor.gen_run_phase_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\t\tforever begin", file = file)
        print (f"\t\t\titem = sequence_item{generic_assign}::type_id::create(\"item\", this);", file = file)
        print (f"", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(3);
            lambda_gen = [monitor.gen_run_phase];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\t\t\t`uvm_fatal(this.get_type_name(), \"\\n\\tNo implementation. Please add some implementation\");", file = file)
        print (f"", file = file)
        print (f"\t\t\tanalysis_port.write(item);", file = file)
        print (f"\t\tend", file = file)
        print (f"\tendtask", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)


