#!/bin/python3

import argparse
import os
import pathlib
import xml.etree.ElementTree as xml_tree

#import logic_vector_array
#import logic_vector
import uvm_gen



def parse_tree(file, output):
    tree = xml_tree.parse(file)
    generator = uvm_gen.uvm_gen(tree)
    generator.gen_pkg(output)
    #generator.testbench()
    #generator.env()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate UVM testbench from XML description',
        epilog="This is only prototype it can contains some bugs")
    parser.add_argument('--file', required=True, help='xml file with testbench description')
    parser.add_argument('--out',  required=False, help='output directory where will be uvm environmen generated', default="uvm")
    args = parser.parse_args()

    #xml_file = "test_3.xml"
    print (f"parse file {args.file}")
    print (f"generate output to {args.out}")
    parse_tree(args.file, pathlib.Path(args.out))

