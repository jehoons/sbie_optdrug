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
                total_attractor.loc[i,'Apoptosis'] = apo_basin
                total_attractor.loc[i, 'Proliferation'] = pro_basin
                total_attractor.loc[i, 'Quiescent'] = qui_basin
                #total_attractor.loc[i, 'Apoptosis-proliferation'] = apopro_basin
            else:
                total_attractor.loc[i, 'Apoptosis'] = 0
                total_attractor.loc[i, 'Proliferation'] = 0
                total_attractor.loc[i, 'Quiescent'] = 0
                #total_attractor.loc[i, 'Apoptosis-proliferation'] = 0
            total_attractor.loc[i, 'Distance'] = math.sqrt(math.pow(1-apo_basin,2)+math.pow(pro_basin,2)+math.pow(qui_basin,2))

        i += 1
    total_attractor.to_csv(config['output']['output_b'], index=False)

    set_trace()

    simulation_data = total_attractor

    no_pert = simulation_data[
        (str(simulation_data['Perturbation1']) == 'nan') & (str(simulation_data['Perturbation2']) == 'nan')]
    no_pert_Gli = simulation_data[
        (str(simulation_data['Perturbation1']) == 'S_Gli') & (str(simulation_data['Perturbation2']) == 'nan')]
    no_pert_total = no_pert
    no_pert_total.append(no_pert_Gli)

    benign_1 = simulation_data[(simulation_data['Input_GFs'] == 0) & (simulation_data['Input_Hypoxia'] == 0) & (
    simulation_data['Input_Mutagen'] == 0) &
                               (simulation_data['Input_Nutrients'] == 1) & (simulation_data['Input_TNFalpha'] == 0)]
    benign_no1 = benign_1[(str(benign_1['Perturbation1']) == 'nan') & (str(benign_1['Perturbation2']) == 'nan')]
    benign_no1_loc = [benign_no1['Quiescent'], benign_no1['Proliferation'], benign_no1['Apoptosis']]
    benign_Gli1 = benign_1[(str(benign_1['Perturbation1']) == 'S_Gli') & (str(benign_1['Perturbation2']) == 'nan')]
    benign_Gli1_loc = [benign_Gli1['Quiescent'], benign_Gli1['Proliferation'], benign_Gli1['Apoptosis']]
    benign_no_total1_loc = benign_no1_loc
    benign_no_total1_loc.append(benign_Gli1_loc)

    benign_2 = simulation_data[(simulation_data['Input_GFs'] == 0) & (simulation_data['Input_Hypoxia'] == 0) & (
    simulation_data['Input_Mutagen'] == 0) &
                               (simulation_data['Input_Nutrients'] == 1) & (simulation_data['Input_TNFalpha'] == 1)]
    benign_3 = simulation_data[(simulation_data['Input_GFs'] == 1) & (simulation_data['Input_Hypoxia'] == 0) & (
    simulation_data['Input_Mutagen'] == 0) &
                               (simulation_data['Input_Nutrients'] == 1) & (simulation_data['Input_TNFalpha'] == 0)]
    benign_4 = simulation_data[(simulation_data['Input_GFs'] == 1) & (simulation_data['Input_Hypoxia'] == 0) & (
    simulation_data['Input_Mutagen'] == 0) &
                               (simulation_data['Input_Nutrients'] == 1) & (simulation_data['Input_TNFalpha'] == 1)]

    malig_1 = simulation_data[(simulation_data['Input_GFs'] == 0) & (simulation_data['Input_Hypoxia'] == 1) & (
    simulation_data['Input_Mutagen'] == 1) &
                              (simulation_data['Input_Nutrients'] == 0) & (simulation_data['Input_TNFalpha'] == 0)]
    malig_2 = simulation_data[(simulation_data['Input_GFs'] == 0) & (simulation_data['Input_Hypoxia'] == 1) & (
    simulation_data['Input_Mutagen'] == 1) &
                              (simulation_data['Input_Nutrients'] == 0) & (simulation_data['Input_TNFalpha'] == 1)]
    malig_3 = simulation_data[(simulation_data['Input_GFs'] == 1) & (simulation_data['Input_Hypoxia'] == 1) & (
    simulation_data['Input_Mutagen'] == 1) &
                              (simulation_data['Input_Nutrients'] == 0) & (simulation_data['Input_TNFalpha'] == 0)]
    malig_4 = simulation_data[(simulation_data['Input_GFs'] == 1) & (simulation_data['Input_Hypoxia'] == 1) & (
    simulation_data['Input_Mutagen'] == 1) &
                              (simulation_data['Input_Nutrients'] == 0) & (simulation_data['Input_TNFalpha'] == 1)]

    i = 0
    no_pert = {}
    ben_pert_no_tot = {}
    for i in range(len(simulation_data)):
        progressbar.update(i, len(simulation_data))
        sim_data = simulation_data.iloc[i]
        input_condi = [sim_data['Input_GFs'], sim_data['Input_Hypoxia'], sim_data['Input_Mutagen'],
                       sim_data['Input_Nutrients'], sim_data['Input_TNFalpha']]
        if (str(sim_data['Perturbation1']) == 'nan') | (str(sim_data['Perturbation1']) == 'S_Gli'):
            if str(sim_data['Perturbation2']) == 'nan':
                no_pert_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                if len(no_pert) == 0:
                    no_pert = [no_pert_data]
                elif len(no_pert) > 0:
                    no_pert.append(no_pert_data)
        if (input_condi[1] == 0) & (input_condi[2] == 0) & (input_condi[3] == 1):
            if str(sim_data['Perturbation1']) == 'nan' | (str(sim_data['Perturbation1']) == 'S_Gli'):
                if str(sim_data['Perturbation2']) == 'nan':
                    ben_pert_no_total = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(ben_pert_no_total) == 0:
                        ben_pert_no_tot = [ben_pert_no_total]
                    elif len(ben_pert_no_total) > 0:
                        ben_pert_no_tot.append(ben_pert_no_total)
            if (input_condi[0] == 0) & (input_condi[4] == 0):
                if str(sim_data['Perturbation1']) == 'nan' | (str(sim_data['Perturbation1']) == 'S_Gli'):
                    if str(sim_data['Perturbation2']) == 'nan':
                        ben_pert_no1 = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
            elif (input_condi[0] == 0) & (input_condi[4] == 1):
                if str(sim_data['Perturbation1']) == 'nan'| (str(sim_data['Perturbation1']) == 'S_Gli'):
                    if str(sim_data['Perturbation2']) == 'nan':
                        ben_pert_no2 = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
            elif (input_condi[0] == 1) & (input_condi[4] == 0):
                if str(sim_data['Perturbation1']) == 'nan' | (str(sim_data['Perturbation1']) == 'S_Gli'):
                    if str(sim_data['Perturbation2']) == 'nan':
                        ben_pert_no3 = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
            elif (input_condi[0] == 1) & (input_condi[4] == 1):
                if str(sim_data['Perturbation1']) == 'nan' | (str(sim_data['Perturbation1']) == 'S_Gli'):
                    if str(sim_data['Perturbation2']) == 'nan':
                        ben_pert_no4 = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
        elif (input_condi[1] == 1) & (input_condi[2] == 1) & (input_condi[3] == 0):
            if str(sim_data['Perturbation1']) == 'nan' | (str(sim_data['Perturbation1']) == 'S_Gli'):
                if str(sim_data['Perturbation2']) == 'nan':
                    malig_pert_no_total = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
            if (input_condi[0] == 0) & (input_condi[4] == 0):
                if str(sim_data['Perturbation1']) == 'nan'| (str(sim_data['Perturbation1']) == 'S_Gli'):
                    if str(sim_data['Perturbation2']) == 'nan':
                        malig_pert_no1 = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
            elif (input_condi[0] == 0) & (input_condi[4] == 1):
                if str(sim_data['Perturbation1']) == 'nan' | (str(sim_data['Perturbation1']) == 'S_Gli'):
                    if str(sim_data['Perturbation2']) == 'nan':
                        malig_pert_no2 = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
            elif (input_condi[0] == 1) & (input_condi[4] == 0):
                if str(sim_data['Perturbation1']) == 'nan' | (str(sim_data['Perturbation1']) == 'S_Gli'):
                    if str(sim_data['Perturbation2']) == 'nan':
                        malig_pert_no3 = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
            elif (input_condi[0] == 1) & (input_condi[4] == 1):
                if str(sim_data['Perturbation1']) == 'nan' | (str(sim_data['Perturbation1']) == 'S_Gli'):
                    if str(sim_data['Perturbation2']) == 'nan':
                        malig_pert_no4 = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]

    scale = 1
    figure, bengign_no_per = ternary.figure(scale=scale)

    bengign_no_per.boundary(linewidth=2.0)
    bengign_no_per.gridlines(color="blue", multiple=0.05)

    fontsize = 20
    bengign_no_per.set_title("Benign tumor with no perturbation", fontsize=fontsize)
    bengign_no_per.left_axis_label("Quiescent", fontsize=15)
    bengign_no_per.right_axis_label("Apoptosis", fontsize=15)
    bengign_no_per.bottom_axis_label("Proliferation", fontsize=15)

    bengign_no_per.scatter([ben_pert_no1, ben_pert_no2, ben_pert_no3, ben_pert_no4], marker='s', color='red',
                           label="Red Squares")
    bengign_no_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
    bengign_no_per.legend()
    figure.savefig('Benign_with_no_perturbation.png')
    # bengign_no_per.show()


    figure, malig_no_per = ternary.figure(scale=scale)

    malig_no_per.boundary(linewidth=2.0)
    malig_no_per.gridlines(color="blue", multiple=0.05)

    fontsize = 20
    malig_no_per.set_title("Malignant tumor with no perturbation", fontsize=fontsize)
    malig_no_per.left_axis_label("Quiescent", fontsize=15)
    malig_no_per.right_axis_label("Apoptosis", fontsize=15)
    malig_no_per.bottom_axis_label("Proliferation", fontsize=15)

    malig_no_per.scatter([malig_pert_no1, malig_pert_no2, malig_pert_no3, malig_pert_no4], marker='s', color='red',
                         label="Red Squares")
    malig_no_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
    malig_no_per.legend()
    figure.savefig('Malignant_with_no_perturbation.png')

    figure, bengign_per = ternary.figure(scale=scale)

    ben_drug1_data = simulation_data.iloc[17979]
    ben_drug1 = [ben_drug1_data['Quiescent'], ben_drug1_data['Proliferation'], ben_drug1_data['Apoptosis']]

    ben_drug2_data = simulation_data.iloc[17375]
    ben_drug2 = [ben_drug2_data['Quiescent'], ben_drug2_data['Proliferation'], ben_drug2_data['Apoptosis']]

    ben_drug3_data = simulation_data.iloc[17943]
    ben_drug3 = [ben_drug3_data['Quiescent'], ben_drug3_data['Proliferation'], ben_drug3_data['Apoptosis']]

    bengign_per.boundary(linewidth=2.0)
    bengign_per.gridlines(color="blue", multiple=0.05)

    fontsize = 20
    bengign_per.set_title("Benign tumor with perturbation", fontsize=fontsize)
    bengign_per.left_axis_label("Quiescent", fontsize=15)
    bengign_per.right_axis_label("Apoptosis", fontsize=15)
    bengign_per.bottom_axis_label("Proliferation", fontsize=15)

    bengign_per.line(ben_pert_no1, ben_drug1, linewidth=3., marker='s', color='green')
    bengign_per.line(ben_pert_no1, ben_drug2, linewidth=3., marker='s', color='red', linestyle=":")
    bengign_per.line(ben_pert_no1, ben_drug3, linewidth=3., marker='s', color='blue', linestyle=":")
    bengign_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
    bengign_per.legend()
    figure.savefig('Benign_with_perturbation.png')
    # bengign_per.show()

    figure, malig_per = ternary.figure(scale=scale)

    malig_drug1_data = simulation_data.iloc[72374]
    malig_drug1 = [malig_drug1_data['Quiescent'], malig_drug1_data['Proliferation'], malig_drug1_data['Apoptosis']]

    malig_drug2_data = simulation_data.iloc[105891]
    malig_drug2 = [malig_drug2_data['Quiescent'], malig_drug2_data['Proliferation'], malig_drug2_data['Apoptosis']]

    malig_drug3_data = simulation_data.iloc[106926]
    malig_drug3 = [malig_drug3_data['Quiescent'], malig_drug3_data['Proliferation'], malig_drug3_data['Apoptosis']]

    malig_per.boundary(linewidth=2.0)
    malig_per.gridlines(color="blue", multiple=0.05)

    fontsize = 20
    malig_per.set_title("Malignant tumor with perturbation", fontsize=fontsize)
    malig_per.left_axis_label("Quiescent", fontsize=15)
    malig_per.right_axis_label("Apoptosis", fontsize=15)
    malig_per.bottom_axis_label("Proliferation", fontsize=15)

    malig_per.scatter([malig_pert_no1, malig_drug1], marker='D', color='green')
    malig_per.line(malig_pert_no1, malig_drug2, linewidth=3., marker='s', color='red', linestyle=":")
    malig_per.line(malig_pert_no1, malig_drug3, linewidth=3., marker='s', color='blue', linestyle=":")
    malig_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
    malig_per.legend()
    figure.savefig('Malignant_with_perturbation.png')
    # malig_per.show()

    scale = 1
    figure, no_per = ternary.figure(scale=scale)

    no_per.boundary(linewidth=2.0)
    no_per.gridlines(color="blue", multiple=0.05)

    fontsize = 20
    no_per.set_title("No perturbation", fontsize=fontsize)
    no_per.left_axis_label("Quiescent", fontsize=15)
    no_per.right_axis_label("Apoptosis", fontsize=15)
    no_per.bottom_axis_label("Proliferation", fontsize=15)

    no_per.scatter(no_pert, marker='s', color='red', label="Red Squares")
    no_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
    no_per.legend()
    figure.savefig('No_perturbation.png')
    no_per.show()
    # malig_no_per.show()

    # scale = 1
    # figure, tax = ternary.figure(scale=scale)
    #
    # tax.boundary(linewidth=2.0)
    # # tax.gridlines(color = "black", multiple = 0.1)
    # tax.gridlines(color="blue", multiple=0.05)
    #
    # fontsize = 10
    # tax.set_title("", fontsize=fontsize)
    # tax.left_axis_label("Quiescent", fontsize=fontsize)
    # tax.right_axis_label("Apoptosis", fontsize=fontsize)
    # tax.bottom_axis_label("Proliferation", fontsize=fontsize)
    #
    #
    # i = 0
    # for i in range(len(total_attractor)):
    #     print(0)


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
