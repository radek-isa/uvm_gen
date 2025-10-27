#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class driver:
    """
        This class generates systemVerilog sequence file
    """

    def __init__(self, pkg_name, blocks):
        self.pkg_name = pkg_name
        self.blocks   = blocks
        self.name     = "driver"
    
    def name_get(self):
        return self.name

    @staticmethod
    def gen_run_phase_fifo_decl(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[1]}]" for x in lambda_param.array]);
        ret = ""
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}uvm_common::fifo#({obj.item2string(direction)}) {obj.name}_fifo{array};\n" 
        return ret

    @staticmethod
    def gen_run_phase_fifo_get(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);

        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}assert(uvm_config_db#(uvm_common::fifo#({obj.item2string(direction)}))::get(this, \"\", \"{obj.name}_fifo\"  ,  {obj.name}_fifo{array}));\n"
        ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_run_phase_item_decl(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[1]}]" for x in lambda_param.array]);
        ret = ""
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}{obj.item2string(direction)} item_{obj.name}{array};\n" 
        return ret

    @staticmethod
    def gen_run_phase_item_create(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[1]}]" for x in lambda_param.array]);
        ret = ""
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}item_{obj.name}{array} = {obj.item2string(direction)}::type_id::create(\"item_{obj.name}\", this);\n" 
        return ret

    @staticmethod
    def gen_run_phase_item_send(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[1]}]" for x in lambda_param.array]);
        ret = ""
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}{obj.name}_fifo{array}.push_back(item_{obj.name}{array});\n" 
        return ret


    def generate(self, file, generic):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = "driver.sv"), file = file)
        print (f"class driver{generic_decl} extends uvm_driver#(sequence_item{generic_assign});", file = file)
        print (f"\t`uvm_component_param_utils(uvm_{self.pkg_name}::driver{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tuvm_reset::sync_terminate reset_sync;", file = file);
        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
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
        print (f"\ttask run_phase(uvm_phase phase);", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [driver.gen_run_phase_fifo_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [driver.gen_run_phase_fifo_get];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\t\tforever begin", file = file)
        print (f"", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(3);
            lambda_gen = [driver.gen_run_phase_item_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\t\t\tseq_item_port.get_next_item(req);", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(3);
            lambda_gen = [driver.gen_run_phase_item_create];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\t\t\t`uvm_fatal(this.get_type_name(), \"\\n\\tNOT IMPLEMENTED!!!\");", file = file)
        print (f"", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(3);
            lambda_gen = [driver.gen_run_phase_item_send];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\t\t\tseq_item_port.item_done();", file = file)
        print (f"\t\tend", file = file)
        print (f"\tendtask", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)

