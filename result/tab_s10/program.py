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
outputfile_a = join(dirname(__file__), 'TABLE_S8A_aaa.csv')
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

    #apoptotic, characterized by active caspases
    #proliferative, in which cyclins are activated along the cell cycle in the correct sequence;
    #quiescent, with cyclins inactive or activated in a wrong sequence.In terms of such phenotypes

    input_node = input_condi['configs'][0]['parameters']['input_nodes']
    label = attractor_result['scanning_results'][0]['labels']
    i = 0
    for i in range(len(label)):
        label_node = label[i]
        if label_node == 'S_Caspase8':
            apop_1 = i
        elif label_node == 'S_Caspase9':
            apop_2 = i
        elif label_node == 'S_CycA':
            pro_qui_1 = i
        elif label_node == 'S_CycB':
            pro_qui_2 = i
        elif label_node == 'S_CycC':
            pro_qui_3 = i
        elif label_node == 'S_CycD':
            pro_qui_4 = i

    i = 0
    for i in range(len(attractor_result['scanning_results'])):
        off_state = input_condi['configs'][i]['parameters']['off_states']
        on_state = input_condi['configs'][i]['parameters']['on_states']
        if len(off_state) > 0 :
            j = 0
            for j in range(len(off_state)):
                off_state_node = off_state[j]
                if off_state_node in input_node:
                    off_state_input = off_state_node #put in list
                else:
                    off_state_else = off_state_node #putin list
                j += 1
        if len(on_state) > 0 :
            j = 0
            for j in range(len(on_state)):
                on_state_node = on_state[j]
                if on_state_node in input_node:
                    on_state_input = on_state_node #putin list
                else:
                    on_state_else = on_state_node #putin list
                j += 1

        attractor = attractor_result['scanning_results'][i]['attractors']
        state_key = attractor_result['scanning_results'][i]['state_key']
        if len(attractor) > 0 :
            for j in attractor.keys():
                att = attractor[j]
                if att['type'] == 'point':
                    att_state = state_key[j]
                    if (att_state[apop_1] == 1) & (att_state[apop_2] == 1):
                        phenotype = {'phenotype': 'apoptotic'}
                    elif (att_state[pro_qui_1] == 1) & (att_state[pro_qui_2] == 1) & (att_state[pro_qui_3] == 1) & (att_state[pro_qui_4] == 1):
                        phenotype = {'phenotype': 'proliferative'}
                    elif (att_state[pro_qui_1] == 0) & (att_state[pro_qui_2] == 0) & (att_state[pro_qui_3] == 0) & (att_state[pro_qui_4] == 0):
                        phenotype = {'phenotype': 'quiescent'}
                    att_new = att+phenotype #merge two list
                    att_point = {j: att_new} #putin list
                elif att['type'] == 'cyclic':
                    k = 0
                    for k in range(len(att['value'])):
                        att_cycle_value = att['value'][k]
                        att_cycle_state = state_key[att_cycle_value]
                        if (att_state[apop_1] == 1) & (att_state[apop_2] == 1):
                            phenotype = {'phenotype': 'apoptotic'}
                        elif (att_state[pro_qui_1] == 1) & (att_state[pro_qui_2] == 1) & (att_state[pro_qui_3] == 1) & (
                            att_state[pro_qui_4] == 1):
                            phenotype = {'phenotype': 'proliferative'}
                        elif (att_state[pro_qui_1] == 0) & (att_state[pro_qui_2] == 0) & (att_state[pro_qui_3] == 0) & (
                            att_state[pro_qui_4] == 0):
                            phenotype = {'phenotype': 'quiescent'}
                        att_new = att + phenotype  # merge two list
                        k += 1
                    att_cycle = {j: att} #putin list
        #off_state_input,off_state_else,on_state_input,on_state_else,att_point,att_cycle merge한 파일 만들기


        print(0)


    set_trace()

    #with open(config['output']['a'], 'w') as fobj:
    #    fobj.write('hello')
