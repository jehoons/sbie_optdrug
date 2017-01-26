# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.jehoon@gmail.com>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import numpy
from os.path import exists
from sbie_optdrug.result.tab_s4 import program
from pdb import set_trace

def test(with_small, force):

    default_config = program.getconfig()

    if not exists(default_config['output']['a']) or force:
        program.run_step1(default_config)

    if not exists(default_config['output']['b']) or force:
        program.run_step2(default_config)

    if not exists(default_config['output']['c']) or force:
        program.run_step3(default_config)

    if not exists(default_config['output']['d']) or force:
        program.run_step4(default_config)
