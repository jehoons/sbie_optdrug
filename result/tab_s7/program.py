# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
from ipdb import set_trace
import json,re
from boolean3 import Model 
from boolean3_addon import attractor
from termutil import progressbar
from os.path import dirname,join
from sbie_optdrug.result import tab_s3
from sbie_optdrug.result import tab_s7
from boolean3_addon import attr_cy

config = {
    'program': 'Table_S7',
    'parameters': {
        'samples': 10000, 
        'steps': 30
        },
    'input': {
        # 'a': inputfile_a
        },
    'output': {
        'a': tab_s7.outputfile_a, 
        'b': tab_s7.outputfile_b
        }
    }

def getconfig():
    
    return config

# def run(config=None):

#     with open(config['output']['a'], 'w') as fobj:
#         fobj.write('hello')

def run_step1(config=None):

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


def run_step2(config=None):

    data = tab_s7.load_a()
    model = "\n".join( data['equation'].values.tolist() )
    attr_cy.build(model)
    samples = config['parameters']['samples']
    steps = config['parameters']['steps']
    result_data = attr_cy.run(samples=samples, steps=steps, debug=False)
    json.dump(result_data, open(config['output']['b'], 'w'), indent=4)

