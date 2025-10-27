#!/bin/python3


class uvm_dut:
    
    """
        This class represent instantionation of DUT 
    """

    def __init__(self, xml):
        # load generic
        self.generics = {}
        for generic in xml.find('generics'):
            self.generics[generic.tag] = generic.text

        # load copnfig
        self.ports = {}
        for port in xml.find('ports'):
            self.ports[port.tag] = port.get('port')

        # load interface name
        self.name   = xml.get("name")
        self.entity = xml.get("entity")

    def generic2string(self):
        if (len(self.generics) == 0):
            return ""

        generic = ""
        sep     = "\n\t\t"
        for it in self.generics:
            generic += f"{sep} .{it} ({self.generics[it]})"
            sep = ",\n\t\t"
        return f"#({generic}\n\t)"

    def type2string(self):
        return f"{self.entity}"

    def inst2string(self, name):
        ret = "\t";
        ret += self.type2string() + " ";
        ret += self.generic2string();
        ret += f"\n\t{self.name} ("

        sep     = "\n\t\t"
        for it in self.ports:
            ret +=  f"{sep} .{it} ({self.ports[it]})"
            sep = ",\n\t\t"

        ret += "\n\t);\n"
        return ret 

