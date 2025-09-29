#!/bin/python3

import os

from .block    import block
from .constant import uvm_gen_preambule
import instantiation

class uvm_env(block):
    """
        This class generate predefined environment.
    """

    def __init__(self, xml, decl_agents):
        super().__init__(xml, decl_agents)

        # items
        self.items = []
        for item in xml.findall('sequence_item/item'):
            item_array = item.get("array") if item.get("array") != None else "";
            self.items.append( (item.get("type"), item.text, item_array ));

        convert2string = xml.find('sequence_item/convert2string')
        if (convert2string != None):
            self.convert2string = convert2string.text
        else:
            self.convert2string = "\t\t`uvm_fatal(this.get_type_name(), \"\\nfunction convert2string is not implemented\");"

        agents = []
        self.agents_get(agents)
        for agent in agents:
            self.files_sv.append(f"{agent.name}_low_sequence.sv")
        self.files_sv.append("sequence_item.sv");
        self.files_sv.append("config.sv");
        self.files_sv.append("monitor.sv");
        self.files_sv.append("driver.sv");
        self.files_sv.append("sequencer.sv");
        self.files_sv.append("env.sv");
        self.files_sv.append("sequence.sv");

    def create(self, xml):
        return  instantiation.uvm_env(self, xml)
        #return  instantiation.uvm_env(xml, self.interfaces)

    def gen_pkg(self, path, name):
        super().gen_pkg(path, name)

        pkg_path = path / name

        generic_decl   = self._generic_decl();
        generic_assign = self._generic_assign();

        agents = []
        self.agents_get(agents)
        for agent in agents:
            file_name = f"{agent.name}_low_sequence.sv";
            with open(pkg_path / file_name, 'w') as file:
                agent_seq_item = agent.item2string("");
                print (uvm_gen_preambule.format(name = file_name), file = file)
                print (f"class {agent.name}_config_sequence extends uvm_object;", file = file)
                print (f"\t`uvm_object_utils(uvm_{name}::{agent.name}_config_sequence)", file = file)
                print (f"", file = file)
                print (f"\tfunction new (string name = \"uvm_{name}::config_sequence\");", file = file)
                print (f"\t\tsuper.new(name);", file = file)
                print (f"\tendfunction", file = file)
                print (f"", file = file)
                print (f"endclass", file = file)

                print (f"", file = file)
                print (f"class {agent.name}_low_sequence {generic_decl} extends uvm_common::sequence_base#({agent.name}_config_sequence, {agent_seq_item});", file = file)
                print (f"\t`uvm_object_param_utils(uvm_{name}::{agent.name}_low_sequence{generic_assign})", file = file)
                print (f"", file = file)
                print (f"\trand int unsigned transaction_count;", file = file)
                print (f"\t//thing about constraints", file = file)
                print ("\tconstraint c_transactions {\n\t\ttransaction_count inside {[50:200]};\n\t};", file = file)
                print (f"", file = file)
                print (f"\tfunction new(string name = \"{agent.name}_low_sequence\");", file = file)
                print (f"\t\tsuper.new(name);", file = file)
                print (f"\tendfunction", file = file)
                print (f"", file = file)
                print (f"\ttask body();", file = file)
                print (f"\t\tint unsigned it;", file = file)
                print (f"\t\tuvm_common::fifo#({agent_seq_item}) fifo;", file = file)
                print (f"\t\tassert(uvm_config_db#(uvm_common::fifo#({agent_seq_item}))::get(m_sequencer , \"\" , \"fifo\",  fifo));", file = file)
                print (f"", file = file)
                print (f"\t\tit = 0;", file = file)
                print (f"\t\t// Somewhere get sequence item and parse it", file = file)
                print (f"\t\twhile (it < transaction_count) begin", file = file)
                print (f"\t\t\tfifo.get(req);", file = file)
                print (f"\t\t\tstart_item(req);", file = file)
                print (f"\t\t\t//`uvm_fatal(m_sequencer.get_full_name, \"\\n\\tYou have to implement conversion function!!\")", file = file)
                print (f"\t\t\t//assert(req.randomize()) with {{}};", file = file)
                print (f"\t\t\tfinish_item(req);", file = file)
                print (f"\t\t\tit++;", file = file)
                print (f"\t\tend", file = file)
                print (f"", file = file)
                print (f"\tendtask", file = file)
                print (f"endclass", file = file)

                # Create sequence library library
                print (f"", file = file)
                print (f"", file = file)
                print (f"class {agent.name}_low_sequence_lib {generic_decl} extends uvm_common::sequence_library#({agent.name}_config_sequence , {agent_seq_item});", file = file)
                print (f"\t`uvm_object_param_utils     (uvm_{name}::{agent.name}_low_sequence_lib{generic_assign})", file = file)
                print (f"\t`uvm_sequence_library_utils(uvm_{name}::{agent.name}_low_sequence_lib{generic_assign})", file = file)
                print (f"", file = file)
                print (f"\tfunction new(string name = \"uvm_{name}::{agent.name}_low_sequence_lib\");", file = file)
                print (f"\t\tsuper.new(name);", file = file)
                print (f"\t\tthis.add_sequence({agent.name}_low_sequence {generic_assign}::get_type());", file = file)
                print (f"\tendfunction", file = file)
                print (f"", file = file)
                print (f"\tvirtual function void init_sequence({agent.name}_config_sequence param_cfg = null);", file = file)
                print (f"\t\tuvm_common::sequence_library::init_sequence(param_cfg);", file = file)
                print (f"\tendfunction", file = file)
                print (f"endclass", file = file)

        with open(pkg_path / "sequence_item.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "sequence_item.sv"), file = file)
            print (f"class sequence_item{generic_decl} extends uvm_common::sequence_item;", file = file) 
            print (f"\t`uvm_object_param_utils(uvm_{name}::sequence_item{generic_assign})\n", file = file)
            print (f"", file = file)
            for item in self.items:
                print (f"\trand {item[0]} {item[1]} {item[2]};", file = file)
            print (f"", file = file)
            print (f"\tfunction new(string name = \"uvm_{name}::sequence_item\");", file = file)
            print (f"\t\tsuper.new(name);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction void do_copy(uvm_object rhs);", file = file)
            print (f"\t\tsequence_item{generic_assign} c_rhs;", file = file)
            print (f"", file = file)
            print (f"\t\tassert($cast(c_rhs, rhs));", file = file)
            print (f"\t\tsuper.do_copy(rhs);", file = file)
            for item in self.items:
                print (f"\t\t{item[1]} = c_rhs.{item[1]};", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction bit do_compare(uvm_object rhs,uvm_comparer comparer);", file = file)
            print (f"\t\tbit ret;", file = file)
            print (f"\t\tsequence_item{generic_assign} c_rhs;", file = file);
            print (f"", file = file)
            print (f"\t\tassert($cast(c_rhs, rhs));", file = file)
            print (f"\t\tret = super.do_compare(rhs, comparer);", file = file)
            for item in self.items:
                print (f"\t\tret &= ({item[1]} === c_rhs.{item[1]});", file = file)
            print (f"\t\treturn ret;", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction string convert2string();", file = file)
            print (f"\t\tstring ret = \"\";", file = file)
            print (f"\t\tret = this.time2string();", file = file)
            print (f"\t\t{self.convert2string}", file = file)
            print (f"\t\treturn ret;", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)

        with open(pkg_path / "config.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "config.sv"), file = file)
            print (f"", file = file)
            print (f"class config_sequence extends uvm_object;", file = file)
            print (f"\t`uvm_object_utils(uvm_{name}::config_sequence)", file = file)
            print (f"", file = file)
            print (f"\tfunction new (string name = \"uvm_{name}::config_sequence\");", file = file)
            print (f"\t\tsuper.new(name);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)
            print (f"", file = file)
            print (f"", file = file)
            print (f"class config_item extends uvm_object;", file = file)
            print (f"\tstring interface_name;", file = file)
            for cfg in self.config:
                print (f"\t{self.config[cfg]} {cfg};", file = file)
            print (f"", file = file)
            print (f"\tfunction new (string name = \"\");\n\t\tsuper.new(name);\n\tendfunction", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)

        with open(pkg_path / "monitor.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "monitor.sv"), file = file)
            print (f"class monitor{generic_decl} extends uvm_monitor;", file = file)
            print (f"\t`uvm_component_param_utils(uvm_{name}::monitor{generic_assign})", file = file)
            print (f"", file = file)
            print (f"\tuvm_analysis_port #(sequence_item{generic_assign}) analysis_port;", file = file)
            print (f"\tuvm_reset::sync_terminate reset_sync;", file = file);
            print (f"\t//fifo input", file = file)
            for block in self.blocks:
                f_string = "{prefix}uvm_tlm_analysis_fifo#({item}) {agent}_fifo{array};\n"
                ret_str  = block.cmd_inst2string(f_string, False, "\t", "")
                print (ret_str, file = file)
            print (f"", file = file)
            print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
            print (f"\t\tanalysis_port = new(\"analysis port\", this);\n", file = file)
            for block in self.blocks:
                f_string = "{prefix}{agent}_fifo{array} = new({br_left}\"{agent}_fifo\"{reg_array}{br_right}, this);\n"
                ret_str = block.cmd2string(f_string, False, "\t\t")
                print (ret_str, file = file)

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
            print (f"\t\tsequence_item{generic_assign} item;", file = file) 
            for block in self.blocks:
                f_string = "{prefix}{item} item_{agent}{array};\n"
                ret_str = block.cmd_inst2string(f_string, False, "\t\t", "")
                print (ret_str, file = file)

            print (f"\t\tforever begin", file = file)
            for block in self.blocks:
                f_string = "{prefix}{agent}_fifo{array}.get(item_{agent}{array});\n"
                ret_str = block.cmd2string(f_string, False, "\t\t\t")
                print (ret_str, file = file)
            print (f"\t\t\titem = sequence_item{generic_assign}::type_id::create(\"item\", this);", file = file)
            for block in self.blocks:
                f_string = "{prefix}item.time_array_add(item_{agent}{array}.start);\n"
                ret_str = block.cmd2string(f_string, False, "\t\t\t")
                print (ret_str, file = file)
            print (f"\t\t\t`uvm_fatal(this.get_type_name(), \"\\n\\tNo implementation. Please add some implementation\");", file = file)
            print (f"", file = file)
            print (f"\t\t\tanalysis_port.write(item);", file = file)
            print (f"\t\tend", file = file)
            print (f"\tendtask", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)

        with open(pkg_path / "driver.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "driver.sv"), file = file)
            print (f"class driver{generic_decl} extends uvm_driver#(sequence_item{generic_assign});", file = file)
            print (f"\t`uvm_component_param_utils(uvm_{name}::driver{generic_assign})", file = file)
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
                f_string = "{prefix}uvm_common::fifo#({item}) {agent}_fifo{array};\n"
                ret_str = block.cmd_inst2string(f_string, False, "\t\t", "")
                print (ret_str, file = file)
            print (f"", file = file)
            for block in self.blocks:
                f_string = "{prefix}assert(uvm_config_db#(uvm_common::fifo#({item}))::get(this, \"\", \"{agent}_fifo\"  ,  {agent}_fifo{array}));\n"
                ret_str = block.cmd2string(f_string, False, "\t\t")
                print (ret_str, file = file)

            print (f"", file = file)
            print (f"\t\tforever begin", file = file)
            print (f"", file = file)
            for block in self.blocks:
                f_string = "{prefix}{item} item_{agent}{array};\n"
                ret_str = block.cmd_inst2string(f_string, False, "\t\t\t", "")
                print (ret_str, file = file)
            print (f"", file = file)
            print (f"\t\t\tseq_item_port.get_next_item(req);", file = file)
            for block in self.blocks:
                f_string = "{prefix}item_{agent}{array} = {item}::type_id::create(\"item_{agent}\", this);\n"
                ret_str = block.cmd2string(f_string, False, "\t\t\t")
                print (ret_str, file = file)
            print (f"", file = file)
            print (f"\t\t\t`uvm_fatal(this.get_type_name(), \"\\n\\tNOT IMPLEMENTED!!!\");", file = file)
            print (f"", file = file)
            for block in self.blocks:
                f_string = "{prefix}{agent}_fifo{array}.push_back(item_{agent}{array});\n"
                ret_str = block.cmd2string(f_string, False, "\t\t\t")
                print (ret_str, file = file)
            print (f"\t\t\tseq_item_port.item_done();", file = file)
            print (f"\t\tend", file = file)
            print (f"\tendtask", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)


        with open(pkg_path / "sequencer.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "sequencer.sv"), file = file)
            print (f"class sequencer{generic_decl} extends uvm_sequencer#(sequence_item{generic_assign});", file = file)
            print (f"\t`uvm_component_param_utils(uvm_{name}::sequencer{generic_assign})", file = file)
            print (f"", file = file)
            print (f"\tuvm_reset::sync_terminate reset_sync;", file = file);
            print (f"", file = file)
            print (f"\tfunction new (string name, uvm_component parent = null);\n\t\tsuper.new(name, parent);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction void build_phase (uvm_phase phase);", file = file)
            print (f"\t\tsuper.build_phase(phase);", file = file)
            print (f"\t\treset_sync = new();", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)

        with open(pkg_path / "sequence.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "sequence.sv"), file = file)
            print (f"class sequence_base{generic_decl} extends uvm_common::sequence_base#(config_sequence, sequence_item{generic_assign});", file = file)
            print (f"\t`uvm_object_param_utils(uvm_{name}::sequence_base{generic_assign})", file = file)
            print (f"", file = file)
            print (f"\tint unsigned transaction_count_min = 10;", file = file)
            print (f"\tint unsigned transaction_count_max = 200;", file = file)
            print (f"\trand int unsigned transaction_count;", file = file)
            print ("\tconstraint c1 {transaction_count inside {[transaction_count_min : transaction_count_max]};}", file = file)
            print (f"", file = file)
            print (f"\tfunction new (string name);\n\t\tsuper.new(name);", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\ttask body ();", file = file)
            print (f"\t\tint unsigned it;", file = file)
            print (f"\t\tuvm_common::sequence_cfg state;", file = file)
            print (f"", file = file)
            print (f"\t\tif(!uvm_config_db#(uvm_common::sequence_cfg)::get(m_sequencer, \"\", \"state\", state)) begin", file = file)
            print (f"\t\t\tstate = null;", file = file)
            print (f"\t\tend", file = file)
            print (f"", file = file)
            print (f"\t\t`uvm_info(m_sequencer.get_full_name(), \"\\n\\tsequence_simple is running\", UVM_DEBUG);", file = file)
            print (f"", file = file)
            print (f"\t\tit = 0;", file = file)
            print (f"\t\twhile(it < transaction_count && (state == null || state.next())) begin", file = file)
            print (f"\t\t\treq = sequence_item{generic_assign}::type_id::create(\"req\", m_sequencer);", file = file)
            print (f"\t\t\tstart_item(req);", file = file)
            print (f"\t\t\tassert(req.randomize());", file = file)
            print (f"\t\t\tfinish_item(req);", file = file)
            print (f"\t\tend", file = file);
            print (f"\tendtask", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)
            print (f"", file = file)
            print (f"", file = file)
            print (f"/////////////////////////////////////////////////////////////////////////", file = file)
            print (f"// SEQUENCE LIBRARY", file = file)
            print (f"class sequence_lib{generic_decl}  extends uvm_common::sequence_library#(config_sequence, sequence_item{generic_assign});", file = file)
            print (f"\t`uvm_object_param_utils(uvm_{name}::sequence_lib{generic_assign})", file = file)
            print (f"\t`uvm_sequence_library_utils(uvm_{name}::sequence_lib{generic_assign})", file = file)
            print (f"", file = file)
            print (f"\tfunction new (string name);\n\t\tsuper.new(name);", file = file)
            print (f"\t\tinit_sequence_library();", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tvirtual function void init_sequence(config_sequence param_cfg = null);", file = file)
            print (f"\t\tuvm_common::sequence_library::init_sequence(param_cfg);", file = file)
            print (f"\t\tthis.add_sequence(sequence_base{generic_assign}::get_type());", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)

        with open(pkg_path / "env.sv", 'w') as file:
            print (uvm_gen_preambule.format(name = "env.sv"), file = file)
            print (f"class env_rx{generic_decl} extends uvm_env;", file = file)
            print (f"\t`uvm_component_param_utils(uvm_{name}::env_rx{generic_assign})", file = file)
            print (f"", file = file)
            print (f"\tuvm_analysis_port #(sequence_item{generic_assign}) analysis_port;", file = file)
            print (f"\tsequencer{generic_assign} m_sequencer;", file = file)
            print (f"\tuvm_reset::sync_cbs reset_sync;", file = file)
            print (f"", file = file)
            print (f"\tprotected monitor{generic_assign} m_monitor;", file = file)
            print (f"\tprotected driver{generic_assign}  m_driver;", file = file)
            print (f"", file = file)
            for block in self.blocks:
                f_string = ""
                f_string += "{prefix}protected {type_name} {agent}{array};\n"
                f_string += "{prefix}protected uvm_common::fifo#({item}) {agent}_fifo{array};\n"
                ret_str = block.cmd_inst2string(f_string, False, "\t", "")
                print (ret_str, file = file)
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
            print (self._gen_block_create(False, "\t\t\t"), file = file)
            print (f"", file = file)
            for block in self.blocks:
                f_string = ""
                f_string += "{prefix}{agent}_fifo{array} = uvm_common::fifo#({item})::type_id::create({br_left}\"{agent}_fifo\"{reg_array}{br_right}, this);\n"
                ret_str = block.cmd2string(f_string, False, "\t")
                print (ret_str, file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
            print (f"\t\tsuper.connect_phase(phase);", file = file)
            print (f"", file = file)
            print (f"\t\treset_sync.push_back(m_monitor.reset_sync);", file = file)
            print (f"\t\tif (m_config.active == UVM_ACTIVE) begin", file = file)
            print (f"\t\t\treset_sync.push_back(m_sequencer.reset_sync);", file = file)
            print (f"\t\t\treset_sync.push_back(m_driver.reset_sync);", file = file)
            print (f"\t\t\tm_driver.seq_item_port.connect(m_sequencer.seq_item_export);", file = file)
            print (f"\t\t\t// Connect lower agents monitor to hight level monitor", file = file)
            for block in self.blocks:
                f_string = ""
                f_string += "{prefix}uvm_config_db#(uvm_common::fifo#({item}))::set({agent}{array}.m_sequencer , \"\" , \"fifo\",  {agent}_fifo{array});\n"
                f_string += "{prefix}uvm_config_db#(uvm_common::fifo#({item}))::set(m_driver, \"\", \"{agent}_fifo\",  {agent}_fifo{array});\n"
                ret_str = block.cmd2string(f_string, False, "\t\t\t")
                print (ret_str, file = file)

            print (f"\t\tend", file = file)
            print(self._gen_block_reset_connect("\t\t"), file = file)
            print (f"", file = file)
            print (f"\t\tanalysis_port = m_monitor.analysis_port;", file = file)
            for block in self.blocks:
                f_string = ""
                f_string += "{prefix}{agent}{array}.{analysis_port}.connect(m_monitor.{agent}_fifo{array}.analysis_export);\n"
                ret_str = block.cmd2string(f_string, False, "\t\t")
                print (ret_str, file = file)
            print (f"\t\t// connect driver and low level sequence", file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\ttask run_phase (uvm_phase phase);", file = file)
            print (f"\t\tif (m_config.active == UVM_ACTIVE) begin", file = file)
            for block in self.blocks:
                # Generic assign is from top component!
                f_string = ""
                f_string += "{prefix}fork\n"
                f_string += "{prefix}\tforever begin\n"
                f_string += "{prefix}\t\t{agent}_low_sequence_lib" + f"{generic_assign}" + "{prefix}\t{agent}_low_seq;\n"
                f_string += "{prefix}\t\t{agent}_low_seq = {agent}_low_sequence_lib" f"{generic_assign}" + "{prefix}\t::type_id::create(\"{agent}_low_seq\", this);\n"
                f_string += "{prefix}\t\tassert({agent}_low_seq.randomize()) else begin `uvm_fatal(this.get_full_name(), \"\\n\\tCannot randomize {agent}_low_seq\"); end\n"
                f_string += "{prefix}\t\t{agent}_low_seq.start({agent}{array}.m_sequencer);\n"
                f_string += "{prefix}\tend\n"
                f_string += "{prefix}join_none\n"
                f_string += "{prefix}#(0); // Run first fork then continue\n"
                ret_str = block.cmd2string(f_string, False, "\t\t\t")
                print (ret_str, file = file)

            print (f"\t\tend", file = file)
            print (f"", file = file)
            print (f"\t\tsuper.run_phase(phase);", file = file)
            print (f"\tendtask", file = file)
            print (f"endclass", file = file)

            ####################
            ## ETH_TX
            print (f"", file = file)
            print (f"", file = file)
            print (f"class env_tx{generic_decl} extends uvm_env;", file = file)
            print (f"\t`uvm_component_param_utils(uvm_{name}::env_tx{generic_assign})", file = file)
            print (f"", file = file)
            print (f"\tuvm_analysis_port #(sequence_item{generic_assign}) analysis_port;", file = file)
            #print (f"\tsequencer{generic_assign} m_sequencer;", file = file)
            print (f"\tuvm_reset::sync_cbs reset_sync;", file = file)
            print (f"", file = file)
            print (f"\tprotected monitor{generic_assign} m_monitor;", file = file)
            #print (f"\tprotected driver{generic_assign}  m_driver;", file = file)
            print (f"", file = file)
            for block in self.blocks:
                f_string = ""
                f_string += "{prefix}protected {type_name} {agent}{array};\n"
                ret_str = block.cmd_inst2string(f_string, True, "\t", "")
                print (ret_str, file = file)

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
            print (self._gen_block_create(True, "\t\t\t"), file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"\tfunction void connect_phase (uvm_phase phase);", file = file)
            print (f"\t\tsuper.connect_phase(phase);", file = file)
            print (f"", file = file)
            print (f"\t\treset_sync.push_back(m_monitor.reset_sync);", file = file)
            print(self._gen_block_reset_connect("\t\t"), file = file)

            print (f"", file = file)
            print (f"\t\tanalysis_port = m_monitor.analysis_port;", file = file)
            for block in self.blocks:
                f_string = ""
                f_string += "{prefix}{agent}{array}.{analysis_port}.connect(m_monitor.{agent}_fifo{array}.analysis_export);\n"
                ret_str = block.cmd2string(f_string, True, "\t\t")
                print (ret_str, file = file)
            print (f"\tendfunction", file = file)
            print (f"", file = file)
            print (f"endclass", file = file)


    def module_path(self, name):
        return f"lappend MOD \"$ENTITY_BASE/tbench/{name}/pkg.sv\""

