#!/bin/python3

import os

import instantiation
from . import files

class block:
    """
        This class is base class for block like uvm_env and testbench
    """

    def __init__(self, xml, decl_agents):
        self.xml_tree  = xml

        # load generic
        self.generics = {}
        generics = xml.find('generics')
        if (generics != None):
            for generic in generics:
                value = generic.get("value").strip() if generic.get("value") != None else ""
                self.generics[generic.tag] = {"type" : generic.get("type"), "value" : value}

        # load config
        self.config = {}
        configs = xml.find('config')
        if (configs != None):
            for config in configs:
                self.config[config.tag] = config.get("type");

        # load agents
        self.blocks  = []
        for block in xml.find('agents'):
            match block.tag:
                case "for":
                    block_for = instantiation.block_for(block, decl_agents)
                    self.blocks.append(block_for)
                case _:
                    agent_name  = block.get("name")
                    agent_dir   = block.get("dir")
                    agent_class = decl_agents[block.tag].create(block)
                    self.blocks.append(agent_class);

        # load agents
        self.files_sv  = []

    def create(self, xml):
        raise Exception("Sorry this is not defined")
        return None

    def agents_get(self, agents):
        for block in self.blocks:
            block.agents_get(agents)

    def _generic_decl(self):
        #create generic string
        generic_decl   = ""
        sep = "\n\t\t"
        for generic in self.xml_tree.find('generics'):
            gen_name = generic.tag
            gen_type = generic.get("type");
            generic_decl   = generic_decl   + f"{sep}{gen_type} {gen_name}";
            sep = ",\n\t\t"

        if generic_decl != "":
            generic_decl   = "#(" + generic_decl   + "\n\t)"

        return generic_decl

    def _generic_assign(self):
        #create generic string
        generic_assign = ""
        sep = "\n\t\t"
        for generic in self.xml_tree.find('generics'):
            gen_name = generic.tag
            gen_type = generic.get("type");
            generic_assign = generic_assign + f"{sep}.{gen_name} ({gen_name})";
            sep = ",\n\t\t"

        if generic_assign != "":
            generic_assign = "#(" + generic_assign + "\n\t)"

        return generic_assign

    def gen_pkg(self, path, name):
        pkg_path = path / name
        print(f"uvm_env {name} {path}")

        # Create directory
        if not pkg_path.exists():
            os.makedirs(pkg_path)

        with open(pkg_path / "pkg.sv", 'w') as file:
            print (files.sv.constant.uvm_gen_preambule.format(name = "pkg.sv"), file = file)
            print (f"package uvm_{name};", file = file)
            print (f"", file = file);
            print (f"\timport uvm_pkg::*;", file = file)
            print (f"\t`include \"uvm_macros.svh\"", file = file);
            print (f"", file = file);
            for sv in self.files_sv:
                print (f"\t`include \"{sv}\"", file = file);
            print (f"endpackage", file = file);



    def module_path(self, name):
        return ""

