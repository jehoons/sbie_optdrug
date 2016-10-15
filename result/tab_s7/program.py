# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ipdb import set_trace
import json,re
from boolean3 import Model 
from boolean3_addon import attractor
from termutil import progressbar
from os.path import dirname,join,exists
from sbie_optdrug.result import tab_s3
from sbie_optdrug.result import tab_s7
from boolean3_addon import attr_cy
import json
import numpy as np

config = {
    'program': 'Table_S7',
    'parameters': {
        'samples': 100000,
        'steps': 30
        },
    'input': {
        # 'a': inputfile_a
        },
    'output': {
        'a': tab_s7.outputfile_a, 
        'b': tab_s7.outputfile_b, 
        'b_plot': tab_s7.outputfile_b_plot
        }
    }

def getconfig():
    
    return config


def run_step1(config=None, force=False):
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


def run_step2(config=None, force=False):
    "Compute basin size of the model"
    outputfile = config['output']['b']
    if exists(outputfile) and force==False: 
        return

    data = tab_s7.load_a()
    model = "\n".join( data['equation'].values.tolist() )
    attr_cy.build(model)
    samples = config['parameters']['samples']
    steps = config['parameters']['steps']
    result_data = attr_cy.run(samples=samples, steps=steps, debug=False)
    json.dump(result_data, open(outputfile, 'w'), indent=4)


def run_step2_plot(config=None, force=False):
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

