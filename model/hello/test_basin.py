# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import json
from ipdb import set_trace
from sbie_optdrug.boolean2 import Model
from sbie_optdrug.analysis import boolnet


def test_compute_basin():

    text = """
    A = Random
    B = Random
    C = Random
    D = Random

    A *= D or C
    B *= A
    C *= B or D
    D *= B
    """

    model = Model( text=text, mode='sync')
    res = boolnet.find_attractors(model=model, sample_size=10000)
    
    print (res)

    outputfile = 'output.json'

    json.dump(res, open(outputfile, 'w'), indent=1)

    # set_trace()