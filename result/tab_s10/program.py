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
outputfile_b = join(dirname(__file__), 'TABLE.S8B_total_attractor_input_condition.csv')
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
        'output_b': outputfile_b,
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
    total_attractor = pd.DataFrame([], columns=['Input_GFs', 'Input_Gli', 'Input_Hypoxia', 'Input_Mutagen',
                                               'Input_Nutrients', 'Input_TNFalpha', 'Perturbation1', 'Perturbation2',
                                               'Apoptosis', 'Proliferation', 'Quiescent', 'Apoptosis-proliferation',
                                                'Total', 'Attractor'])

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
                        if ((att_cycle_state[pro_qui_1] == '1') | (att_cycle_state[pro_qui_2] == '1') | (
                            att_cycle_state[pro_qui_3] == '1') | (att_cycle_state[pro_qui_4] == '1')):
                            att_condi.loc[k, 'Phenotype'] = 'Proliferation'
                        elif ((att_cycle_state[pro_qui_1] == '0') & (att_cycle_state[pro_qui_2] == '0') & (
                            att_cycle_state[pro_qui_3] == '0') & (att_cycle_state[pro_qui_4] == '0')):
                            att_condi.loc[k, 'Phenotype'] = 'Quiescent'
                        ii += 1
                        k += 1

            att_condi_apo = att_condi[att_condi['Phenotype'] == 'Apoptosis']
            #att_condi_apopro = att_condi[att_condi['Phenotype'] == 'Apoptosis-Proliferation']
            att_condi_pro = att_condi[att_condi['Phenotype'] == 'Proliferation']
            att_condi_qui = att_condi[att_condi['Phenotype'] == 'Quiescent']
            total_basin = sum(att_condi['Ratio'])
            if total_basin != 0:
                apo_basin = sum(att_condi_apo['Ratio'])/total_basin
                #apopro_basin = sum(att_condi_apopro['Ratio'])/total_basin
                pro_basin = sum(att_condi_pro['Ratio'])/total_basin
                qui_basin = sum(att_condi_qui['Ratio'])/total_basin
            total_attractor.loc[i,'Apoptosis'] = apo_basin
            total_attractor.loc[i, 'Proliferation'] = pro_basin
            total_attractor.loc[i, 'Quiescent'] = qui_basin
            #total_attractor.loc[i, 'Apoptosis-proliferation'] = apopro_basin
            total_attractor.loc[i, 'Total'] = total_basin
        i += 1
    total_attractor.to_csv(config['output']['output_b'], index=False)
    set_trace()


            # j = 0
            # if len(att_condi_cyc) > 0:
            #     for j in range(len(att_condi_cyc)):
            #         att_no = att_condi_cyc.loc[j, 'Attractor_No']
            #         if len(att_no) > 0:
            #             att_ratio = att_condi_cyc.loc[j, 'Ratio']
            #             att_phe = att_condi_cyc.loc[j, 'Phenotype']
            #         elif len(att_no) == 0:
            #             if len(att_condi_cyc.loc[j-1, 'Attractor_No']) > 0:
            #                 if att_phe != att_condi_cyc.loc[j-1, 'Phenotype']:
            #                     print(0)
            #         j += 1




    #     input_state = {'on': {}, 'off': {}}
    #     ano_state = {'on': {}, 'off': {}}
    #     if len(off_state) > 0 :
    #         j = 0
    #         input_off = {}
    #         ano_off = {}
    #         for j in range(len(off_state)):
    #             off_state_node = off_state[j]
    #             if off_state_node in input_nodes:
    #                 if len(input_off) == 0:
    #                     input_off = [off_state_node]
    #                 elif len(input_off) != 0:
    #                     input_off.append(off_state_node)
    #             else:
    #                 if len(ano_off) == 0:
    #                     ano_off = [off_state_node]
    #                 elif len(ano_off) != 0:
    #                     ano_off.append(off_state_node)
    #             j += 1
    #         input_state['off'] = input_off
    #         ano_state['off'] = ano_off
    #
    #     if len(on_state) > 0 :
    #         j = 0
    #         input_on = {}
    #         ano_on = {}
    #         for j in range(len(on_state)):
    #             on_state_node = on_state[j]
    #             if on_state_node in input_nodes:
    #                 if len(input_on) == 0:
    #                     input_on = [on_state_node]
    #                 elif len(input_state) != 0:
    #                     input_on.append(on_state_node)
    #             else:
    #                 if len(ano_on) == 0:
    #                     ano_on = [on_state_node]
    #                 elif len(ano_on) != 0:
    #                     ano_on.append(on_state_node)
    #             j += 1
    #         input_state['on'] = input_on
    #         ano_state['on'] = ano_on
    #
    #     attractor = attractor_result['scanning_results'][i]['attractors']
    #     state_key = attractor_result['scanning_results'][i]['state_key']
    #     if len(attractor) > 0 :
    #         att_condi = {}
    #         for j in attractor.keys():
    #             #progressbar.update(i, len(attractor.keys()))
    #             att = attractor[j]
    #             phenotype = {'phenotype': {}}
    #             att = dict(att.items() + phenotype.items())
    #             if att['type'] == 'point':
    #                 att_state = state_key[j]
    #                 if att_state[apop] == '1':
    #                     att['phenotype'] = 'apoptosis'
    #                 elif (att_state[pro_qui_1] == '1') | (att_state[pro_qui_2] == '1') | (att_state[pro_qui_3] == '1') | (att_state[pro_qui_4] == '1'):
    #                     att['phenotype'] = 'proliferation'
    #                 elif (att_state[pro_qui_1] == '0') & (att_state[pro_qui_2] == '0') & (att_state[pro_qui_3] == '0') & (att_state[pro_qui_4] == '0'):
    #                     att['phenotype'] = 'quiescent'
    #                 att_put_in = {j: att}
    #
    #             elif att['type'] == 'cyclic':
    #                 k = 0
    #                 cyc_phe = []
    #                 for k in range(len(att['value'])):
    #                     att_cycle_value = att['value'][k]
    #                     att_cycle_state = state_key[att_cycle_value]
    #                     if att_cycle_state[apop] == '1':
    #                         if len(cyc_phe) == 0:
    #                             cyc_phe = ['apoptosis']
    #                         else:
    #                             cyc_phe.append('apoptosis')
    #                     elif (att_cycle_state[pro_qui_1] == '1') | (att_cycle_state[pro_qui_2] == '1') | (att_cycle_state[pro_qui_3] == '1') | (att_cycle_state[pro_qui_4] == '1'):
    #                         if len(cyc_phe) == 0:
    #                             cyc_phe = ['proliferation']
    #                         else:
    #                             cyc_phe.append('proliferation')
    #                     elif (att_cycle_state[pro_qui_1] == 0) & (att_cycle_state[pro_qui_2] == 0) & (att_cycle_state[pro_qui_3] == 0) & (att_cycle_state[pro_qui_4] == 0):
    #                         if len(cyc_phe) == 0:
    #                             cyc_phe = ['quiescent']
    #                         else:
    #                             cyc_phe.append('quiescent')
    #                     k += 1
    #                 att['phenotype'] = cyc_phe
    #                 att_put_in = {j: att}
    #             if len(att_condi) == 0:
    #                 att_condi = att_put_in
    #             else:
    #                 att_condi = dict(att_condi.items()+att_put_in.items())
    #         data_attractor = {'input_node': input_state, 'node_perturbation': ano_state, 'attractor': att_condi,'attractor_state': state_key}
    #     data_put_in = {i: data_attractor}
    #     if len(total_data) == 0:
    #         total_data = data_put_in
    #     else:
    #         total_data = dict(total_data.items()+data_put_in.items())
    #     i += 1
    # json.dump(total_data, total_attractor_data, indent=3, sort_keys=True)
    # total_attractor_data.close()


    #with open(config['output']['a'], 'w') as fobj:
    #    fobj.write('hello')
