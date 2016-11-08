# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import json
import pickle
from os.path import dirname,join
from sbie_optdrug.dataset import filelist
import pandas as pd
from ipdb import set_trace
import sbie_optdrug
from sbie_optdrug.dataset import ccle
from termutil import progressbar

#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#import random

#from boolean3_addon import attr_cy
#import numpy as np

#from boolean3 import Model
#from boolean3_addon import attractor

""" requirements """
inputfile_a = join(dirname(__file__), '..','tab_s2','TABLE.S2.NODE-NAME.CSV')
inputfile_b = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s1.json')
inputfile_c = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s4.json')
inputfile_d = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s1.json')
inputfile_e = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s4.json')
inputfile_f = join(dirname(__file__), '..','tab_s5','TABLE.S5C.DRUG_data.json')
inputfile_g = join(dirname(__file__), '..','tab_s7','TABLE_S7A_FUMIA_PROCESSED.csv')
inputfile_h = join(dirname(__file__), '..','tab_s7','TABLE_S7C_INPUT_COMBINATIONS.json')
inputfile_i = join(dirname(__file__), '..','tab_s7','TABLE_S7D_SCANNING_RESULT.json')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE_S8A_total_attractor_input_condition.json')
#outputfile_b = join(dirname(__file__), 'TABLE.S8A.COPYNUMVAR_data_s4.json')
#outputfile_c = join(dirname(__file__), 'TABLE.S8B.MUTATION_data_s1.json')
#outputfile_d = join(dirname(__file__), 'TABLE.S8B.MUTATION_data_s4.json')
#outputfile_e = join(dirname(__file__), 'TABLE.S8C.DRUG_data.json')

config = {
    'program': 'template',
    'input': {
        'input_a': inputfile_a,
        'input_b': inputfile_b,
        'input_c': inputfile_c,
        'input_d': inputfile_d,
        'input_e': inputfile_e,
        'input_f': inputfile_f,
        'input_g': inputfile_g,
        'input_h': inputfile_h,
        'input_i': inputfile_i
        },
    'output': {
        'output_a': outputfile_a,
        #'output_b': outputfile_b,
        #'output_c': outputfile_c,
        #'output_d': outputfile_d,
        #'output_e': outputfile_e
        }
    }


def getconfig():

    return config


