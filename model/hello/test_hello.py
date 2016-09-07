from ipdb import set_trace
from boolean2 import Model

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

model.iterate( steps=10, repeat=1)

for state in model.states:
    print state.A, state.B, state.C

# set_trace()
