import json
from boolean2 import Model
from pyhet.analysis import find_attractors
from ipdb import set_trace

def test_compute_basin():

    text = """
    A = Random
    B = Random
    C = Random
    D = Random
    E = Random

    A* = B or C and D
    B* = A or C and D or E
    C* = A or (C and E) or B
    D* = (A or B) and (D or E)
    E* = A or (C and D)
    """

    model = Model( text=text, mode='sync')
    res = find_attractors(model=model, steps=60, sample_size=100)
    # print res

    outputfile = 'output1.json'
    json.dump(res, open(outputfile, 'w'), indent=1)

    # model.

    #set_trace()