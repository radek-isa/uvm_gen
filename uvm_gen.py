#!/bin/python3


import pathlib
import os

import decladation

#from enum import Enum
#
#class direction(Enum):
#    NORMAL  = 1
#    REVERSE = 2


class uvm_gen:
    """
        This class should generate uvm verification environment from XML description file.
        For run verification is required ndk-fpga from CESNET. This program is not for 
        automatic generation. This program servers for generating first implementation (prototype)
        of verification environment.
    """

    def __init__(self, xml):
        self.xml_tree  = xml
        xml_root = self.xml_tree.getroot()

        # Divide Instantiation of agents and creation of new agents (DON'T Forget)

        # agents definitions
        self.agents    = {}
        # base environments
        # what if someohne put reset agent to new environment
        self.agents["reset"]                  = decladation.uvm_reset();
        self.agents["logic_vector_array_mfb"] = decladation.uvm_logic_vector_array_mfb();
        self.agents["logic_vector_mvb"]       = decladation.uvm_logic_vector_mvb();
        #create new environment
        for env_new in xml_root.findall('envs/new'):
            self.agents[env_new.get("name")] = decladation.uvm_env(env_new, self.agents);

        #create top level environment
        self.testbench   = decladation.uvm_testbench(xml_root, self.agents);

    def gen_pkg(self, path = pathlib.Path("./uvm")):
        firmware_path = "../../../"

        # Create directory
        if not path.exists():
            os.makedirs(path)

        # Generate package
        tbench_path = path / "tbench"
        if not tbench_path.exists():
            os.makedirs(tbench_path)

        for gen in self.agents:
            self.agents[gen].gen_pkg(tbench_path, gen)

        self.testbench.gen_pkg(tbench_path, "testbench.sv")
        #generate top_level.fdo and Modules.tcl
        with open(path / "Modules.tcl", 'w') as file:
            print (f"# Modules.tcl: Components include script", file = file)
            print (f"# Copyright (C) 2025 CESNET z. s. p. o.", file = file)
            print (f"# Author(s): Radek Iša <isa@cesnet.cz>", file = file)
            print (f"#", file = file)
            print (f"# SPDX-License-Identifier: BSD-3-Clause", file = file)
            print (f"", file = file)
            print (f"set SV_UVM_BASE \"$OFM_PATH/comp/uvm\"", file = file)
            print (f"", file = file)
            #add agents
            for it in self.agents:
                agent_path = self.agents[it].module_path(it)
                print (f"{agent_path}", file = file)

            print (f"", file = file)
            print (f"lappend MOD \"$ENTITY_BASE/tbench/env_top/pkg.sv\"", file = file)
            print (f"lappend MOD \"$ENTITY_BASE/tbench/test/pkg.sv\"", file = file)
            print (f"lappend MOD \"$ENTITY_BASE/tbench/generic_pkg.sv\"", file = file)
            print (f"lappend MOD \"$ENTITY_BASE/tbench/testbench.sv\"", file = file)
            print (f"", file = file)


        with open(path / "top_level.fdo", 'w') as file:
            print (f"# Modules.tcl: Components include script", file = file)
            print (f"# Copyright (C) 2025 CESNET z. s. p. o.", file = file)
            print (f"# Author(s): Mikuláš Brázda <xbrazd21@vutbr.cz>", file = file)
            print (f"#", file = file)
            print (f"# SPDX-License-Identifier: BSD-3-Clause", file = file)
            print (f"", file = file)
            print (f"set FIRMWARE_BASE \"{firmware_path}\"", file = file)
            print (f"set TB_FILE \"./tbench/testbench.sv\"", file = file)
            print (f"", file = file)
            print (f"set COMPONENTS [list \\", file = file)
            print (f"\t[list \"DUT\"      \"..\" \"FULL\"]\\", file = file)
            print (f"\t[list \"DUT_UVM\"  \".\"  \"FULL\"]\\", file = file)
            print (f"]", file = file)
            print (f"", file = file)
            print (f"set SIM_FLAGS(CODE_COVERAGE) false", file = file)
            print (f"set SIM_FLAGS(UVM_ENABLE) true", file = file)
            print (f"set SIM_FLAGS(UVM_TEST) \"test::base\"", file = file)
            print (f"set SIM_FLAGS(UVM_VERBOSITY) \"UVM_NONE\"", file = file)
            print (f"set SIM_FLAGS(DEBUG) false", file = file)
            print (f"", file = file)
            print (f"# Global include file for compilation", file = file)
            print (f"source \"$FIRMWARE_BASE/build/Modelsim.inc.fdo\"", file = file)
            print (f"", file = file)
            print (f"puts \"Numeric_std Warnings - Disabled\"", file = file)
            print (f"set NumericStdNoWarnings 1", file = file)
            print (f"", file = file)
            print (f"#Run simulation", file = file)
            print (f"nb_sim_run", file = file)
            print (f"", file = file)



