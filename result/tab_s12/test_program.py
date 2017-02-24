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

from os import system
from os.path import dirname,join,exists
from boolean3_addon import attr_cy
import numpy as np

from sbie_optdrug.result import tab_s3
from sbie_optdrug.result import tab_s7
from sbie_optdrug.result import tab_s12 # this 

from boolean3 import Model
from boolean3_addon import attractor
import pandas as pd

if not exists('engine.pyx'):
    data = tab_s7.load_a()
    model = "\n".join( data['equation'].values.tolist() )
    attr_cy.build(model)

import pyximport; pyximport.install()
import engine


def attr_summary(attrdata):

    attrs, statekey, labels = attrdata['attractors'], attrdata['state_key'], attrdata['labels']
    i_apop,i_cyca,i_cycb,i_cycd,i_cyce = labels.index('S_Apoptosis'), \
        labels.index('S_CycA'),labels.index('S_CycB'),labels.index('S_CycD'),labels.index('S_CycE')

    attr2 = {}
    for att in attrs:         
        ratio,value,att_type,count = attrs[att]['ratio'],attrs[att]['value'], \
            attrs[att]['type'],attrs[att]['count']
        if att_type=='point':
            s = [int(c) for c in statekey[value]]
            marker_A = bool(s[i_apop])
            marker_P = bool(s[i_cyca])
            marker_P |= bool(s[i_cycb])
            marker_P |= bool(s[i_cycd])
            marker_P |= bool(s[i_cyce])
            marker_Q =  not marker_A and not marker_P
            res = {
                'A':int(marker_A), 'P':int(marker_P), 'Q':int(marker_Q)
                }

        elif att_type=='cyclic':
            res_arr = [] 
            for v in value:
                s = [int(c) for c in statekey[v]]
                
                marker_A = bool(s[i_apop])
                marker_P = bool(s[i_cyca])
                marker_P |= bool(s[i_cycb])
                marker_P |= bool(s[i_cycd])
                marker_P |= bool(s[i_cyce])

                marker_Q =  not marker_A and not marker_P
                res = {
                    'A':int(marker_A), 'P':int(marker_P), 'Q':int(marker_Q)
                    }
                res_arr.append(res)

            res = {'A':0, 'P':0, 'Q':0}
            for res0 in res_arr: 
                res['A'] += res0['A']/len(res_arr)
                res['P'] += res0['P']/len(res_arr)
                res['Q'] += res0['Q']/len(res_arr)

        else: 
            # assert False
            pass

        attr2[att] = {'ratio': ratio, 'desc': res}

    summary = {
        'attrinfo': attr2, 
        'summary_desc': { 'A':0,'P':0,'Q':0 }
        } 

    A = 0
    P = 0
    Q = 0
    for a in attr2: 
        ratio = attr2[a]['ratio']
        A += attr2[a]['desc']['A']*ratio
        P += attr2[a]['desc']['P']*ratio
        Q += attr2[a]['desc']['Q']*ratio

    summary['summary_desc']['A'] = A
    summary['summary_desc']['P'] = P
    summary['summary_desc']['Q'] = Q

    return summary


def myengine(config):

    samples = config['parameters']['samples']
    steps = config['parameters']['steps']
    on_states = config['parameters']['on_states']
    off_states = config['parameters']['off_states']

    result = engine.main(samples=samples, steps=steps, debug=False, \
        progress=False, on_states=on_states, off_states=off_states)

    result['parameters'] = {
        'samples': samples,
        'steps': steps
        }

    return result


def run_table_a(config=None, force=False):

    from itertools import combinations,product
    from copy import deepcopy

    outputfile = config['tables']['a']

    if exists(outputfile) and force==False:
         return

    result_data = tab_s7.load_b()
    nodes = result_data['labels']

    config_list = []

    # config.

    # config1 = deepcopy(config)
    # config_list.append(config1)

    config_0 = {
        'parameters': {
            'samples': 5000,
            'steps': 60,
            'on_states': None, 
            'off_states': None, 
            'input_nodes': ['S_Mutagen', 'S_GFs', 'S_Nutrients', 'S_TNFalpha', 'S_Hypoxia']
            }
        }

    # carcino, gf, nut, growsupp, hypox
    input_nodes = config_0['parameters']['input_nodes'] 
    on_states = []
    off_states = [] 
    for i, b in enumerate([1,1,1,0,0]):
        if b == 1:
            on_states.append(input_nodes[i])
        else: 
            off_states.append(input_nodes[i])

    # no mutation 
    config_0['parameters']['on_states'] = on_states   
    config_0['parameters']['off_states'] = off_states 

    # # apc 
    config_0['parameters']['on_states'] = on_states 
    config_0['parameters']['off_states'] = off_states + ['S_APC']

    # # apc, ras 
    config_0['parameters']['on_states'] = on_states   + ['S_Ras']
    config_0['parameters']['off_states'] = off_states + ['S_APC']

    # # apc, ras, smad
    config_0['parameters']['on_states'] = on_states   + ['S_Ras']
    config_0['parameters']['off_states'] = off_states + ['S_APC', 'S_Smad']

    # # apc, ras, smad, pten
    config_0['parameters']['on_states'] = on_states   + ['S_Ras']
    config_0['parameters']['off_states'] = off_states + ['S_APC','S_PTEN', 'S_Smad']
    
    # # apc, ras, smad, pten, p53
    config_0['parameters']['on_states'] = on_states   + ['S_Ras']
    config_0['parameters']['off_states'] = off_states + ['S_APC','S_PTEN', 'S_p53', 'S_Smad']

    # print(config_0)

    config_list.append(config_0)  

    with open(outputfile, 'w') as outfile:
        json.dump({'configs': config_list, 'num_configs': len(config_list)},
            outfile, indent=4)


def run_table_b(config=None, force=False):

    outputfile = config['tables']['b']

    if exists(outputfile) and force==False:
         return

    data = json.load(open(config['tables']['a'],'r'))

    import time
    from multiprocessing import Pool

    # p = Pool(20)
    # scanning_result = p.map(myengine, data['configs'])
    # scanning_result = [myengine( data['configs'][1] )]
    
    scanning_result = []
    
    for myconf in data['configs']:
        # print(myconf)
        res = myengine(myconf)
        scanning_result.append(res)

    with open(outputfile, 'w') as fileout:
        json.dump({'scanning_results': scanning_result}, fileout, indent=1)


def run_table_c(config=None, force=False):

    # set_trace()

    table_a = json.load( open(config['tables']['a'], 'r') )
    table_b = json.load( open(config['tables']['b'], 'r') )

    for data in table_b['scanning_results']: 
        res = attr_summary(data)
        P = res['summary_desc']['P']
        A = res['summary_desc']['A']
        Q = res['summary_desc']['Q']

        print ('%.04f\t%.04f\t%.04f'%(P,A,Q))


def test_this(with_small, force):

    # prepare input data 
    run_table_a(config=tab_s12.get_config(), force=True) 

    # simulation 
    run_table_b(config=tab_s12.get_config(), force=True)

    # make summary 
    run_table_c(config=tab_s12.get_config(), force=True)

