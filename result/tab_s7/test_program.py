# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.jehoon@gmail.com>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import numpy
from os.path import exists
from sbie_optdrug.result.tab_s7 import program
from ipdb import set_trace
from boolean3_addon import attr_cy
import json

default_config = program.getconfig()

def check_outputs(config):

    exist_list = [exists(config['output'][key]) for key \
        in config['output'] ]

    return numpy.product(exist_list)

def test_1(with_small, force):
    
    program.run_a(config=default_config, force=force)
    
def test_2(with_small, force):

    program.run_b(config=default_config, force=force)
    
def test_3(with_small, force):

    program.run_b_plot(config=default_config, force=force)
    
def test_4(with_small, force):

    program.run_c(config=default_config, force=force)    

def test_5(with_small, force):

    program.run_d(config=default_config, force=force)


# def test_this(with_small, force):
    # default_config = program.getconfig()
    # if not check_outputs(default_config) or force:
    #     program.run(default_config)
    # assert check_outputs(default_config)
    # program.run(default_config)
    