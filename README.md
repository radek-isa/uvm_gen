# uvm_gen

This is my simple generator of uvm environment from {XML} description. This should
speed up creating UVM environment for components. As you known
UVM is complicated and a very chatty methodology. This should save you
a lot of work. Generator use environments created in
project [ndk-fpga](https://github.com/CESNET/ndk-fpga/tree/devel/comp/uvm).

# Example

All examples is in directory ./tests
Run simple examle:

    `./main.py --file tests/gen_loop_switch.xml --out=uvm`

# Supported feature

- [x] generics
- [x] array
- [x] creating UVC
- [x] creating scoreboard
- [x] creating core of model
- [x] connect DUT


# key words

- testbench
- generics
- envs
- new
- sequence_item
- convert2string
- config
- agents
- for
- active
- dut
    - generics
    - ports

