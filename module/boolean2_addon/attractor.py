# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import sbie_optdrug
import hashlib
from pdb import set_trace
# import boolean2
from boolean2 import Model
import pandas as pd
from sbie_optdrug.util import progressbar 
import json


def find_attractors(model=None, steps=10, mode='sync', sample_size=1000):

    simulation_data = { }
    seen = {}
    fingerprint_mapping = {}

    for i in range(sample_size):
        progressbar.update(i, sample_size)

        model.initialize()
        model.iterate( steps=steps )
        index,size = model.detect_cycles()
        key = model.first.fp()

        values = [ x.fp() for x in model.states[:steps] ]

        if size == 1:
            attr_type = 'point'
        elif size > 1:
            attr_type = 'cyclic'
        elif size == 0:
            attr_type = 'unknown'

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

