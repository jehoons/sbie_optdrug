# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import json,re
from ipdb import set_trace
from termutil import progressbar
from os import system
from os.path import dirname,join,exists
from boolean3_addon import attr_cy
import numpy as np

from sbie_optdrug.result import tab_s3
from sbie_optdrug.result import tab_s7
from boolean3 import Model 
from boolean3_addon import attractor


def getconfig():
    "return config object"
    return tab_s7.config


def run_a(config=None, force=False):    
    "Prepare equation file"    
    if exists(config['output']['a']) and force==False: 
        return

    data = tab_s3.load()
    eq_list = data['equation'].values.tolist()    

    node_set = set() 
    for eq in eq_list: 
        text2 = eq.replace('and', ' ')    
        text2 = text2.replace('or', ' ')    
        text2 = text2.replace('not', ' ')    
        text2 = text2.replace('*=', ' ')
        nodes = set(text2.split(' '))
        node_set = node_set.union(nodes)    
    
    for el in ['', '0', '1', 'True', 'False']: 
        if el in node_set: 
            node_set.remove(el)
    
    datadict = {} 
    
    for node in node_set: 
        if node == '':
            continue 
        data = { 'type': 'normal', 'value': None }
        datadict[node] = data
    init_list = []
    
    for node in node_set:
        init_list.append('%s=Random' % node)
    
    alleq = init_list + eq_list
    model_string = "\n".join(init_list + eq_list)

    with open(config['output']['a'], 'w') as f: 
        f.write(model_string)


def run_b(config=None, force=False):
    "Compute basin size of the model"
    outputfile = config['output']['b']
    if exists(outputfile) and force==False: 
        return

    data = tab_s7.load_a()
    model = "\n".join( data['equation'].values.tolist() )

    samples = config['parameters']['samples']
    steps = config['parameters']['steps']
    on_states = config['parameters']['on_states'] 
    off_states = config['parameters']['off_states'] 

    attr_cy.build(model, on_states=on_states, off_states=off_states)
    result_data = attr_cy.run(samples=samples, steps=steps, debug=True)
    # on_states=[], off_states=[]
    json.dump(result_data, open(outputfile, 'w'), indent=4)


def run_b_plot(config=None, force=False):
    "draw figure"
    outputfile = config['output']['b_plot']
    if exists(outputfile) and force==False: 
        return

    result_data = tab_s7.load_b()
    ratio_list = [] 
    labels = []
    for attrk in result_data['attractors'].keys():
        r = result_data['attractors'][attrk]['ratio']
        ratio_list.append(r)
        labels.append(attrk)
    
    fig, ax = plt.subplots()
    
    ax.bar(np.arange(len(ratio_list)), ratio_list)
    ax.set_xticklabels(labels)
    plt.savefig(outputfile)


def run_c(config=None, force=False):
    "generate input combinations"
    from itertools import combinations,product
    from copy import deepcopy

    outputfile = config['output']['c']
    if exists(outputfile) and force==False: 
         return

    result_data = tab_s7.load_b()    
    nodes = result_data['labels']
    input_nodes = config['parameters']['input_nodes']

    free_nodes = set(nodes) - set(input_nodes)
    free_nodes = list(set(free_nodes))
    combi1 = [c for c in combinations(free_nodes, 1)]
    combi2 = [c for c in combinations(free_nodes, 2)]
    combi3 = [c for c in combinations(free_nodes, 3)]
    combi = combi1 + combi2 + [()]
    table = list(product([False, True], repeat=len(input_nodes)))
    
    config_list = []
    for k,inp in enumerate(table):
        progressbar.update(k, len(table))
        for com in combi:
            on_states = [] 
            off_states = [] 
            off_states = off_states + [c for c in com]
            for i,t in enumerate(inp):
                if t : 
                    on_states.append( input_nodes[i] ) 
                else: 
                    off_states.append( input_nodes[i] )
            
            config1 = deepcopy(config)
            config1['parameters']['on_states'] = deepcopy(on_states)
            config1['parameters']['off_states'] = deepcopy(off_states)
            config_list.append(deepcopy(config1))                       

    with open(outputfile, 'w') as outfile:
        json.dump({'configs': config_list, 'num_configs': len(config_list)},
            outfile, indent=4)


def myengine(config): 
    samples = config['parameters']['samples']
    steps = config['parameters']['steps']
    on_states = config['parameters']['on_states'] 
    off_states = config['parameters']['off_states']

    if not exists('engine.pyx'):
        data = tab_s7.load_a()        
        model = "\n".join( data['equation'].values.tolist() )
        attr_cy.build(model)

    import pyximport; pyximport.install()

    import engine

    result = engine.main(samples=samples, steps=steps, debug=False, \
        progress=False, on_states=on_states, off_states=off_states)

    result['parameters'] = {
        'samples': samples,
        'steps': steps
        }

    return result


def run_d(config=None, force=False): 

    outputfile = config['output']['d']
    if exists(outputfile) and force==False: 
         return

    data = json.load(open('TABLE_S7C_INPUT_COMBINATIONS.json','r'))    
    
    import time 
    from multiprocessing import Pool    
    p = Pool(60)    
    
    scanning_result = p.map(myengine, data['configs'])
    
    with open(outputfile, 'w') as fileout:
        json.dump({'scanning_results': scanning_result}, fileout, indent=1)

        