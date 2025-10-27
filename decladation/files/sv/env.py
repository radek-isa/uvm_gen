#!/bin/python3

import pathlib
import os

from .constant   import uvm_gen_preambule
import instantiation

class env_lambda_param(instantiation.lambda_param):

    def __init__(self, prefix = 0, direction = False):
        super().__init__(prefix, direction)
        self.generic_assign = ""



class env:

    """
        This class generates systemVerilog environment file
    """
    def __init__(self, pkt_name, blocks):
        self.pkt_name = pkt_name
        self.blocks   = blocks
        self.name     = "env"

    def name_get(self):
        return self.name

    @staticmethod
    def gen_decl(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[1]}]" for x in lambda_param.array]);
        ret = ""
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}protected {obj.type2string(direction)} {obj.name}{array};\n"
        ret += f"{prefix}protected uvm_common::fifo#({obj.item2string(direction)}) {obj.name}_fifo{array};\n"
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
    def gen_build_phase_fifo(obj, lambda_param):
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
        ret += f"{prefix}{obj.name}_fifo{array} = uvm_common::fifo#({obj.item2string(direction)})::type_id::create({{\"{obj.name}_fifo\"{reg_name_arr}}}, this);\n"
        ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_reset_connect(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);

        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()
        reset_connet = f"{obj.reset}.sync_connect" if obj.reset != None else "reset_sync.push_back"
        f_string = f"{prefix}{reset_connet}({obj.name}{array}.reset_sync);\n"
        ret += obj.reset2string(f_string, prefix, array)
        ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_connet_phase(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);

        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()

        ret += f"{prefix}{obj.name}{array}.{obj.analysis_port(direction)}.connect(m_monitor.{obj.name}_fifo{array}.analysis_export);\n"
        ret += lambda_param.print_for_end()
        return ret

    @staticmethod
    def gen_connet_phase_fifo(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);

        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()
        ret += f"{prefix}uvm_config_db#(uvm_common::fifo#({obj.item2string(direction)}))::set({obj.name}{array}.m_sequencer , \"\" , \"fifo\",  {obj.name}_fifo{array});\n"
        ret += f"{prefix}uvm_config_db#(uvm_common::fifo#({obj.item2string(direction)}))::set(m_driver, \"\", \"{obj.name}_fifo\",  {obj.name}_fifo{array});\n"
        ret += lambda_param.print_for_end()
        return ret


    @staticmethod
    def gen_run_phase(obj, lambda_param):
        direction = lambda_param.direction
        array = "".join([f"[{x[0]}]" for x in lambda_param.array]);

        env_generic = lambda_param.generic_assign
        ret = ""
        ret += lambda_param.print_for_start()
        prefix  = lambda_param.print_prefix()
        # Generic assign is from top component!
        ret += f"{prefix}fork\n"
        ret += f"{prefix}\tforever begin\n"
        ret += f"{prefix}\t\t{obj.name}_low_sequence_lib{env_generic} {obj.name}_low_seq;\n"
        ret += f"{prefix}\t\t{obj.name}_low_seq = {obj.name}_low_sequence_lib{env_generic}::type_id::create(\"{obj.name}_low_seq\", this);\n"
        ret += f"{prefix}\t\tassert({obj.name}_low_seq.randomize()) else begin `uvm_fatal(this.get_full_name(), \"\\n\\tCannot randomize {obj.name}_low_seq\"); end\n"
        ret += f"{prefix}\t\t{obj.name}_low_seq.start({obj.name}{array}.m_sequencer);\n"
        ret += f"{prefix}\tend\n"
        ret += f"{prefix}join_none\n"
        ret += f"{prefix}#(0); // Run first fork then continue\n"
        ret += lambda_param.print_for_end()
        return ret


    def generate(self, file, generic):
        (generic_decl, generic_assign) = generic

        print (uvm_gen_preambule.format(name = "env.sv"), file = file)
        print (f"class env_rx{generic_decl} extends uvm_env;", file = file)
        print (f"\t`uvm_component_param_utils(uvm_{self.pkt_name}::env_rx{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tuvm_analysis_port #(sequence_item{generic_assign}) analysis_port;", file = file)
        print (f"\tsequencer{generic_assign} m_sequencer;", file = file)
        print (f"\tuvm_reset::sync_cbs reset_sync;", file = file)
        print (f"", file = file)
        print (f"\tprotected monitor{generic_assign} m_monitor;", file = file)
        print (f"\tprotected driver{generic_assign}  m_driver;", file = file)
        print (f"", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(1);
            lambda_gen = [env.gen_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\tprotected config_item m_config;", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.build_phase(phase);", file = file)
        print (f"", file = file)
        print (f"\t\t\treset_sync = new();", file = file)
        print (f"", file = file)
        print (f"\t\tif(!uvm_config_db #(config_item)::get(this, \"\", \"m_config\", m_config)) begin", file = file)
        print (f"\t\t\t`uvm_fatal(get_type_name(), \"\\n\\tUnable to get configuration object\")", file = file)
        print (f"\t\tend", file = file)
        print (f"", file = file)
        print (f"\t\tm_monitor = monitor{generic_assign}::type_id::create(\"m_monitor\", this);", file = file)
        print (f"\t\tif (m_config.active == UVM_ACTIVE) begin", file = file)
        print (f"\t\t\tm_sequencer = sequencer{generic_assign}::type_id::create(\"m_sequencer\", this);", file = file)
        print (f"\t\t\tm_driver  = driver{generic_assign}::type_id::create(\"m_driver\", this);", file = file)
        print (f"\t\tend else begin", file = file)
        print (f"\t\t\tm_sequencer = null;", file = file)
        print (f"\t\t\tm_driver    = null;", file = file)
        print (f"\t\tend", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [env.gen_build_phase ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [env.gen_build_phase_fifo ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.connect_phase(phase);", file = file)
        print (f"", file = file)
        print (f"\t\treset_sync.push_back(m_monitor.reset_sync);", file = file)
        print (f"\t\tanalysis_port = m_monitor.analysis_port;", file = file)
        print (f"\t\tif (m_config.active == UVM_ACTIVE) begin", file = file)
        print (f"\t\t\treset_sync.push_back(m_sequencer.reset_sync);", file = file)
        print (f"\t\t\treset_sync.push_back(m_driver.reset_sync);", file = file)
        print (f"\t\t\tm_driver.seq_item_port.connect(m_sequencer.seq_item_export);", file = file)
        print (f"\t\t\t// Connect lower agents monitor to hight level monitor", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [env.gen_connet_phase_fifo ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\t\tend", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [env.gen_connet_phase ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [env.gen_reset_connect ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"", file = file)
        print (f"\t\t// connect driver and low level sequence", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\ttask run_phase (uvm_phase phase);", file = file)
        print (f"\t\tif (m_config.active == UVM_ACTIVE) begin", file = file)
        for block in self.blocks:
            lambda_param = env_lambda_param(3);
            lambda_param.generic_assign = generic_assign
            lambda_gen = [env.gen_run_phase ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\t\tend", file = file)
        print (f"", file = file)
        print (f"\t\tsuper.run_phase(phase);", file = file)
        print (f"\tendtask", file = file)
        print (f"endclass", file = file)


        #################### TODO: United with RX_environment
        ## ETH_TX
        print (f"", file = file)
        print (f"", file = file)
        print (f"class env_tx{generic_decl} extends uvm_env;", file = file)
        print (f"\t`uvm_component_param_utils(uvm_{self.pkt_name}::env_tx{generic_assign})", file = file)
        print (f"", file = file)
        print (f"\tuvm_analysis_port #(sequence_item{generic_assign}) analysis_port;", file = file)
        #print (f"\tsequencer{generic_assign} m_sequencer;", file = file)
        print (f"\tuvm_reset::sync_cbs reset_sync;", file = file)
        print (f"", file = file)
        print (f"\tprotected monitor{generic_assign} m_monitor;", file = file)
        #print (f"\tprotected driver{generic_assign}  m_driver;", file = file)
        print (f"", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(1, True);
            lambda_gen = [env.gen_decl];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')

        print (f"", file = file)
        print (f"\tprotected config_item m_config;", file = file)
        print (f"", file = file)
        print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
        print (f"", file = file)
        print (f"\t\tsuper.build_phase(phase);", file = file)
        print (f"", file = file)
        print (f"\t\t\treset_sync = new();", file = file)
        print (f"", file = file)
        print (f"\t\tif(!uvm_config_db #(config_item)::get(this, \"\", \"m_config\", m_config)) begin", file = file)
        print (f"\t\t\t`uvm_fatal(get_type_name(), \"\\n\\tUnable to get configuration object\")", file = file)
        print (f"\t\tend", file = file)
        print (f"", file = file)
        print (f"\t\tm_monitor = monitor{generic_assign}::type_id::create(\"m_monitor\", this);", file = file)
        print (f"", file = file)
        # Create agent environment
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2, True);
            lambda_gen = [env.gen_build_phase ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
        print (f"\t\tsuper.connect_phase(phase);", file = file)
        print (f"\t\tanalysis_port = m_monitor.analysis_port;", file = file)
        print (f"", file = file)
        print (f"\t\treset_sync.push_back(m_monitor.reset_sync);", file = file)
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [env.gen_reset_connect ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        for block in self.blocks:
            lambda_param = instantiation.lambda_param(2);
            lambda_gen = [env.gen_connet_phase ];
            ret_str = block.lambda2string(lambda_gen, lambda_param);
            print (ret_str, file = file, end='')
        print (f"\tendfunction", file = file)
        print (f"", file = file)
        print (f"endclass", file = file)


