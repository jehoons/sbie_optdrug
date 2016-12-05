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
inputfile_g = join(dirname(__file__), '..','tab_s7','TABLE_S7A_FUMIA_PROCESSED.csv')
inputfile_h = join(dirname(__file__), '..','tab_s7','TABLE_S7C_INPUT_COMBINATIONS.json')
inputfile_i = join(dirname(__file__), '..','tab_s7','TABLE_S7D_SCANNING_RESULT.json')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S10B_total_attractor_input_condition.csv')
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
            one_input = total_input[j]
            if not (one_input in input_nodes):
                if len(ano_input) == 0:
                    total_attractor.loc[i, 'Perturbation1'] = one_input
                    ano_input = [one_input]
                else:
                    total_attractor.loc[i, 'Perturbation2'] = one_input
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

            if i == 10000:
                set_trace()

        i += 1
    total_attractor.to_csv(config['output']['output_a'], index=False)

    simulation_data = total_attractor

    i = 0
    no_pert = {}
    sing_pert = {}
    doub_pert = {}
    ben_no_pert_1 = {}
    ben_sing_pert_1 = {}
    ben_doub_pert_1 = {}
    ben_no_pert_2 = {}
    ben_sing_pert_2 = {}
    ben_doub_pert_2 = {}
    ben_no_pert_3 = {}
    ben_sing_pert_3 = {}
    ben_doub_pert_3 = {}
    ben_no_pert_4 = {}
    ben_sing_pert_4 = {}
    ben_doub_pert_4 = {}
    mal_no_pert_1 = {}
    mal_sing_pert_1 = {}
    mal_doub_pert_1 = {}
    mal_no_pert_2 = {}
    mal_sing_pert_2 = {}
    mal_doub_pert_2 = {}
    mal_no_pert_3 = {}
    mal_sing_pert_3 = {}
    mal_doub_pert_3 = {}
    mal_no_pert_4 = {}
    mal_sing_pert_4 = {}
    mal_doub_pert_4 = {}

    for i in range(len(simulation_data)):
        progressbar.update(i, len(simulation_data))
        sim_data = simulation_data.iloc[i]
        input_condi = [sim_data['Input_GFs'], sim_data['Input_Hypoxia'], sim_data['Input_Mutagen'],
                       sim_data['Input_Nutrients'], sim_data['Input_TNFalpha']]
        if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
            if (str(sim_data['Perturbation2']) == 'nan'):
                no_pert_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                if len(no_pert) == 0:
                    no_pert = [no_pert_data]
                elif len(no_pert) > 0:
                    no_pert.append(no_pert_data)
        if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
            if (str(sim_data['Perturbation2']) == 'nan'):
                sing_pert_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                if len(sing_pert) == 0:
                    sing_pert = [sing_pert_data]
                elif len(sing_pert) > 0:
                    sing_pert.append(sing_pert_data)
            elif (str(sim_data['Perturbation2']) != 'nan'):
                doub_pert_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                if len(doub_pert) == 0:
                    doub_pert = [doub_pert_data]
                elif len(doub_pert) > 0:
                    doub_pert.append(doub_pert_data)

        if (input_condi[1] == 0) & (input_condi[2] == 0) & (input_condi[3] == 1):
            if (input_condi[0] == 0) & (input_condi[4] == 0):
                if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        ben_no_pert_1_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_no_pert_1) == 0:
                            ben_no_pert_1 = [ben_no_pert_1_data]
                        elif len(ben_no_pert_1) > 0:
                            ben_no_pert_1.append(ben_no_pert_1_data)
                if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        ben_sing_pert_1_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_sing_pert_1) == 0:
                            ben_sing_pert_1 = [ben_sing_pert_1_data]
                        elif len(ben_sing_pert_1) > 0:
                            ben_sing_pert_1.append(ben_sing_pert_1_data)
                    elif (str(sim_data['Perturbation2']) != 'nan'):
                        ben_doub_pert_1_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_doub_pert_1) == 0:
                            ben_doub_pert_1 = [ben_doub_pert_1_data]
                        elif len(ben_doub_pert_1) > 0:
                            ben_doub_pert_1.append(ben_doub_pert_1_data)
            if (input_condi[0] == 0) & (input_condi[4] == 1):
                if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        ben_no_pert_2_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_no_pert_2) == 0:
                            ben_no_pert_2 = [ben_no_pert_2_data]
                        elif len(ben_no_pert_2) > 0:
                            ben_no_pert_2.append(ben_no_pert_2_data)
                if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        ben_sing_pert_2_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_sing_pert_2) == 0:
                            ben_sing_pert_2 = [ben_sing_pert_2_data]
                        elif len(ben_sing_pert_2) > 0:
                            ben_sing_pert_2.append(ben_sing_pert_2_data)
                    elif (str(sim_data['Perturbation2']) != 'nan'):
                        ben_doub_pert_2_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_doub_pert_2) == 0:
                            ben_doub_pert_2 = [ben_doub_pert_2_data]
                        elif len(ben_doub_pert_2) > 0:
                            ben_doub_pert_2.append(ben_doub_pert_2_data)
            if (input_condi[0] == 1) & (input_condi[4] == 0):
                if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        ben_no_pert_3_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_no_pert_3) == 0:
                            ben_no_pert_3 = [ben_no_pert_3_data]
                        elif len(ben_no_pert_3) > 0:
                            ben_no_pert_3.append(ben_no_pert_3_data)
                if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        ben_sing_pert_3_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_sing_pert_3) == 0:
                            ben_sing_pert_3 = [ben_sing_pert_3_data]
                        elif len(ben_sing_pert_3) > 0:
                            ben_sing_pert_3.append(ben_sing_pert_3_data)
                    elif (str(sim_data['Perturbation2']) != 'nan'):
                        ben_doub_pert_3_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_doub_pert_3) == 0:
                            ben_doub_pert_3 = [ben_doub_pert_3_data]
                        elif len(ben_doub_pert_3) > 0:
                            ben_doub_pert_3.append(ben_doub_pert_3_data)
            if (input_condi[0] == 1) & (input_condi[4] == 1):
                if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        ben_no_pert_4_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_no_pert_4) == 0:
                            ben_no_pert_4 = [ben_no_pert_4_data]
                        elif len(ben_no_pert_4) > 0:
                            ben_no_pert_4.append(ben_no_pert_4_data)
                if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        ben_sing_pert_4_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_sing_pert_4) == 0:
                            ben_sing_pert_4 = [ben_sing_pert_4_data]
                        elif len(ben_sing_pert_4) > 0:
                            ben_sing_pert_4.append(ben_sing_pert_4_data)
                    elif (str(sim_data['Perturbation2']) != 'nan'):
                        ben_doub_pert_4_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(ben_doub_pert_4) == 0:
                            ben_doub_pert_4 = [ben_doub_pert_4_data]
                        elif len(ben_doub_pert_4) > 0:
                            ben_doub_pert_4.append(ben_doub_pert_4_data)

        elif (input_condi[1] == 1) & (input_condi[2] == 1) & (input_condi[3] == 0):
            if (input_condi[0] == 0) & (input_condi[4] == 0):
                if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        mal_no_pert_1_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_no_pert_1) == 0:
                            mal_no_pert_1 = [mal_no_pert_1_data]
                        elif len(mal_no_pert_1) > 0:
                            mal_no_pert_1.append(mal_no_pert_1_data)
                if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        mal_sing_pert_1_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_sing_pert_1) == 0:
                            mal_sing_pert_1 = [mal_sing_pert_1_data]
                        elif len(mal_sing_pert_1) > 0:
                            mal_sing_pert_1.append(mal_sing_pert_1_data)
                    elif (str(sim_data['Perturbation2']) != 'nan'):
                        mal_doub_pert_1_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_doub_pert_1) == 0:
                            mal_doub_pert_1 = [mal_doub_pert_1_data]
                        elif len(mal_doub_pert_1) > 0:
                            mal_doub_pert_1.append(mal_doub_pert_1_data)
            if (input_condi[0] == 0) & (input_condi[4] == 1):
                if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        mal_no_pert_2_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_no_pert_2) == 0:
                            mal_no_pert_2 = [mal_no_pert_2_data]
                        elif len(mal_no_pert_2) > 0:
                            mal_no_pert_2.append(mal_no_pert_2_data)
                if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        mal_sing_pert_2_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_sing_pert_2) == 0:
                            mal_sing_pert_2 = [mal_sing_pert_2_data]
                        elif len(mal_sing_pert_2) > 0:
                            mal_sing_pert_2.append(mal_sing_pert_2_data)
                    elif (str(sim_data['Perturbation2']) != 'nan'):
                        mal_doub_pert_2_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_doub_pert_2) == 0:
                            mal_doub_pert_2 = [mal_doub_pert_2_data]
                        elif len(mal_doub_pert_2) > 0:
                            mal_doub_pert_2.append(mal_doub_pert_2_data)
            if (input_condi[0] == 1) & (input_condi[4] == 0):
                if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        mal_no_pert_3_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_no_pert_3) == 0:
                            mal_no_pert_3 = [mal_no_pert_3_data]
                        elif len(mal_no_pert_3) > 0:
                            mal_no_pert_3.append(mal_no_pert_3_data)
                if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        mal_sing_pert_3_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_sing_pert_3) == 0:
                            mal_sing_pert_3 = [mal_sing_pert_3_data]
                        elif len(mal_sing_pert_3) > 0:
                            mal_sing_pert_3.append(mal_sing_pert_3_data)
                    elif (str(sim_data['Perturbation2']) != 'nan'):
                        mal_doub_pert_3_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_doub_pert_3) == 0:
                            mal_doub_pert_3 = [mal_doub_pert_3_data]
                        elif len(mal_doub_pert_3) > 0:
                            mal_doub_pert_3.append(mal_doub_pert_3_data)
            if (input_condi[0] == 1) & (input_condi[4] == 1):
                if ((str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        mal_no_pert_4_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_no_pert_4) == 0:
                            mal_no_pert_4 = [mal_no_pert_4_data]
                        elif len(mal_no_pert_4) > 0:
                            mal_no_pert_4.append(mal_no_pert_4_data)
                if ((str(sim_data['Perturbation1']) != 'nan') & (str(sim_data['Perturbation1']) != 'S_Gli')):
                    if (str(sim_data['Perturbation2']) == 'nan'):
                        mal_sing_pert_4_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_sing_pert_4) == 0:
                            mal_sing_pert_4 = [mal_sing_pert_4_data]
                        elif len(mal_sing_pert_4) > 0:
                            mal_sing_pert_4.append(mal_sing_pert_4_data)
                    elif (str(sim_data['Perturbation2']) != 'nan'):
                        mal_doub_pert_4_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                        if len(mal_doub_pert_4) == 0:
                            mal_doub_pert_4 = [mal_doub_pert_4_data]
                        elif len(mal_doub_pert_4) > 0:
                            mal_doub_pert_4.append(mal_doub_pert_4_data)
        i += 1
    set_trace()
    scale = 1
    figure, total_plot = ternary.figure(scale=scale)
    total_plot.boundary(linewidth=2.0)
    total_plot.gridlines(color="blue", multiple=0.05)
    fontsize = 20
    total_plot.set_title("Total Distribution", fontsize=fontsize)
    total_plot.left_axis_label("Quiescent", fontsize=10)
    total_plot.right_axis_label("Apoptosis", fontsize=10)
    total_plot.bottom_axis_label("Proliferation", fontsize=10)
    total_plot.scatter(no_pert, marker='s', color='blue', label="No perturbation")
    total_plot.scatter(sing_pert, marker='s', color='red', label="Single perturbation")
    total_plot.scatter(doub_pert, marker='s', color='green', label="Double perturbation")
    total_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    total_plot.legend()
    #figure.savefig('Total distribution.png')

    figure, ben_no_pert = ternary.figure(scale=scale)
    ben_no_pert.boundary(linewidth=2.0)
    ben_no_pert.gridlines(color="blue", multiple=0.05)
    ben_no_pert.set_title("Beign tumor cell with no perturbation", fontsize=fontsize)
    ben_no_pert.left_axis_label("Quiescent", fontsize=10)
    ben_no_pert.right_axis_label("Apoptosis", fontsize=10)
    ben_no_pert.bottom_axis_label("Proliferation", fontsize=10)
    ben_no_pert.scatter(ben_no_pert_1, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
    ben_no_pert.scatter(ben_no_pert_2, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
    ben_no_pert.scatter(ben_no_pert_3, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
    ben_no_pert.scatter(ben_no_pert_4, marker='s', color='yellow', label="GFs = 1, TNFalpha = 1")
    ben_no_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
    ben_no_pert.legend()
    #figure.savefig('Benign tumor cell with no perturbation.png')

    figure, ben_sing_pert = ternary.figure(scale=scale)
    ben_sing_pert.boundary(linewidth=2.0)
    ben_sing_pert.gridlines(color="blue", multiple=0.05)
    ben_sing_pert.set_title("Beign tumor cell with single perturbation", fontsize=fontsize)
    ben_sing_pert.left_axis_label("Quiescent", fontsize=10)
    ben_sing_pert.right_axis_label("Apoptosis", fontsize=10)
    ben_sing_pert.bottom_axis_label("Proliferation", fontsize=10)
    ben_sing_pert.scatter(ben_sing_pert_1, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
    ben_sing_pert.scatter(ben_sing_pert_2, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
    ben_sing_pert.scatter(ben_sing_pert_3, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
    ben_sing_pert.scatter(ben_sing_pert_4, marker='s', color='yellow', label="GFs = 1, TNFalpha = 1")
    ben_sing_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
    ben_sing_pert.legend()
    #figure.savefig('Benign tumor cell with single perturbation.png')

    figure, ben_doub_pert = ternary.figure(scale=scale)
    ben_doub_pert.boundary(linewidth=2.0)
    ben_doub_pert.gridlines(color="blue", multiple=0.05)
    ben_doub_pert.set_title("Beign tumor cell with double perturbation", fontsize=fontsize)
    ben_doub_pert.left_axis_label("Quiescent", fontsize=10)
    ben_doub_pert.right_axis_label("Apoptosis", fontsize=10)
    ben_doub_pert.bottom_axis_label("Proliferation", fontsize=10)
    ben_doub_pert.scatter(ben_doub_pert_1, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
    ben_doub_pert.scatter(ben_doub_pert_2, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
    ben_doub_pert.scatter(ben_doub_pert_3, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
    ben_doub_pert.scatter(ben_doub_pert_4, marker='s', color='yellow', label="GFs = 1, TNFalpha = 1")
    ben_doub_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
    ben_doub_pert.legend()
    #figure.savefig('Benign tumor cell with double perturbation.png')

    figure, mal_no_pert = ternary.figure(scale=scale)
    mal_no_pert.boundary(linewidth=2.0)
    mal_no_pert.gridlines(color="blue", multiple=0.05)
    mal_no_pert.set_title("Malignt tumor cell with no perturbation", fontsize=fontsize)
    mal_no_pert.left_axis_label("Quiescent", fontsize=10)
    mal_no_pert.right_axis_label("Apoptosis", fontsize=10)
    mal_no_pert.bottom_axis_label("Proliferation", fontsize=10)
    mal_no_pert.scatter(mal_no_pert_1, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
    mal_no_pert.scatter(mal_no_pert_2, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
    mal_no_pert.scatter(mal_no_pert_3, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
    mal_no_pert.scatter(mal_no_pert_4, marker='s', color='yellow', label="GFs = 1, TNFalpha = 1")
    mal_no_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
    mal_no_pert.legend()
    #figure.savefig('Malignt tumor cell with no perturbation.png')

    figure, mal_sing_pert = ternary.figure(scale=scale)
    mal_sing_pert.boundary(linewidth=2.0)
    mal_sing_pert.gridlines(color="blue", multiple=0.05)
    mal_sing_pert.set_title("Malignt tumor cell with single perturbation", fontsize=fontsize)
    mal_sing_pert.left_axis_label("Quiescent", fontsize=10)
    mal_sing_pert.right_axis_label("Apoptosis", fontsize=10)
    mal_sing_pert.bottom_axis_label("Proliferation", fontsize=10)
    mal_sing_pert.scatter(mal_sing_pert_1, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
    mal_sing_pert.scatter(mal_sing_pert_2, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
    mal_sing_pert.scatter(mal_sing_pert_3, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
    mal_sing_pert.scatter(mal_sing_pert_4, marker='s', color='yellow', label="GFs = 1, TNFalpha = 1")
    mal_sing_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
    mal_sing_pert.legend()
    #figure.savefig('Malignt tumor cell with single perturbation.png')

    figure, mal_doub_pert = ternary.figure(scale=scale)
    mal_doub_pert.boundary(linewidth=2.0)
    mal_doub_pert.gridlines(color="blue", multiple=0.05)
    mal_doub_pert.set_title("Malignt tumor cell with double perturbation", fontsize=fontsize)
    mal_doub_pert.left_axis_label("Quiescent", fontsize=10)
    mal_doub_pert.right_axis_label("Apoptosis", fontsize=10)
    mal_doub_pert.bottom_axis_label("Proliferation", fontsize=10)
    mal_doub_pert.scatter(mal_doub_pert_1, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
    mal_doub_pert.scatter(mal_doub_pert_2, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
    mal_doub_pert.scatter(mal_doub_pert_3, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
    mal_doub_pert.scatter(mal_doub_pert_4, marker='s', color='yellow', label="GFs = 1, TNFalpha = 1")
    mal_doub_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
    mal_doub_pert.legend()
    #figure.savefig('Malignt tumor cell with double perturbation.png')

    figure, ben_1_plot = ternary.figure(scale=scale)
    ben_1_plot.boundary(linewidth=2.0)
    ben_1_plot.gridlines(color="blue", multiple=0.05)
    ben_1_plot.set_title("Benign Distribution (GFs = 0. TNFalpha = 0)", fontsize=fontsize)
    ben_1_plot.left_axis_label("Quiescent", fontsize=10)
    ben_1_plot.right_axis_label("Apoptosis", fontsize=10)
    ben_1_plot.bottom_axis_label("Proliferation", fontsize=10)
    ben_1_plot.scatter(ben_no_pert_1, marker='s', color='blue', label="No perturbation")
    ben_1_plot.scatter(ben_sing_pert_1, marker='s', color='red', label="Single perturbation")
    ben_1_plot.scatter(ben_doub_pert_1, marker='s', color='green', label="Double perturbation")
    ben_1_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    ben_1_plot.legend()
    #figure.savefig('Benign Distribution (GFs = 0. TNFalpha = 0).png')

    figure, ben_2_plot = ternary.figure(scale=scale)
    ben_2_plot.boundary(linewidth=2.0)
    ben_2_plot.gridlines(color="blue", multiple=0.05)
    ben_2_plot.set_title("Benign Distribution (GFs = 0. TNFalpha = 1)", fontsize=fontsize)
    ben_2_plot.left_axis_label("Quiescent", fontsize=15)
    ben_2_plot.right_axis_label("Apoptosis", fontsize=15)
    ben_2_plot.bottom_axis_label("Proliferation", fontsize=15)
    ben_2_plot.scatter(ben_no_pert_2, marker='s', color='blue', label="No perturbation")
    ben_2_plot.scatter(ben_sing_pert_2, marker='s', color='red', label="Single perturbation")
    ben_2_plot.scatter(ben_doub_pert_2, marker='s', color='green', label="Double perturbation")
    ben_2_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    ben_2_plot.legend()
    #figure.savefig('Benign Distribution (GFs = 0. TNFalpha = 1).png')

    figure, ben_3_plot = ternary.figure(scale=scale)
    ben_3_plot.boundary(linewidth=2.0)
    ben_3_plot.gridlines(color="blue", multiple=0.05)
    ben_3_plot.set_title("Benign Distribution (GFs = 1. TNFalpha = 0)", fontsize=fontsize)
    ben_3_plot.left_axis_label("Quiescent", fontsize=10)
    ben_3_plot.right_axis_label("Apoptosis", fontsize=10)
    ben_3_plot.bottom_axis_label("Proliferation", fontsize=10)
    ben_3_plot.scatter(ben_no_pert_3, marker='s', color='blue', label="No perturbation")
    ben_3_plot.scatter(ben_sing_pert_3, marker='s', color='red', label="Single perturbation")
    ben_3_plot.scatter(ben_doub_pert_3, marker='s', color='green', label="Double perturbation")
    ben_3_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    ben_3_plot.legend()
    #figure.savefig('Benign Distribution (GFs = 1. TNFalpha = 0).png')

    figure, ben_4_plot = ternary.figure(scale=scale)
    ben_4_plot.boundary(linewidth=2.0)
    ben_4_plot.gridlines(color="blue", multiple=0.05)
    ben_4_plot.set_title("Benign Distribution (GFs = 1. TNFalpha = 1)", fontsize=fontsize)
    ben_4_plot.left_axis_label("Quiescent", fontsize=10)
    ben_4_plot.right_axis_label("Apoptosis", fontsize=10)
    ben_4_plot.bottom_axis_label("Proliferation", fontsize=10)
    ben_4_plot.scatter(ben_no_pert_4, marker='s', color='blue', label="No perturbation")
    ben_4_plot.scatter(ben_sing_pert_4, marker='s', color='red', label="Single perturbation")
    ben_4_plot.scatter(ben_doub_pert_4, marker='s', color='green', label="Double perturbation")
    ben_4_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    ben_4_plot.legend()
    #figure.savefig('Benign Distribution (GFs = 1. TNFalpha = 1).png')

    figure, mal_1_plot = ternary.figure(scale=scale)
    mal_1_plot.boundary(linewidth=2.0)
    mal_1_plot.gridlines(color="blue", multiple=0.05)
    mal_1_plot.set_title("Malignant Distribution (GFs = 0. TNFalpha = 0)", fontsize=fontsize)
    mal_1_plot.left_axis_label("Quiescent", fontsize=10)
    mal_1_plot.right_axis_label("Apoptosis", fontsize=10)
    mal_1_plot.bottom_axis_label("Proliferation", fontsize=10)
    mal_1_plot.scatter(mal_no_pert_1, marker='s', color='blue', label="No perturbation")
    mal_1_plot.scatter(mal_sing_pert_1, marker='s', color='red', label="Single perturbation")
    mal_1_plot.scatter(mal_doub_pert_1, marker='s', color='green', label="Double perturbation")
    mal_1_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    mal_1_plot.legend()
    #figure.savefig('Malignant Distribution (GFs = 0. TNFalpha = 0).png')

    figure, mal_2_plot = ternary.figure(scale=scale)
    mal_2_plot.boundary(linewidth=2.0)
    mal_2_plot.gridlines(color="blue", multiple=0.05)
    mal_2_plot.set_title("Malignant Distribution (GFs = 0. TNFalpha = 1)", fontsize=fontsize)
    mal_2_plot.left_axis_label("Quiescent", fontsize=10)
    mal_2_plot.right_axis_label("Apoptosis", fontsize=10)
    mal_2_plot.bottom_axis_label("Proliferation", fontsize=10)
    mal_2_plot.scatter(mal_no_pert_2, marker='s', color='blue', label="No perturbation")
    mal_2_plot.scatter(mal_sing_pert_2, marker='s', color='red', label="Single perturbation")
    mal_2_plot.scatter(mal_doub_pert_2, marker='s', color='green', label="Double perturbation")
    mal_2_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    mal_2_plot.legend()
    #figure.savefig('Malignant Distribution (GFs = 0. TNFalpha = 1).png')

    figure, mal_3_plot = ternary.figure(scale=scale)
    mal_3_plot.boundary(linewidth=2.0)
    mal_3_plot.gridlines(color="blue", multiple=0.05)
    mal_3_plot.set_title("Malignant Distribution (GFs = 1. TNFalpha = 0)", fontsize=fontsize)
    mal_3_plot.left_axis_label("Quiescent", fontsize=15)
    mal_3_plot.right_axis_label("Apoptosis", fontsize=15)
    mal_3_plot.bottom_axis_label("Proliferation", fontsize=15)
    mal_3_plot.scatter(mal_no_pert_3, marker='s', color='blue', label="No perturbation")
    mal_3_plot.scatter(mal_sing_pert_3, marker='s', color='red', label="Single perturbation")
    mal_3_plot.scatter(mal_doub_pert_3, marker='s', color='blue', label="Double perturbation")
    mal_3_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    mal_3_plot.legend()
    #figure.savefig('Malignant Distribution (GFs = 1. TNFalpha = 0).png')

    figure, mal_4_plot = ternary.figure(scale=scale)
    mal_4_plot.boundary(linewidth=2.0)
    mal_4_plot.gridlines(color="blue", multiple=0.05)
    mal_4_plot.set_title("Malignant Distribution (GFs = 1. TNFalpha = 1)", fontsize=fontsize)
    mal_4_plot.left_axis_label("Quiescent", fontsize=15)
    mal_4_plot.right_axis_label("Apoptosis", fontsize=15)
    mal_4_plot.bottom_axis_label("Proliferation", fontsize=15)
    mal_4_plot.scatter(mal_no_pert_4, marker='s', color='blue', label="No perturbation")
    mal_4_plot.scatter(mal_sing_pert_4, marker='s', color='red', label="Single perturbation")
    mal_4_plot.scatter(mal_doub_pert_4, marker='s', color='blue', label="Double perturbation")
    mal_4_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
    mal_4_plot.legend()
    #figure.savefig('Malignant Distribution (GFs = 1. TNFalpha = 1).png')
    mal_4_plot.show()



    #with open(config['output']['a'], 'w') as fobj:
    #    fobj.write('hello')
