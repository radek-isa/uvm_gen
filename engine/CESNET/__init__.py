#!/bin/python3

from . import decladation
from . import instantiation

#class CESNET:
    #def __init__(self):
    #    super().__init__();

def init():
    agents = {}
    agents["reset"]                  = decladation.uvm_reset();
    agents["logic_vector_array_mfb"] = decladation.uvm_logic_vector_array_mfb();
    agents["logic_vector_mvb"]       = decladation.uvm_logic_vector_mvb();

    return agents

