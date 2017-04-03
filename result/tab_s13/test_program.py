# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import numpy
from os.path import exists
from sbie_optdrug.result.tab_s13 import program
from ipdb import set_trace
import json

#from pyexcel-xlsx import get_data

def check_outputs(config):

    exist_list = [exists(config['output'][key]) for key \
        in config['output'] ]

    return numpy.product(exist_list)


def test(with_small, force):

    default_config = program.getconfig()

    if not check_outputs(default_config) or force:
        program.run(default_config)

    assert check_outputs(default_config)

#def test_a(with_small, force):

    #if not check_outputs(default_config) or force:
        #program.run_a(config=default_config, force=force)

    #assert check_outputs(default_config)

#def test_b(with_small, force):
    #program.run_b(config=default_config, force=force)

#def test_c(with_small, force):
    #program.run_c(config=default_config, force=force)
