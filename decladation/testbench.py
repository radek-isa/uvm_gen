#!/bin/python3

import os

from .block    import block
from .constant import uvm_gen_preambule
import instantiation

class uvm_testbench(block):
    """
        This class generate predefined top environment in testbench. 
    """

    def __init__(self, xml, decl_agents):
        super().__init__(xml, decl_agents)

        self.dut = instantiation.uvm_dut(xml.find('dut'))

        #add file for print
        #TODO: print pkg for tests or top_env?
        self.files_sv.append("config.sv");
        self.files_sv.append("sequencer.sv");
        self.files_sv.append("model.sv");
        self.files_sv.append("scoreboard.sv");
        self.files_sv.append("env.sv");

    def create(self, xml):
        return instantiation.uvm_env_top(xml)

    def gen_pkg(self, path, name):
        super().gen_pkg(path, "env_top")

        pkg_path = path / "env_top"

        generic_decl   = self._generic_decl();
        generic_assign = self._generic_assign();

        with open(pkg_path / "sequencer.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "sequencer.sv"), file = file)
            print (f"class sequencer{generic_decl} extends uvm_sequencer;", file = file)
            print (f"\t`uvm_component_param_utils(uvm_env_top::sequencer{generic_assign})", file = file)
            print (f"", file = file)
            for block in self.blocks:
                f_string = ""
                f_string += "{prefix}{pkg}::sequencer{generic_assign} {agent}{array};\n"
                ret_str = block.cmd_inst2string(f_string, False, "\t", "")
                print (ret_str, file = file)
            print (f"", file = file)
            print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
            print (f"\t\tsuper.build_phase(phase);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)

        with open(pkg_path / "config.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "config.sv"), file = file)
            print (f"", file = file)
            print (f"class config_item extends uvm_object;", file = file)
            print (f"\tstring interface_name;", file = file)
            print (f"", file = file)
            print (f"\tfunction new (string name = \"\");\n\t\tsuper.new(name);", file = file)
            print (f"\t\tinterface_name = \"vif\";", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)


        with open(pkg_path / "env.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "env.sv"), file = file)
            print (f"class env_top{generic_decl} extends uvm_env;", file = file)
            print (f"\t`uvm_component_param_utils(uvm_env_top::env_top{generic_assign})", file = file)
            print (f"", file = file)
            print (f"\tsequencer{generic_assign} m_sequencer;", file = file)
            print (f"", file = file)
            for block in self.blocks:
                f_string = ""
                f_string += "{prefix}protected {type_name} {agent}{array};\n"
                ret_str = block.cmd_inst2string(f_string, False, "\t", "")
                print (ret_str, file = file)
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
            print (self._gen_block_create(False, "\t\t\t"), file = file)
            print (f"", file = file)
            print (f"\t\tm_model      = model{generic_assign}::type_id::create(\"m_model\", this);", file = file)
            print (f"\t\tm_scoreboard = scoreboard{generic_assign}::type_id::create(\"m_scoreboard\", this);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
            print (f"\t\tsuper.connect_phase(phase);", file = file)
            print (f"", file = file)
            #self.reset
            print(self._gen_block_reset_connect("\t\t"), file = file)
            print (f"", file = file)
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(2);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_start())
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)]))
                lambda_gen.append(lambda obj, lambda_param : obj.name + "".join([f"[{x[0]}]" for x in lambda_param.array]) + "." + obj.analysis_port(obj.dir) + ".connect(")
                #RX
                lambda_gen.append(lambda obj, lambda_param : "m_model.fifo_" + obj.name + "".join([f"[{x[0]}]" for x in lambda_param.array])  if obj.dir ==  instantiation.agent_dir.RX else "")
                lambda_gen.append(lambda obj, lambda_param : ".analysis_export);\n"  if obj.dir ==  instantiation.agent_dir.RX else "")
                #TX
                lambda_gen.append(lambda obj, lambda_param : "m_scoreboard.cmp_" + obj.name + "".join([f"[{x[0]}]" for x in lambda_param.array])  if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : ".analysis_imp_dut);\n"  if obj.dir ==  instantiation.agent_dir.TX else "")
                #TX connct model to DUT
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)])   if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "m_model.port_" + obj.name + "".join([f"[{x[0]}]" for x in lambda_param.array]) +  ".connect("   if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "m_scoreboard.cmp_" + obj.name + "".join([f"[{x[0]}]" for x in lambda_param.array])  if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : ".analysis_imp_model);\n"  if obj.dir ==  instantiation.agent_dir.TX else "")

                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_end())
                ret_str = block.lambda2string(lambda_gen, lambda_param);
                print (ret_str, file = file, end='')
            print (f"\tendfunction", file = file)
            print (f"endclass", file = file)

        with open(pkg_path / "model.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "model.sv"), file = file)
            print (f"class model{generic_decl} extends uvm_component;", file = file)
            print (f"\t`uvm_component_param_utils(uvm_env_top::model{generic_assign})", file = file)
            print (f"", file = file)
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(1);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)]))
                lambda_gen.append(lambda obj, lambda_param : "uvm_tlm_analysis_fifo" if obj.dir ==  instantiation.agent_dir.RX else "uvm_analysis_port")
                lambda_gen.append(lambda obj, lambda_param : "#(" + obj.item2string(obj.dir) + ") ")
                lambda_gen.append(lambda obj, lambda_param : "fifo_" if obj.dir ==  instantiation.agent_dir.RX else "port_")
                lambda_gen.append(lambda obj, lambda_param : obj.name + "".join([f"[{x[1]}]" for x in lambda_param.array]))
                lambda_gen.append(lambda obj, lambda_param : ";\n")
                ret_str = block.lambda2string(lambda_gen, lambda_param);
                print (ret_str, file = file,  end='')
            print (f"", file = file)
            print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(2);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_start())
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)]))
                lambda_gen.append(lambda obj, lambda_param : "fifo_" if obj.dir ==  instantiation.agent_dir.RX else "port_")
                lambda_gen.append(lambda obj, lambda_param : obj.name + "".join([f"[{x[0]}]" for x in lambda_param.array]))
                lambda_gen.append(lambda obj, lambda_param : "".join([" = new($sformatf(\"", "fifo_" if obj.dir ==  instantiation.agent_dir.RX else "port_", obj.name, "".join([f"_%0d" for x in lambda_param.array]), "\"" ,"".join([f", {x[0]}" for x in lambda_param.array]), "), this);\n"]))
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_end())
                ret_str = block.lambda2string(lambda_gen, lambda_param);
                print (ret_str, file = file, end='')
            print (f"\tendfunction", file = file)
            print (f"", file = file)

            print (f"\tfunction int unsigned used();", file = file)
            print (f"\t\tint unsigned ret = 0;", file = file)
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(2);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_start() if obj.dir ==  instantiation.agent_dir.RX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)]) if obj.dir ==  instantiation.agent_dir.RX else "")
                lambda_gen.append(lambda obj, lambda_param : "ret |= (fifo_" + obj.name if obj.dir ==  instantiation.agent_dir.RX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join([f"[{x[0]}]" for x in lambda_param.array]) + ".used() != 0);\n" if obj.dir ==  instantiation.agent_dir.RX else "")
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_end() if obj.dir ==  instantiation.agent_dir.RX else "")
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

        with open(pkg_path / "scoreboard.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "scoreboard.sv"), file = file)
            print (f"class scoreboard{generic_decl} extends uvm_component;", file = file)
            print (f"\t`uvm_component_param_utils(uvm_env_top::scoreboard{generic_assign})", file = file)
            print (f"", file = file)
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(0);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : "\t"                                 if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "uvm_common::comparer_ordered"         if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "#(" + obj.item2string(obj.dir) + ") " if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "cmp_" + obj.name                      if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join([f"[{x[1]}]" for x in lambda_param.array]) + ";" if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "\n"                                   if obj.dir ==  instantiation.agent_dir.TX else "")
                ret_str = block.lambda2string(lambda_gen, lambda_param);
                print (ret_str, file = file, end='')

            print (f"", file = file)
            print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction int unsigned used();", file = file)
            print (f"\t\tint unsigned ret = 0;", file = file)
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(2);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_start() if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)]) if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "ret |= (cmp_" + obj.name if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join([f"[{x[0]}]" for x in lambda_param.array]) + ".used() != 0);\n" if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_end() if obj.dir ==  instantiation.agent_dir.TX else "")
                ret_str = block.lambda2string(lambda_gen, lambda_param);
                print (ret_str, file = file, end='')
            print (f"\t\treturn ret;", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction int unsigned success();", file = file)
            print (f"\t\tint unsigned ret = 1;", file = file)
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(2);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_start() if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)]) if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "ret &= (cmp_" + obj.name if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join([f"[{x[0]}]" for x in lambda_param.array]) + ".success() != 0);\n" if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_end() if obj.dir ==  instantiation.agent_dir.TX else "")
                ret_str = block.lambda2string(lambda_gen, lambda_param);
                print (ret_str, file = file, end='')
            print (f"\t\treturn ret;", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
            print (f"\t\tsuper.build_phase(phase);", file = file)
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(2);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_start() if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)]) if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "cmp_" + obj.name if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join([f"[{x[0]}]" for x in lambda_param.array]) + " = " if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "uvm_common::comparer_ordered#(" +  obj.item2string(obj.dir) + ")" if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "::type_id::create($sformatf(\"cmp_"+ obj.name                     if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join(["_%0d" for x in lambda_param.array]) if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "\"" + "".join([f", {x[0]}" for x in lambda_param.array]) if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "), this);\n" if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_end() if obj.dir ==  instantiation.agent_dir.TX else "")
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
            for block in self.blocks:
                lambda_param = instantiation.lambda_param(2);
                lambda_gen = [];
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_start() if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join(["\t" for x in range (0, lambda_param.prefix)]) if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "msg = {msg, cmp_" + obj.name if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : "".join([f"[{x[0]}]" for x in lambda_param.array]) if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : ".info(failed)};\n" if obj.dir ==  instantiation.agent_dir.TX else "")
                lambda_gen.append(lambda obj, lambda_param : lambda_param.print_for_end() if obj.dir ==  instantiation.agent_dir.TX else "")
                ret_str = block.lambda2string(lambda_gen, lambda_param);
                print (ret_str, file = file, end='')
            print ("\t\t`uvm_info(this.get_full_name(), msg, UVM_NONE);", file = file)
            print (f"\tendfunction", file = file)
            print (f"endclass", file = file)

        with open(path / "testbench.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "tetbench.sv"), file = file)
            print (f"", file = file)
            print (f"import uvm_pkg::*;", file = file)
            print (f"`include \"uvm_macros.svh\"", file = file)
            print (f"import generic_pkg::*;", file = file)
            print (f"", file = file)
            print (f"module testbench;", file = file)
            print (f"", file = file)
            print (f"\ttypedef test::base{generic_assign} base;", file = file)
            print (f"", file = file)
            print (f"\t//generate clock", file = file)
            print (f"\tlogic CLK = 1'b1;", file = file)
            print (f"\talways #(CLK_PERIOD) CLK = ~CLK;", file = file)
            print (f"", file = file)
            print (f"\t//generat interface", file = file)
            #self.block
            for block in self.blocks:
                f_string = "\t{prefix}{inf_type} inf{inf_name} {array} (CLK);"
                for inf in block.interfaces2inst({}, f_string, "", "", "CLK"):
                    print (f"{inf}", file = file)

            #print("", file = file)
            print("\tinitial begin", file = file)
            for block in self.blocks:
                f_string = "\t\t{prefix}automatic virtual {inf_type} vif{inf_name} {array} = inf{inf_name};"
                for inf in block.interfaces2inst({}, f_string, "", "", "CLK"):
                    print (f"{inf}", file = file)
            print("", file = file)

            for block in self.blocks:
                f_string = "{prefix}uvm_config_db#(virtual {inf_type})::set(null, \"\", {{\"vif\" {reg_name} }}, vif{inf_name}{array});\n"
                inf = block.interfaces2cmd({}, f_string, "\t\t", "", "", "")
                print (f"{inf}", file = file)
            #print("", file = file)
            #for inf in self.interfaces:
            #    inf_type = inf[0]
            #    vif_name = inf[1].format(name = "vif", arr = "")
            print("\tend\n", file = file)
            print (f"", file = file)
            dut = self.dut.inst2string("!!!")
            print (f"", file = file)
            print (f"{dut}", file = file)
            print (f"", file = file)
            print (f"\tinitial begin", file = file)
            print (f"\t\tuvm_root m_root;", file = file)
            print (f"\t\t//add interfaces", file = file)
            print (f"", file = file)
            print (f"\t\tm_root = uvm_root::get();", file = file)
            print (f"\t\tm_root.finish_on_completion = 0;", file = file)
            print (f"\t\tm_root.set_report_id_action_hier(\"ILLEGALNAME\", UVM_NO_ACTION);", file = file)
            print (f"", file = file)
            print (f"\t\tuvm_config_db #(int)            ::set(null, \"\", \"recording_detail\", 0);", file = file)
            print (f"\t\tuvm_config_db #(uvm_bitstream_t)::set(null, \"\", \"recording_detail\", 0);", file = file)
            print (f"", file = file)
            print (f"\t\trun_test();", file = file)
            print (f"\t\t$stop(2);", file = file)
            print (f"\tend", file = file)
            print (f"endmodule", file = file)

        with open(path / "generic_pkg.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "pkg.sv"), file = file)
            print (f"package generic_pkg;", file = file)
            print (f"", file = file);
            for generic in self.generics:
                generic_type  = self.generics[generic]["type"];
                generic_value = self.generics[generic]["value"];
                print (f"\tparameter {generic_type} {generic} = {generic_value};", file = file);
            print (f"\t", file = file);
            print (f"\tparameter time CLK_PERIOD = 4ns;", file = file);
            print (f"endpackage", file = file);


        # Create test
        test_path = path / "test"
        if not test_path.exists():
            os.makedirs(test_path)

        with open(test_path / "pkg.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "pkg.sv"), file = file)
            print (f"package test;", file = file)
            print (f"", file = file)
            print (f"\timport uvm_pkg::*;", file = file)
            print (f"\t`include \"uvm_macros.svh\"", file = file)
            print (f"", file = file)
            print (f"\t`include \"base.sv\"", file = file)
            print (f"endpackage", file = file)

        with open(test_path / "base.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "base.sv"), file = file)
            print (f"class base{generic_decl} extends uvm_test;", file = file)
            print (f"\ttypedef uvm_component_registry #(test::base{generic_assign}, \"test::base\") type_id;", file = file)
            print (f"//change to something more generic.", file = file)
            print (f"", file = file)
            print (f"\tuvm_env_top::env_top{generic_assign} m_env;", file = file)
            print (f"", file = file)
            print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tstatic function type_id get_type();", file = file)
            print (f"\t\treturn type_id::get();", file = file)
            print (f"\tendfunction", file = file)
            print (f"\tfunction string get_type_name();", file = file)
            print (f"\t\treturn get_type().get_type_name();", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction void build_phase (uvm_phase phase);\n\t\tsuper.build_phase(phase);", file = file)
            print (f"\t\tm_env = uvm_env_top::env_top{generic_assign}::type_id::create(\"m_env\", this);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\ttask run_phase (uvm_phase phase);", file = file)
            print (f"\t\tphase.raise_objection(this);", file = file)
            print (f"\t\tphase.drop_objection(this);", file = file)
            print (f"\tendtask", file = file)
            print (f"", file = file)
            print (f"\tfunction void report_phase(uvm_phase phase);", file = file)
            print ("\t\tstring msg = \"\";", file = file)
            print ("\t\tmsg = {\"\\n\\tTEST : \", this.get_type_name()};", file = file)
            print (f"", file = file)
            print ("\t\tmsg = {msg, $sformatf(\"\\n\\tSuccess %0d Used %0d\", m_env.success(), m_env.used())};", file = file)
            print (f"\t\tif (m_env.success() == 1 && m_env.used() == 0) begin", file = file)
            print ("\t\t\t`uvm_info(this.get_full_name(), {msg, \"\\n\\n\\t---------------------------------------\\n\\t----     VERIFICATION SUCCESS       ----\\n\\t---------------------------------------\"}, UVM_NONE);", file = file)
            print (f"\t\tend else begin", file = file)
            print ("\t\t\t`uvm_info(this.get_full_name(), {msg, \"\\n\\n\\t---------------------------------------\\n\\t----     VERIFICATION FAILED        ----\\n\\t---------------------------------------\"}, UVM_NONE);", file = file)
            print (f"\t\tend", file = file)
            print (f"\tendfunction", file = file)
            print (f"endclass", file = file)




