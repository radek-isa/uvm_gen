#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class virt_sequence:
    """
        This class generates systemVerilog sequence file
    """

    def __init__(self):
        self.name = "sequence"
    
    def name_get(self):
        return self.name

    @staticmethod
    def gen_seq_decl(obj, lambda_param):
        prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
        array  = "".join([f"[{x[1]}]" for x in lambda_param.array])

        ret = ""
        if (obj.sequence2string(False) != None):
            ret += f"{prefix}protected {obj.sequence2string(False)} seq_{obj.name}{array};\n"
        return ret

    @staticmethod
    def gen_seq_create(obj, lambda_param):
        array  = "".join([f"[{x[0]}]" for x in lambda_param.array])
        reg_name_arr = ""
        if (len(lambda_param.array) > 0):
            reg_name_arr = ", $sformatf(\""
            reg_name_arr += "".join([f"_%0d" for x in lambda_param.array])
            reg_name_arr += "\""
            reg_name_arr += "".join([f", {x[0]}" for x in lambda_param.array])
            reg_name_arr += ")"

        ret = ""
        if (obj.sequence2string(False) != None):
            ret += lambda_param.print_for_start()
            prefix = "".join(["\t" for x in range (0, lambda_param.prefix)])
            ret += f"{prefix}seq_{obj.name}{array} = {obj.sequence2string(False)}" 
            ret += f"::type_id::create({{\"seq_{obj.name}\"{reg_name_arr}}}, p_sequencer.{obj.name}{array});\n"
            ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_seq_run(obj, lambda_param):
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
        ret += f"{prefix}fork\n"
        ret += f"{prefix}\tbegin\n"
        ret += f"{prefix}\t\tassert(seq_{obj.name}{array}.randomize()) else `uvm_fatal(m_sequencer.get_full_name(), \"\\n\\tCannot randomize sequence\");\n"
        ret += f"{prefix}\t\tseq_{obj.name}{array}.start(p_sequencer.{obj.name}{array});\n"
        ret += f"{prefix}\tend\n"
        ret += f"{prefix}join_none;\n"
        ret += f"{prefix}#(0);\n"
        ret += lambda_param.print_for_end()
        return ret

    def generate(self, file, blocks, generic):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = self.name), file = file)
        print (f"class sequence_base{generic_decl} extends uvm_sequence;", file = file)
        print (f"\t`uvm_object_param_utils(uvm_env_top::sequence_base{generic_assign})", file = file)
        print (f"\t`uvm_declare_p_sequencer(uvm_env_top::sequencer{generic_assign})", file = file)
        print (f"", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(1);
            lambda_gen = [virt_sequence.gen_seq_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\tfunction new (string name = \"{self.name}\");\n\t\tsuper.new(name);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\ttask body();", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [virt_sequence.gen_seq_create];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)

        print (f"\t\t// RUN sequnces", file = file)
        for block in blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [virt_sequence.gen_seq_run];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\tendtask", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)

