#!/bin/python3

#from .constant import *

from enum import Enum
import re

# class syntax
class agent_dir(Enum):
    RX = 1
    TX = 2
    NONE = 3

def agent_dir_get(origin, revert):
    if (revert == False):
        return origin
    else:
        if (origin == agent_dir.RX):
            return agent_dir.TX
        elif(origin == agent_dir.TX):
            return agent_dir.TX
        else:
            return agent_dir.NONE

def str2agent_dir(direction):
    if (direction == None):
        return agent_dir.NONE

    if (direction == "RX"):
        return agent_dir.RX
    elif (direction == "TX"):
        return agent_dir.TX
    else:
        return agent_dir.NONE


def cfg_substitute(cfg, subs):
    new_cfg = {}
    for it in subs:
        new_item = subs[it]
        for jt in cfg:
            new_item = re.sub(f"\\b{jt}\\b", f"({cfg[jt]})", new_item)
        new_cfg[it] = new_item
    return new_cfg

