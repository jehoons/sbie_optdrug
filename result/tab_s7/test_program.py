# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import numpy
from os.path import exists
from sbie_optdrug.result.tab_s7 import program
from ipdb import set_trace
from boolean3_addon import attr_cy
import json

# def test_hello(with_small, force):
#     text='''
#     A=Random
#     B=Random
#     C=Random
#     A*= A or C
#     B*= A and C
#     C*= not A or B
#     '''
#     attr_cy.build(text)
#     res = attr_cy.run(samples=100, steps=30, debug=False)
#     json.dump(res, open('output.json', 'w'), indent=4)


def check_outputs(config):

    exist_list = [exists(config['output'][key]) for key \
        in config['output'] ]

    return numpy.product(exist_list)


# def test_this(with_small, force):

#     default_config = program.getconfig()

#     # if not check_outputs(default_config) or force:
#     #     program.run(default_config)

#     # assert check_outputs(default_config)

#     program.run(default_config)

def test_this(with_small, force):
    default_config = program.getconfig()
    
    program.run_step1(default_config)
    
    program.run_step2(default_config)
    
    program.run_step2_plot(default_config)

