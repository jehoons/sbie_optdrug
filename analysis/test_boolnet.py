# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from pdb import set_trace
from sbie_optdrug.boolean2 import Model
from sbie_optdrug.analysis import boolnet


def test_find_attractors():

    # text = """
    # A = Random
    # B = Random
    # C = Random
    # D = Random
    #
    # A *= D or C
    # B *= A
    # C *= B or D
    # D *= B
    # """

    # Random sampling of initial conditions
    #
    # If A is set to False, a steady state is obtained.
    #
    #
    # text = """
    # A = True
    # B = Random
    # C = Random
    # D = Random
    #
    # B* = A or C
    # C* = A and not D
    # D* = B and C
    # """

    text = """
    A = True
    B = Random
    C = Random
    D = Random

    B* = A or C
    C* = A and not D
    D* = B and C
    """

    model = Model( text=text, mode='sync')
    res = boolnet.find_attractors(model=model, steps=100, sample_size=100000)

    outputfile = 'output.json'
    json.dump(res, open(outputfile, 'w'), indent=1)

