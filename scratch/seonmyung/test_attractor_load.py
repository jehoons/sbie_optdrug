import json
from sbie_optdrug.boolean2 import Model
from sbie_optdrug.analysis.boolnet import find_attractors
from ipdb import set_trace
from itertools import izip
import pandas as pd

attr_data = json.load(open('output.json','rb'))

attrs = attr_data['basin_of_attraction']
fmap = attr_data['fingerprint_map']
mapkeys = attr_data['fingerprint_map_keys']
attr_info = attr_data['attractor_info']

df0 = pd.DataFrame([], columns=['attrid'] + mapkeys + ['size'] + ['type'])

i = 0
for attrid in attrs.keys():

    attr_type = attr_info[attrid]

    basinsize = attrs[attrid]
    statevectr = fmap[attrid]

    state = {}
    for k, s in izip(mapkeys, statevectr):
        #print k, s
        state[k] = int(s)

    df0.loc[i, 'attrid'] = attrid
    df0.loc[i, mapkeys] = state
    #df0.loc[i] = state
    df0.loc[i, 'size'] = basinsize
    df0.loc[i, 'type'] = attr_type

    i += 1

df0.to_csv('output_attr_analysis.csv', index=False)