def run(config=None):

    gene = pd.read_csv(config['input']['input_a'])
    copy_number_data_s1 = json.load(open(config['input']['input_b'], 'rb'))
    copy_number_data_s4 = json.load(open(config['input']['input_c'], 'rb'))
    mutation_data_s1 = json.load(open(config['input']['input_d'], 'rb'))
    mutation_data_s4 = json.load(open(config['input']['input_e'], 'rb'))
    drug_data = json.load(open(config['input']['input_f'], 'rb'))
    equation = pd.read_csv(config['input']['input_g'])
    input_condi = json.load(open(config['input']['input_h'], 'rb'))
    attractor_result = json.load(open(config['input']['input_i'], 'rb'))

    total_attractor_data = open(config['output']['output_a'], 'w')
    #apoptotic, characterized by active caspases
    #proliferative, in which cyclins are activated along the cell cycle in the correct sequence;
    #quiescent, with cyclins inactive or activated in a wrong sequence.In terms of such phenotypes

    input_nodes = input_condi['configs'][0]['parameters']['input_nodes']
    label = attractor_result['scanning_results'][0]['labels']
    i = 0
    for i in range(len(label)):
        label_node = label[i]
        if label_node == 'S_Apoptosis':
            apop = i
        elif label_node == 'S_CycA':
            pro_qui_1 = i
        elif label_node == 'S_CycB':
            pro_qui_2 = i
        elif label_node == 'S_CycD':
            pro_qui_3 = i
        elif label_node == 'S_CycE':
            pro_qui_4 = i
        i += 1

    i = 0
    total_data = {}
    for i in range(len(attractor_result['scanning_results'])):
        progressbar.update(i, len(attractor_result['scanning_results']))
        off_state = input_condi['configs'][i]['parameters']['off_states']
        on_state = input_condi['configs'][i]['parameters']['on_states']
        input_state = {'on': {}, 'off': {}}
        ano_state = {'on': {}, 'off': {}}
        if len(off_state) > 0 :
            j = 0
            input_off = {}
            ano_off = {}
            for j in range(len(off_state)):
                off_state_node = off_state[j]
                if off_state_node in input_nodes:
                    if len(input_off) == 0:
                        input_off = [off_state_node]
                    elif len(input_off) != 0:
                        input_off.append(off_state_node)
                else:
                    if len(ano_off) == 0:
                        ano_off = [off_state_node]
                    elif len(ano_off) != 0:
                        ano_off.append(off_state_node)
                j += 1
            input_state['off'] = input_off
            ano_state['off'] = ano_off

        if len(on_state) > 0 :
            j = 0
            input_on = {}
            ano_on = {}
            for j in range(len(on_state)):
                on_state_node = on_state[j]
                if on_state_node in input_nodes:
                    if len(input_on) == 0:
                        input_on = [on_state_node]
                    elif len(input_state) != 0:
                        input_on.append(on_state_node)
                else:
                    if len(ano_on) == 0:
                        ano_on = [on_state_node]
                    elif len(ano_on) != 0:
                        ano_on.append(on_state_node)
                j += 1
            input_state['on'] = input_on
            ano_state['on'] = ano_on

        attractor = attractor_result['scanning_results'][i]['attractors']
        state_key = attractor_result['scanning_results'][i]['state_key']
        if len(attractor) > 0 :
            att_condi = {}
            for j in attractor.keys():
                att = attractor[j]
                phenotype = {'phenotype': {}}
                att = dict(att.items() + phenotype.items())
                if att['type'] == 'point':
                    att_state = state_key[j]
                    if att_state[apop] == '1':
                        att['phenotype'] = 'apoptosis'
                    elif (att_state[pro_qui_1] == '1') | (att_state[pro_qui_2] == '1') | (att_state[pro_qui_3] == '1') | (att_state[pro_qui_4] == '1'):
                        att['phenotype'] = 'proliferation'
                    elif (att_state[pro_qui_1] == '0') & (att_state[pro_qui_2] == '0') & (att_state[pro_qui_3] == '0') & (att_state[pro_qui_4] == '0'):
                        att['phenotype'] = 'quiescent'
                    att_put_in = {j: att}

                elif att['type'] == 'cyclic':
                    k = 0
                    cyc_phe = []
                    for k in range(len(att['value'])):
                        att_cycle_value = att['value'][k]
                        att_cycle_state = state_key[att_cycle_value]
                        if att_cycle_state[apop] == '1':
                            if len(cyc_phe) == 0:
                                cyc_phe = ['apoptosis']
                            else:
                                cyc_phe.append('apoptosis')
                        elif (att_cycle_state[pro_qui_1] == '1') | (att_cycle_state[pro_qui_2] == '1') | (att_cycle_state[pro_qui_3] == '1') | (att_cycle_state[pro_qui_4] == '1'):
                            if len(cyc_phe) == 0:
                                cyc_phe = ['proliferation']
                            else:
                                cyc_phe.append('proliferation')
                        elif (att_cycle_state[pro_qui_1] == 0) & (att_cycle_state[pro_qui_2] == 0) & (att_cycle_state[pro_qui_3] == 0) & (att_cycle_state[pro_qui_4] == 0):
                            if len(cyc_phe) == 0:
                                cyc_phe = ['quiescent']
                            else:
                                cyc_phe.append('quiescent')
                        k += 1
                    att['phenotype'] = cyc_phe
                    att_put_in = {j: att}
                if len(att_condi) == 0:
                    att_condi = att_put_in
                else:
                    att_condi = dict(att_condi.items()+att_put_in.items())
            data_attractor = {'input_node': input_state, 'node_perturbation': ano_state, 'attractor': att_condi,'attractor_state': state_key}
        data_put_in = {i: data_attractor}
        if len(total_data) == 0:
            total_data = data_put_in
        else:
            total_data = dict(total_data.items()+data_put_in.items())
        i += 1
    json.dump(total_data, total_attractor_data, indent=3, sort_keys=True)
    total_attractor_data.close()


    #with open(config['output']['a'], 'w') as fobj:
    #    fobj.write('hello')
