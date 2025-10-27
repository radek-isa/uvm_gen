#!/bin/python3

import os

from .block    import block
from .constant import uvm_gen_preambule

from . import files
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
            low_sequence = files.sv.low_sequence(name, agent)
            with open(pkg_path / f"{low_sequence.name_get()}.sv", 'w') as file:
                low_sequence.generate(file, (generic_decl, generic_assign))

        sequence_item = files.sv.sequence_item(name, self.items, self.convert2string)
        with open(pkg_path / f"{sequence_item.name_get()}.sv", 'w') as file:
            sequence_item.generate(file, (generic_decl, generic_assign))

        config = files.sv.config(name, self.config)
        with open(pkg_path / f"{config.name_get()}.sv", 'w') as file:
            config.generate(file, None, (generic_decl, generic_assign))

        monitor = files.sv.monitor(name, self.blocks)
        with open(pkg_path / f"{monitor.name_get()}.sv", 'w') as file:
            monitor.generate(file, (generic_decl, generic_assign))

        driver = files.sv.driver(name, self.blocks)
        with open(pkg_path / f"{driver.name_get()}.sv", 'w') as file:
            driver.generate(file, (generic_decl, generic_assign))

        sequencer = files.sv.sequencer(name)
        with open(pkg_path / f"{sequencer.name_get()}.sv", 'w') as file:
            sequencer.generate(file, (generic_decl, generic_assign))

        sequence = files.sv.sequence(name)
        with open(pkg_path / f"{sequence.name_get()}.sv", 'w') as file:
            sequence.generate(file, (generic_decl, generic_assign))

        env = files.sv.env(name, self.blocks)
        with open(pkg_path / f"{env.name_get()}.sv", 'w') as file:
            env.generate(file, (generic_decl, generic_assign))

    def module_path(self, name):
        return f"lappend MOD \"$ENTITY_BASE/tbench/{name}/pkg.sv\""

