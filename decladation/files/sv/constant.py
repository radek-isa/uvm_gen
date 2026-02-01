
from datetime import datetime


uvm_preambule = """// {name}: uvm verification testbench
// Copyright (C) {cfg.year} CESNET z. s. p. o.
// Author:   {cfg.author_name} <{cfg.author_email}>

// SPDX-License-Identifier: BSD-3-Clause

"""

def uvm_gen_preambule(file_name, cfg):
    return uvm_preambule.format(name = file_name, cfg = cfg)

