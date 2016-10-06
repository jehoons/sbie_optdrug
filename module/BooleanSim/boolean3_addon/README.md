# boolean2_addon 

## Requirement

This module is a kind of addon for the boolean simulator developed by Albert. Therefore, `booleannet` package should be installed as follwong:

```bash 
git clone https://github.com/ialbert/booleannet.git
```

## Example

example of find_attractor function in `attractor` module is shown as follows: 

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

The `find_attractors` function returns dictionary object as follows: 

```json
{
 "basin_of_attraction": {
  "b6ead8fadc6fe8c7b625": 6
 }, 
 "attractors": {
  "1": {
   "index": 0, 
   "attractor": "b6ead8fadc6fe8c7b625", 
   "trajectory": [
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1
   ], 
   "initial": 1, 
   "type": "cyclic", 
   "size": 4
  }, 
  "0": {
   "index": 0, 
   "attractor": "b6ead8fadc6fe8c7b625", 
   "trajectory": [
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0
   ], 
   "initial": 0, 
   "type": "cyclic", 
   "size": 4
  }, 
  "3": {
   "index": 0, 
   "attractor": "b6ead8fadc6fe8c7b625", 
   "trajectory": [
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3
   ], 
   "initial": 3, 
   "type": "cyclic", 
   "size": 4
  }, 
  "2": {
   "index": 0, 
   "attractor": "b6ead8fadc6fe8c7b625", 
   "trajectory": [
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2
   ], 
   "initial": 2, 
   "type": "cyclic", 
   "size": 4
  }, 
  "5": {
   "index": 1, 
   "attractor": "b6ead8fadc6fe8c7b625", 
   "trajectory": [
    5, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3
   ], 
   "initial": 5, 
   "type": "cyclic", 
   "size": 4
  }, 
  "4": {
   "index": 1, 
   "attractor": "b6ead8fadc6fe8c7b625", 
   "trajectory": [
    4, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3, 
    0, 
    1, 
    2, 
    3
   ], 
   "initial": 4, 
   "type": "cyclic", 
   "size": 4
  }
 }, 
 "fingerprint_map": {
  "1": [
   true, 
   true, 
   true, 
   false
  ], 
  "0": [
   true, 
   true, 
   false, 
   false
  ], 
  "3": [
   true, 
   true, 
   false, 
   true
  ], 
  "2": [
   true, 
   true, 
   true, 
   true
  ], 
  "5": [
   true, 
   false, 
   true, 
   true
  ], 
  "4": [
   true, 
   false, 
   false, 
   true
  ]
 }, 
 "cyclic_attractor_info": {
  "b6ead8fadc6fe8c7b625": [
   0, 
   1, 
   2, 
   3
  ]
 }, 
 "attractor_info": {
  "b6ead8fadc6fe8c7b625": "cyclic"
 }, 
 "fingerprint_map_keys": [
  "A", 
  "B", 
  "C", 
  "D"
 ]
}
```
