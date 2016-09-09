# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from pdb import set_trace
from sbie_optdrug.boolean2 import Model
import pickle 


def test_hello():

    text = """
    # initial values
    A = Random
    B = Random
    C = Random

    # updating rules
    A* = A and C
    B* = A and B
    C* = not A
    """

    model = Model( text=text, mode='sync')

    model.initialize()

    model.iterate( steps=5, repeat=1)

    for state in model.states:
        print (state.A, state.B, state.C)

    with open('test_hello_result.pkl','w') as fobj: 
        pickle.dump(model.states, fobj)

    # set_trace()