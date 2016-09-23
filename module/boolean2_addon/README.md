# boolean2_addon 

## example of `attractor` module 

```python 
import sbie_optdrug
import json
from pdb import set_trace
from boolean2 import Model
from boolean2_addon import attractor


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
    res = attractor.find_attractors(model=model, steps=100, sample_size=10)

    outputfile = 'output.json'
    json.dump(res, open(outputfile, 'w'), indent=1)

```

