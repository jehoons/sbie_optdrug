# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import sbie_optdrug
from os.path import exists
from ipdb import set_trace
from boolean2 import Model
import hashlib
import pandas as pd
from util import progressbar 
import json

# 아래의 알고리즘에서는 2번의 반복이 있어야만 사이클로 인식을 하는것 같다. 
# 왜 이렇게 하는것일까? 그것은... chaos인 경우가 있기때문인 것으로 생각된다. 
# def detect_cycles( data ):
#     """
#     Detects cycles in the data

#     Returns a tuple where the first item is the index at wich the cycle occurs 
#     the first time and the second number indicates the lenght of the cycle 
#     (it is 1 for a steady state)
#     """

#     fsize   = len(data)

#     # set_trace()

#     # maximum size
#     for msize in range(1, fsize/2+1):
#         for index in range(fsize):
#             left  = data[index:index+msize]
#             right = data[index+msize:index+2*msize]

#             # print data
#             # print left, right 

#             if left == right:
#                 return index, msize

#     return 0, 0


def find_attractors(model=None, steps=30, mode='sync', sample_size=1000):

    simulation_data = { }
    fingerprint_mapping = { }
    seen = { }

    for i in range(sample_size):
        progressbar.update(i, sample_size)

        model.initialize()
        model.iterate( steps=steps )

        key = model.first.fp()
        
        values = [ x.fp() for x in model.states[:steps] ]

        # detect_cycles() 함수가 사이클을 검출하기 위해서는 2개의 주기가 필요하다. 그러므로 
        # 충분히 긴 timesteps 동안 시뮬레이션을 해야 한다.        
        index, size = model.detect_cycles( )

        if size == 1:
            attr_type = 'point'
        elif size > 1:
            attr_type = 'cyclic'
        elif size == 0:
            attr_type = 'unknown'
        else: 
            assert False

        if attr_type == 'cyclic':
            cyc_traj = values[index:index + size]
            cyc_hash = hashlib.sha224(repr(sorted(cyc_traj))).hexdigest()
            cyc_hash = cyc_hash[0:20]
            attr_id = cyc_hash 
        else: 
            attr_id = values[-1]

        seen [str(key)] = {
            'index':index, 
            'size':size,
            'trajectory': values,
            'type': attr_type,
            'initial': values[0],
            'attractor': attr_id
            }

        for x in model.states:
            fingerprint_mapping[ str(x.fp()) ] = x.values()

    simulation_data = {
        'fingerprint_map': fingerprint_mapping,
        'fingerprint_map_keys': x.keys(),
        'attractors': seen
        }

    df = pd.DataFrame([], columns=[
        'initial_state','attractor', 'cyclic_attractor'])
    j = 0
    
    cyclic_attr_info = {}
    for initial in simulation_data['attractors'].keys():
        if simulation_data['attractors'][str(initial)]['type'] == 'unknown':
            continue

        attr = simulation_data['attractors'][str(initial)]['attractor']
        attr_type = simulation_data['attractors'][str(initial)]['type']
        df.loc[j, 'initial_state'] = str(initial)
        df.loc[j, 'type'] = attr_type

        if attr_type == 'point':
            df.loc[j, 'attractor'] = attr

        elif attr_type == 'cyclic':
            traj = simulation_data['attractors'][str(initial)]['trajectory']
            idx = simulation_data['attractors'][str(initial)]['index']
            sz = simulation_data['attractors'][str(initial)]['size']
            cyc_traj = traj[idx:idx+sz]
            cyc_hash = hashlib.sha224(repr(sorted(cyc_traj))).hexdigest()
            cyc_hash = cyc_hash[0:20]
            df.loc[j, 'attractor'] = cyc_hash
            cyclic_attr_info[cyc_hash] = cyc_traj

        j += 1

    simulation_data['cyclic_attractor_info'] = cyclic_attr_info

    basin = df.groupby('attractor')['initial_state'].count().to_frame()
    basin.rename(columns={'initial_state': 'basin_size'}, inplace=True)
    basin = basin.to_dict()['basin_size']

    for old_key in basin.keys():
        new_key = str(old_key)
        basin[new_key] = int( basin.pop(old_key) )

    simulation_data['basin_of_attraction'] = basin

    attr_type_data = {}
    for i in df.index:
        attr =  df.loc[i, 'attractor']
        attr_type = df.loc[i, 'type']
        attr_type_data[attr] = attr_type

    simulation_data['attractor_info'] = attr_type_data

    # df.to_csv('output.csv')

    return simulation_data



def test_compute_basin():


    import sbie_optdrug
    from boolean2 import Model
    from boolean2_addon import attractor 

    # text = """
    # A = Random
    # B = Random
    # C = Random
    # D = Random

    # A *= D or C
    # B *= A
    # C *= B or D
    # D *= B
    # """

    text = """
    A = True
    B = True
    C = False
    
    B*= A
    C*= B 
    A*= not C
    """

    model = Model( text=text, mode='sync')
    res = attractor.find_attractors(model=model, sample_size=10)
    
    outputfile = 'test_basin_result.json'

    json.dump(res, open(outputfile, 'w'), indent=1)

    assert exists(outputfile)

