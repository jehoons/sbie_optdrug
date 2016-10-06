# BooleanSim

### INSTALL 
```
git clone git@github.com:jehoons/BooleanSim.git
cd BooleanSim 
python setup.py install 
```

### ORIGINAL CODE
Original code of `boolean2` module is developed by Albert. Original code can be downloaded by following command:

```
git clone https://github.com/ialbert/booleannet.git
```

As original code is excuted only from `python2`, I translated the code by using `2to3.py` and updated version of `ply`. 

Ply can be downloaded from following link:

http://www.dabeaz.com/ply/

### TEST

Test code: 
```python
import pickle 
from pdb import set_trace
from boolean3 import Model

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
    model = Model( text=text, mode='sync')
    model.initialize()
    model.iterate( steps=10, repeat=1)
    
    for state in model.states:
        print (state.A, state.B, state.C)
```
