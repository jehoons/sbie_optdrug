# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import numpy
from os.path import exists
from sbie_optdrug.result.tab_s6 import program
from ipdb import set_trace


def check_outputs(config):

    exist_list = [exists(config['output'][key]) for key \
        in config['output'] ]

    return numpy.product(exist_list)


def test(with_small, force):

    default_config = program.getconfig()

    if not check_outputs(default_config) or force:
        program.run(default_config)

    assert check_outputs(default_config)


def test_1():


    from sbie_optdrug.dataset import ccle

    # set_trace()
