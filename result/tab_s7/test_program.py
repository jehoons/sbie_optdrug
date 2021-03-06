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

def test_a(with_small, force):
    program.run_a(config=default_config, force=force)

def test_b(with_small, force):
    program.run_b(config=default_config, force=force)

def test_b_plot(with_small, force):
    program.run_b_plot(config=default_config, force=force)

def test_c(with_small, force):
    program.run_c(config=default_config, force=force)

def test_d(with_small, force):
    program.run_d(config=default_config, force=force)

def test_e(with_small, force):
    program.run_e(config=default_config, force=force)

def test_f(with_small, force):
    program.run_f(config=default_config, force=force)

def test_g(with_small, force):
    program.run_g(config=default_config, force=force)
