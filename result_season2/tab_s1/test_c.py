import json,itertools,pytest
from os.path import exists
from numpy.random import random
from boolean3_addon import attr_cy, to_logic
from pdb import set_trace
from boolean3_addon import to_logic 
from os.path import exists,dirname
import pandas as pd
from tqdm import tqdm 

from sbie_optdrug.result_season2 import tab_s1
from sbie_optdrug.result_season2.tab_s1 import fumia_phenotype
from fumia_phenotype import *


def get_input_combinations():    

    inputs = [ {
    'State_Mutagen' : State_Mutagen, 
    'State_GFs': State_GFs,
    'State_Nutrients': State_Nutrients,
    'State_TNFalpha': State_TNFalpha,
    'State_Hypoxia': State_Hypoxia,
    'State_Gli': False,
    } for State_Mutagen,State_GFs,State_Nutrients,State_TNFalpha, \
        State_Hypoxia in itertools.product([False,True], repeat=5)]

    return inputs

def get_mutations_config_all():
    list_mutations_config = []
    for State_APC, State_Ras, State_Smad, State_PTEN, State_p53 in \
        itertools.product([None, 'off', 'on'], repeat=5):

        mutations_config = {
            'State_APC': State_APC,
            'State_Ras': State_Ras,
            'State_Smad': State_Smad,
            'State_PTEN': State_PTEN,
            'State_p53': State_p53,
            }   

        list_mutations_config.append(mutations_config)

    return list_mutations_config


def get_mutations_config():
   
    # free
    mutations_config_list = [ 
        {
            'State_APC': None,
            'State_Ras': None,
            'State_Smad': None,
            'State_PTEN': None,
            'State_p53': None,
        },

        {
            'State_APC': 'off',
            'State_Ras': None,
            'State_Smad': None, 
            'State_PTEN': None, 
            'State_p53': None, 
        }, 

        {
            'State_APC': 'off',
            'State_Ras': 'on',
            'State_Smad': None, 
            'State_PTEN': None, 
            'State_p53': None, 
        }, 

        {
            'State_APC': 'off',
            'State_Ras': 'on',
            'State_Smad': 'off',
            'State_PTEN': None, 
            'State_p53': None, 
        }, 
        
        {
            'State_APC': 'off',
            'State_Ras': 'on',
            'State_Smad': 'off',
            'State_PTEN': 'off', 
            'State_p53': None, 
        },

        {
            'State_APC': 'off',
            'State_Ras': 'on',
            'State_Smad': 'off',
            'State_PTEN': 'off', 
            'State_p53': 'off',
        }
    ]
    return mutations_config_list

def test_c1():    
    import engine
    
    mut_configs = get_mutations_config_all()
    input_combinations = get_input_combinations()

    steps = 60
    samples = 1000
    repeats = 100
    ncpus = 25

    list_simul_condition = [] 
    for input0 in input_combinations:
        for mut0 in mut_configs:
            simul_condition = {'input': input0, 'mutation': mut0}
            on_states = [] 
            off_states = [] 

            for lbl in input0: 
                if input0[lbl] == True: 
                    on_states.append(lbl)
                else:
                    off_states.append(lbl)

            for lbl in mut0: 
                if mut0[lbl] == 'on': 
                    on_states.append(lbl)
                elif mut0[lbl] == 'off':
                    off_states.append(lbl)
                else: 
                    pass

            list_simul_condition.append({
                'simul_condition': simul_condition,
                'on_states': on_states, 
                'off_states': off_states, 
                })

    results = []

    for simul_condition in tqdm(list_simul_condition, ascii=True): 
        on_states = simul_condition['on_states']
        off_states = simul_condition['off_states']
        res = attr_cy.parallel(engine, 
                                steps=steps,
                                samples=samples,
                                ncpus=ncpus,
                                repeats=repeats, 
                                on_states=on_states,
                                off_states=off_states
                                )
        res = attach_phenotype({'input_condition': simul_condition, 
                                'simul_result': res})        
        results.append(res)

    json.dump(results, open(file_c1, 'w'), indent=4)



    
# input 
file_a2 = join(dirname(tab_s1.__file__), 'a', 
                'a2-fumia-model-processed-weighted-sum.txt')

# output 
file_c1 = join(dirname(tab_s1.__file__), 'c', 
                'c1-simul-results.json')

file_c2 = join(dirname(tab_s1.__file__), 'c', 
                'c2-simul-results-summary.csv')

with open(file_a2, 'r') as fobj:
    lines = fobj.readlines()
    lines2 = [] 
    for lin in lines: 
        lin = lin.strip()
        if lin[0] == '#': 
            continue 
        right = lin.split('=')[1].strip()
        if right == 'input':            
            lines2.append( lin.split('=')[0].strip() + '=' + 'False') 
        else: 
            lines2.append(lin)

    modeltext = "\n".join(lines2)

attr_cy.build(modeltext, pyx='engine.pyx', weighted_sum=True)

import pyximport; pyximport.install()




