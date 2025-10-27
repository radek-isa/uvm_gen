#!/bin/python3


class block_for:
    
    """
        This class represent instantionation of uvm_logic_vector_array_mfb. 
    """

    def __init__(self, xml, decl_agents):
        # load generic
        self.iterator = xml.get("iterator")
        self.end      = xml.get("end")
        self.blocks = []

        for block in xml:
            match block.tag:
                case "for":
                    block_for = instantiation.block_for(block, decl_agents)
                    self.blocks.append(block_for)
                case _:
                    agent_name  = block.get("name")
                    agent_dir   = block.get("dir")
                    agent_class = decl_agents[block.tag].create(block)
                    self.blocks.append(agent_class);

    def lambda2string(self, lambda_fce, lambda_param):
        ret_str = ""
        lambda_param.array.append((self.iterator, self.end))
        for block in self.blocks:
            ret_str +=  block.lambda2string(lambda_fce, lambda_param);
        return ret_str;


    def generic2string(self):
        return f""

    def type2string(self, direction):
        return f"//for loop "

    def reset2string(self, f_string, prefix, array):
        new_array  = f"{array}[{self.iterator}]"

        ret_str = ""
        ret_str += f"{prefix}for (int unsigned {self.iterator} = 0; {self.iterator} < {self.end};  {self.iterator}++) begin\n"
        for block in self.blocks:
            ret_str +=  block.reset2string(f_string, prefix + "\t", new_array);
        ret_str += f"{prefix}end"
        return ret_str;

    def agents_get(self, agents):
        for block in self.blocks:
            block.agents_get(agents)

    def interfaces2inst(self, cfg, f_string, name, array, clk):
        ret = [];
        for it in self.blocks:
            ret += it.interfaces2inst(cfg, f_string, name, array + f"[{self.end}]", clk)
        return ret;

    def interfaces2cmd(self, cfg, f_string, prefix, reg_name, name, array):
        ret = ""
        ret += f"{prefix}for (int unsigned {self.iterator} = 0; {self.iterator} < {self.end};  {self.iterator}++) begin\n"
        reg_name = reg_name + f", $sformatf(\"_%0d\", {self.iterator})"
        for it in self.blocks:
            ret += it.interfaces2cmd(cfg, f_string, prefix + "\t", reg_name, name, array + f"[{self.iterator}]");
        ret += f"{prefix}end"
        return ret


