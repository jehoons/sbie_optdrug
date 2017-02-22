# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import pickle 
from pdb import set_trace
from boolean2 import Model


def test_hello():

    text = """
    # initial values
    A = True
    B = Random
    C = Random

    # updating rules
    B* = A
    C* = B
    """


    text = """
    A = False
    B = False
    C = False
    
    B*= A
    C*= B 
    A*= not C
    """


    model = Model( text=text, mode='sync')

    model.initialize()

    model.iterate( steps=10, repeat=1)

    for state in model.states:
        print (state.A, state.B, state.C)

    with open('test_hello_result.pkl','w') as fobj: 
        pickle.dump(model.states, fobj)


