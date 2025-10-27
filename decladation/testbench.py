#!/bin/python3

import os

from .block    import block

from . import files
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
        self.files_sv.append("sequence.sv");

    def create(self, xml):
        return instantiation.uvm_env_top(xml)

    def gen_pkg(self, path, name):
        super().gen_pkg(path, "env_top")

        pkg_path = path / "env_top"

        generic_decl   = self._generic_decl();
        generic_assign = self._generic_assign();

        #Generate sequence.sv
        sequence = files.sv.virt_sequence()
        with open(pkg_path / f"{sequence.name_get()}.sv", 'w') as file:
            sequence.generate(file, self.blocks, (generic_decl, generic_assign))

        sequencer = files.sv.virt_sequencer()
        with open(pkg_path / f"{sequencer.name_get()}.sv", 'w') as file:
            sequencer.generate(file, self.blocks, (generic_decl, generic_assign))

        config = files.sv.config("env_top")
        with open(pkg_path / f"{config.name_get()}.sv", 'w') as file:
            config.generate(file, self.blocks, (generic_decl, generic_assign))

        # Generate env.sv
        env = files.sv.top_env()
        with open(pkg_path / f"{env.name_get()}.sv", 'w') as file:
            env.generate(file, self.blocks, (generic_decl, generic_assign))

        model = files.sv.model()
        with open(pkg_path / f"{model.name_get()}.sv", 'w') as file:
            model.generate(file, self.blocks, (generic_decl, generic_assign))

        scoreboard = files.sv.scoreboard()
        with open(pkg_path / f"{scoreboard.name_get()}.sv", 'w') as file:
            scoreboard.generate(file, self.blocks, (generic_decl, generic_assign))

        testbench = files.sv.testbench(self.dut)
        with open(path / f"{testbench.name_get()}.sv", 'w') as file:
            testbench.generate(file, self.blocks, (generic_decl, generic_assign))

        generic_pkg = files.sv.pkg("generic_pkg")
        for generic in self.generics:
            generic_pkg.add_parameter(generic, self.generics[generic]["value"], self.generics[generic]["type"]);
        generic_pkg.add_parameter("CLK_PERIOD", "4ns", "time");
        with open(path / f"{generic_pkg.name_get()}.sv", 'w') as file:
            generic_pkg.generate(file, self.blocks, (generic_decl, generic_assign))

        # Create test
        test_path = path / "test"
        if not test_path.exists():
            os.makedirs(test_path)

        test_pkg = files.sv.pkg("test")
        test_pkg.add_file(f"base.sv");
        with open(test_path / f"pkg.sv", 'w') as file:
            test_pkg.generate(file, self.blocks, (generic_decl, generic_assign))

        test = files.sv.test("base")
        with open(test_path / f"{test.name_get()}.sv", 'w') as file:
            test.generate(file, self.blocks, (generic_decl, generic_assign))


