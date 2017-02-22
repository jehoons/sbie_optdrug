# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import json
from pdb import set_trace
import sys 
from os.path import join, exists

import sbie_optdrug
from boolean2 import Model
from boolean2_addon import attractor 


def test_compute_basin():

    # text = """
    # A = Random
    # B = Random
    # C = Random
    # D = Random

    # A *= D or C
    # B *= A
    # C *= B or D
    # D *= B
    # """

    text = """
    A = Random
    B = Random
    C = Random
    
    B*= A
    C*= B 
    A*= not C
    """

    model = Model( text=text, mode='sync')
    res = attractor.find_attractors(model=model, sample_size=1000)
    
    outputfile = 'test_basin_result.json'

    json.dump(res, open(outputfile, 'w'), indent=1)

    assert exists(outputfile)

    # set_trace()

