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
import ternary
import math

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
inputfile_g = join(dirname(__file__), '..','tab_s7','untracked_Table_S7A_Fumia-processed.csv')
inputfile_h = join(dirname(__file__), '..','tab_s7','untracked_Table_S7F-Input-combinations-APC.json')
inputfile_i = join(dirname(__file__), '..','tab_s7','untracked_Table_S7G-Scanning-results-APC.json')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S10B_total_attractor_input_condition_APC.csv')
#outputfile_b = join(dirname(__file__), 'TABLE.S10B_total_attractor_input_condition.csv')
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

    #total_attractor_data = open(config['output']['output_a'], 'w')
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
    total_attractor = pd.DataFrame([], columns=['Input_GFs', 'Input_Hypoxia', 'Input_Mutagen',
                                               'Input_Nutrients', 'Input_TNFalpha', 'Perturbation1', 'Perturbation2',
                                               'Apoptosis', 'Proliferation', 'Quiescent',
                                                'Total', 'Distance'])

    for i in range(len(attractor_result['scanning_results'])):
        progressbar.update(i, len(attractor_result['scanning_results']))
        off_state = input_condi['configs'][i]['parameters']['off_states']
        on_state = input_condi['configs'][i]['parameters']['on_states']
        if 'S_GFs' in off_state:
            total_attractor.loc[i, 'Input_GFs'] = 0
        elif 'S_GFs' in on_state:
            total_attractor.loc[i, 'Input_GFs'] = 1
        if 'S_Hypoxia' in off_state:
            total_attractor.loc[i, 'Input_Hypoxia'] = 0
        elif 'S_Hypoxia' in on_state:
            total_attractor.loc[i, 'Input_Hypoxia'] = 1
        if 'S_Mutagen' in off_state:
            total_attractor.loc[i, 'Input_Mutagen'] = 0
        elif 'S_Mutagen' in on_state:
            total_attractor.loc[i, 'Input_Mutagen'] = 1
        if 'S_Nutrients' in off_state:
            total_attractor.loc[i, 'Input_Nutrients'] = 0
        elif 'S_Nutrients' in on_state:
            total_attractor.loc[i, 'Input_Nutrients'] = 1
        if 'S_TNFalpha' in off_state:
            total_attractor.loc[i, 'Input_TNFalpha'] = 0
        elif 'S_TNFalpha' in on_state:
            total_attractor.loc[i, 'Input_TNFalpha'] = 1
        total_input = on_state
        total_input.extend(off_state)
        j = 0
        ano_input = {}
        for j in range(len(total_input)):
            input_one = total_input[j]
            if (input_one != 'S_GSK_3_APC') and (input_one != 'S_APC'):
                if not (input_one in input_nodes):
                    if len(ano_input) == 0:
                        total_attractor.loc[i, 'Perturbation1'] = input_one
                        ano_input = [input_one]
                    else:
                        total_attractor.loc[i, 'Perturbation2'] = input_one
            j += 1
        attractor = attractor_result['scanning_results'][i]['attractors']
        state_key = attractor_result['scanning_results'][i]['state_key']
        if len(attractor) > 0:
            att_condi = pd.DataFrame([], columns=['Attractor_No', 'Value', 'Type', 'State_key', 'Ratio', 'Phenotype'])
            k = 0
            for t in attractor.keys():
                att = attractor[t]
                att_type = att['type']
                if att_type == 'point':
                    att_state = state_key[t]
                    att_condi.loc[k, 'Attractor_No'] = t
                    att_condi.loc[k, 'Value'] = att['value']
                    att_condi.loc[k, 'Type'] = att_type
                    att_condi.loc[k, 'Ratio'] = att['ratio']
                    att_condi.loc[k, 'State_key'] = att_state
                    if att_state[apop] == '1':
                        att_condi.loc[k, 'Phenotype'] = 'Apoptosis'
                        # if (att_state[pro_qui_1] == '1') | (att_state[pro_qui_2] == '1') | (
                        #             att_state[pro_qui_3] == '1') | (att_state[pro_qui_4] == '1'):
                        #     att_condi.loc[k, 'Phenotype'] = 'Apoptosis-Proliferation'
                        # elif (att_state[pro_qui_1] == '0') & (att_state[pro_qui_2] == '0') & (
                        # att_state[pro_qui_3] == '0') & (att_state[pro_qui_4] == '0'):
                        #     att_condi.loc[k, 'Phenotype'] = 'Apoptosis'
                    elif (att_state[pro_qui_1] == '1') | (att_state[pro_qui_2] == '1') | (
                        att_state[pro_qui_3] == '1') | (att_state[pro_qui_4] == '1'):
                        att_condi.loc[k, 'Phenotype'] = 'Proliferation'
                    elif (att_state[pro_qui_1] == '0') & (att_state[pro_qui_2] == '0') & (
                        att_state[pro_qui_3] == '0') & (att_state[pro_qui_4] == '0'):
                        att_condi.loc[k, 'Phenotype'] = 'Quiescent'
                    k += 1

                elif att_type == 'cyclic':
                    ii = 0
                    att_condi.loc[k, 'Attractor_No'] = t
                    att_condi.loc[k, 'Type'] = att_type
                    len_cycle = len(att['value'])
                    for ii in range(len(att['value'])):
                        att_cycle_value = att['value'][ii]
                        att_cycle_state = state_key[att_cycle_value]
                        att_condi.loc[k, 'Value'] = att_cycle_value
                        att_condi.loc[k, 'State_key'] = att_cycle_state
                        att_condi.loc[k, 'Ratio'] = att['ratio']/len_cycle
                        if att_cycle_state[apop] == '1':
                            att_condi.loc[k, 'Phenotype'] = 'Apoptosis'
                            # if (att_state[pro_qui_1] == '1') | (att_state[pro_qui_2] == '1') | (
                            #             att_state[pro_qui_3] == '1') | (att_state[pro_qui_4] == '1'):
                            #     att_condi.loc[k, 'Phenotype'] = 'Apoptosis-Proliferation'
                            # elif (att_state[pro_qui_1] == '0') & (att_state[pro_qui_2] == '0') & (
                            #             att_state[pro_qui_3] == '0') & (att_state[pro_qui_4] == '0'):
                            #     att_condi.loc[k, 'Phenotype'] = 'Apoptosis'
                        elif ((att_cycle_state[pro_qui_1] == '1') | (att_cycle_state[pro_qui_2] == '1') | (
                            att_cycle_state[pro_qui_3] == '1') | (att_cycle_state[pro_qui_4] == '1')):
                            att_condi.loc[k, 'Phenotype'] = 'Proliferation'
                        elif ((att_cycle_state[pro_qui_1] == '0') & (att_cycle_state[pro_qui_2] == '0') & (
                            att_cycle_state[pro_qui_3] == '0') & (att_cycle_state[pro_qui_4] == '0')):
                            att_condi.loc[k, 'Phenotype'] = 'Quiescent'
                        ii += 1
                        k += 1

            total_basin = sum(att_condi['Ratio'])
            total_attractor.loc[i, 'Total'] = total_basin
            att_condi_apo = att_condi[att_condi['Phenotype'] == 'Apoptosis']
            #att_condi_apopro = att_condi[att_condi['Phenotype'] == 'Apoptosis-Proliferation']
            att_condi_pro = att_condi[att_condi['Phenotype'] == 'Proliferation']
            att_condi_qui = att_condi[att_condi['Phenotype'] == 'Quiescent']
            apo_basin_b = sum(att_condi_apo['Ratio'])
            #apopro_basin_b = sum(att_condi_apopro['Ratio'])
            pro_basin_b = sum(att_condi_pro['Ratio'])
            qui_basin_b = sum(att_condi_qui['Ratio'])
            basin_sum = apo_basin_b + pro_basin_b + qui_basin_b

            if total_basin != 0:
                if total_basin == basin_sum:
                    apo_basin = apo_basin_b/total_basin
                    #apopro_basin = apopro_basin_b/total_basin
                    pro_basin = pro_basin_b/total_basin
                    qui_basin = qui_basin_b/total_basin
            else:
                apo_basin = apo_basin_b
                # apopro_basin = apopro_basin_b
                pro_basin = pro_basin_b
                qui_basin = qui_basin_b
            total_attractor.loc[i, 'Apoptosis'] = apo_basin
            total_attractor.loc[i, 'Proliferation'] = pro_basin
            total_attractor.loc[i, 'Quiescent'] = qui_basin
            # total_attractor.loc[i, 'Apoptosis-proliferation'] = apopro_basin
            total_attractor.loc[i, 'Distance'] = math.sqrt(math.pow(1-apo_basin,2)+math.pow(pro_basin,2)+math.pow(qui_basin,2))

        i += 1
    total_attractor.to_csv(config['output']['output_a'], index=False)

    set_trace()




    #with open(config['output']['a'], 'w') as fobj:
    #    fobj.write('hello')
