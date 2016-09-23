### hello

여기서는 `boolean2` 패키지를 이용해서 boolean network를 어떻게 시뮬레이션 할수 있는지를 소개한다. 

test_hello.py 의 코드는 아래에와 같다: 

```python
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

```

이 코드를 실행하면, 아래와 같은 출력을 줄것이다. 

```
(False, False, True)
(False, False, True)
(False, False, True)
(False, False, True)
(False, False, True)
(False, False, True)
```

또한 이 코드는 pickle을 사용한 바이너리 출력을 한다. 

