import json,re
import pickle
from os.path import dirname,join,exists
import sbie_optdrug
from sbie_optdrug.dataset import ccle,filelist
import pandas as pd
from ipdb import set_trace
from sbie_optdrug.dataset import ccle
from sbie_optdrug.result import tab_s1
from sbie_optdrug.result import tab_s2
from sbie_optdrug.result import tab_s5
from sbie_optdrug.result import tab_s10
import ternary
import math

import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#from boolean3 import Model
#from boolean3_addon import attractor
from termutil import progressbar
#import random

inputfile = join(dirname(tab_s2.__file__), 'TABLE.S2.NODE-NAME.CSV')
outputfile = join(dirname(tab_s1.__file__), 'TABLE.S1A.MUTCNA_CRC_NET.CSV')
outputfile1 = join(dirname(tab_s1.__file__), 'TABLE.S1B.THERAPY_CRC_NET.CSV')
outputfile2 = join(dirname(tab_s1.__file__), 'TABLE.S1C.NUM_MUTCNA.CSV')
outputfile3 = join(dirname(tab_s1.__file__), 'TABLE.S1D.NUM_DRUG.CSV')
outputfile4 = join(dirname(tab_s5.__file__), 'TABLE.S5A.COPYNUMVAR_data.json')
outputfile5 = join(dirname(tab_s5.__file__), 'TABLE.S5B.MUTATION_data.json')
outputfile6 = join(dirname(tab_s5.__file__), 'TABLE.S5C.DRUG_data.json')
outputfile7 = join(dirname(tab_s10.__file__), 'TABLE.S10B_total_attractor_input_condition_APC.csv')

config = {
    'input': inputfile,
    'output': outputfile,
    'output1': outputfile1,
    'output2': outputfile2,
    'output3': outputfile3,
    'output4': outputfile4,
    'output5': outputfile5,
    'output6': outputfile6,
    'output7': outputfile7,
    }

ccle_mutcna = ccle.mutcna()
ccle_therapy = ccle.therapy()
mutcna_col = ccle_mutcna.filter(regex='LARGE_INTESTINE')
ccle_therapy_col = ccle_therapy[ccle_therapy['CCLE Cell Line Name'].str.contains("LARGE_INTESTINE")]

gene = pd.read_csv(config['input'])
data_mutcna = pd.read_csv(config['output'])
data_therapy = pd.read_csv(config['output1'])
data_num_mutcna = pd.read_csv(config['output2'])
data_num_drug = pd.read_csv(config['output3'])
cnv_data = json.load(open(config['output4']),'rb')
mutation_data = json.load(open(config['output5']),'rb')
drug_data = json.load(open(config['output6']),'rb')
simulation_data = pd.read_csv(config['output7'])


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
    if (str(sim_data['Perturbation1']) == 'nan'):
        if (str(sim_data['Perturbation2']) == 'nan'):
            no_pert_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
            if len(no_pert) == 0:
                no_pert = [no_pert_data]
            elif len(no_pert) > 0:
                no_pert.append(no_pert_data)
    if (str(sim_data['Perturbation1']) != 'nan'):
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
            if (str(sim_data['Perturbation1']) == 'nan'):
                if (str(sim_data['Perturbation2']) == 'nan'):
                    ben_no_pert_1_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(ben_no_pert_1) == 0:
                        ben_no_pert_1 = [ben_no_pert_1_data]
                    elif len(ben_no_pert_1) > 0:
                        ben_no_pert_1.append(ben_no_pert_1_data)
            if (str(sim_data['Perturbation1']) != 'nan'):
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
            if (str(sim_data['Perturbation1']) == 'nan'):
                if (str(sim_data['Perturbation2']) == 'nan'):
                    ben_no_pert_2_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(ben_no_pert_2) == 0:
                        ben_no_pert_2 = [ben_no_pert_2_data]
                    elif len(ben_no_pert_2) > 0:
                        ben_no_pert_2.append(ben_no_pert_2_data)
            if (str(sim_data['Perturbation1']) != 'nan'):
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
            if (str(sim_data['Perturbation1']) == 'nan'):
                if (str(sim_data['Perturbation2']) == 'nan'):
                    ben_no_pert_3_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(ben_no_pert_3) == 0:
                        ben_no_pert_3 = [ben_no_pert_3_data]
                    elif len(ben_no_pert_3) > 0:
                        ben_no_pert_3.append(ben_no_pert_3_data)
            if (str(sim_data['Perturbation1']) != 'nan'):
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
            if (str(sim_data['Perturbation1']) == 'nan'):
                if (str(sim_data['Perturbation2']) == 'nan'):
                    ben_no_pert_4_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(ben_no_pert_4) == 0:
                        ben_no_pert_4 = [ben_no_pert_4_data]
                    elif len(ben_no_pert_4) > 0:
                        ben_no_pert_4.append(ben_no_pert_4_data)
            if (str(sim_data['Perturbation1']) != 'nan'):
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
            if (str(sim_data['Perturbation1']) == 'nan'):
                if (str(sim_data['Perturbation2']) == 'nan'):
                    mal_no_pert_1_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(mal_no_pert_1) == 0:
                        mal_no_pert_1 = [mal_no_pert_1_data]
                    elif len(mal_no_pert_1) > 0:
                        mal_no_pert_1.append(mal_no_pert_1_data)
            if (str(sim_data['Perturbation1']) != 'nan'):
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
            if (str(sim_data['Perturbation1']) == 'nan'):
                if (str(sim_data['Perturbation2']) == 'nan'):
                    mal_no_pert_2_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(mal_no_pert_2) == 0:
                        mal_no_pert_2 = [mal_no_pert_2_data]
                    elif len(mal_no_pert_2) > 0:
                        mal_no_pert_2.append(mal_no_pert_2_data)
            if (str(sim_data['Perturbation1']) != 'nan'):
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
            if (str(sim_data['Perturbation1']) == 'nan'):
                if (str(sim_data['Perturbation2']) == 'nan'):
                    mal_no_pert_3_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(mal_no_pert_3) == 0:
                        mal_no_pert_3 = [mal_no_pert_3_data]
                    elif len(mal_no_pert_3) > 0:
                        mal_no_pert_3.append(mal_no_pert_3_data)
            if (str(sim_data['Perturbation1']) != 'nan'):
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
            if (str(sim_data['Perturbation1']) == 'nan'):
                if (str(sim_data['Perturbation2']) == 'nan'):
                    mal_no_pert_4_data = [sim_data['Quiescent'], sim_data['Proliferation'], sim_data['Apoptosis']]
                    if len(mal_no_pert_4) == 0:
                        mal_no_pert_4 = [mal_no_pert_4_data]
                    elif len(mal_no_pert_4) > 0:
                        mal_no_pert_4.append(mal_no_pert_4_data)
            if (str(sim_data['Perturbation1']) != 'nan'):
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

scale = 1
figure, total_plot1 = ternary.figure(scale=scale)
#total_plot1.boundary(linewidth=2.0)
total_plot1.gridlines(color="blue", multiple=0.1)
fontsize = 15
total_plot1.set_title("Phenotype change when give one perturbation in TNFalpha off", fontsize=fontsize)
total_plot1.left_axis_label("Apoptosis", fontsize=10)
total_plot1.right_axis_label("Proliferation", fontsize=10)
total_plot1.bottom_axis_label("Quiescent", fontsize=10)
total_plot1.scatter(ben_sing_pert_1, alpha = 0.5, marker='s', color='blue', label = "GFs = 0, TNFalpha = 0")
total_plot1.scatter(ben_sing_pert_3, alpha = 0.5, marker='s', color='green', label = "GFs = 1, TNFalpha = 0")
i = 0
for i in range(len(ben_sing_pert_1)):
    total_plot1.line(ben_no_pert_1[0], ben_sing_pert_1[i], alpha = 0.5, marker='s', color='blue', linestyle="--")
    i += 1
i = 0
for i in range(len(ben_sing_pert_3)):
    total_plot1.line(ben_no_pert_3[0], ben_sing_pert_3[i], alpha = 0.5, marker='s', color='green', linestyle=":")
    i += 1
total_plot1.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot1.legend()
#total_plot1.show()

figure, total_plot2 = ternary.figure(scale=scale)
#total_plot1.boundary(linewidth=2.0)
total_plot2.gridlines(color="blue", multiple=0.1)
fontsize = 15
total_plot2.set_title("Phenotype change when give two perturbation in TNFalpha off", fontsize=fontsize)
total_plot2.left_axis_label("Apoptosis", fontsize=10)
total_plot2.right_axis_label("Proliferation", fontsize=10)
total_plot2.bottom_axis_label("Quiescent", fontsize=10)
total_plot2.scatter(ben_doub_pert_1, alpha = 0.5, marker='s', color='blue', label = "GFs = 0, TNFalpha = 0")
total_plot2.scatter(ben_doub_pert_3, alpha = 0.5, marker='s', color='green', label = "GFs = 1, TNFalpha = 0")
i = 0
for i in range(len(ben_doub_pert_1)):
    total_plot2.line(ben_no_pert_1[0], ben_doub_pert_1[i], alpha = 0.5, marker='s', color='blue', linestyle="--")
    i += 1
i = 0
for i in range(len(ben_doub_pert_3)):
    total_plot2.line(ben_no_pert_3[0], ben_doub_pert_3[i], alpha = 0.5, marker='s', color='green', linestyle=":")
    i += 1
total_plot2.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot2.legend()
#total_plot2.show()

figure, total_plot3 = ternary.figure(scale=scale)
#total_plot1.boundary(linewidth=2.0)
total_plot3.gridlines(color="blue", multiple=0.1)
fontsize = 15
total_plot3.set_title("Phenotype change when give one perturbation in TNFalpha on", fontsize=fontsize)
total_plot3.left_axis_label("Apoptosis", fontsize=10)
total_plot3.right_axis_label("Proliferation", fontsize=10)
total_plot3.bottom_axis_label("Quiescent", fontsize=10)
total_plot3.scatter(ben_sing_pert_2, alpha = 0.5, marker='s', color='blue', label = "GFs = 0, TNFalpha = 1")
total_plot3.scatter(ben_sing_pert_4, alpha = 0.5, marker='s', color='green', label = "GFs = 1, TNFalpha = 1")
i = 0
for i in range(len(ben_sing_pert_2)):
    total_plot3.line(ben_no_pert_2[0], ben_sing_pert_2[i], alpha = 0.5, marker='s', color='blue', linestyle="--")
    i += 1
i = 0
for i in range(len(ben_sing_pert_4)):
    total_plot3.line(ben_no_pert_4[0], ben_sing_pert_4[i], alpha = 0.5, marker='s', color='green', linestyle=":")
    i += 1
total_plot3.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot3.legend()
#total_plot3.show()

figure, total_plot4 = ternary.figure(scale=scale)
#total_plot1.boundary(linewidth=2.0)
total_plot4.gridlines(color="blue", multiple=0.1)
fontsize = 15
total_plot4.set_title("Phenotype change when give two perturbation in TNFalpha on", fontsize=fontsize)
total_plot4.left_axis_label("Apoptosis", fontsize=10)
total_plot4.right_axis_label("Proliferation", fontsize=10)
total_plot4.bottom_axis_label("Quiescent", fontsize=10)
total_plot4.scatter(ben_doub_pert_2, alpha = 0.5, marker='s', color='blue', label = "GFs = 0, TNFalpha = 1")
total_plot4.scatter(ben_doub_pert_4, alpha = 0.5, marker='s', color='green', label = "GFs = 1, TNFalpha = 1")
i = 0
for i in range(len(ben_doub_pert_2)):
    total_plot4.line(ben_no_pert_2[0], ben_doub_pert_2[i], alpha = 0.5, marker='s', color='blue', linestyle="--")
    i += 1
i = 0
for i in range(len(ben_doub_pert_4)):
    total_plot4.line(ben_no_pert_4[0], ben_doub_pert_4[i], alpha = 0.5, marker='s', color='green', linestyle=":")
    i += 1
total_plot4.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot4.legend()
#total_plot4.show()

figure, total_plot5 = ternary.figure(scale=scale)
#total_plot1.boundary(linewidth=2.0)
total_plot5.gridlines(color="blue", multiple=0.1)
fontsize = 15
total_plot5.set_title("Phenotype change when give one perturbation in TNFalpha off", fontsize=fontsize)
total_plot5.left_axis_label("Apoptosis", fontsize=10)
total_plot5.right_axis_label("Proliferation", fontsize=10)
total_plot5.bottom_axis_label("Quiescent", fontsize=10)
total_plot5.scatter(mal_sing_pert_1, alpha = 0.5, marker='s', color='blue', label = "GFs = 0, TNFalpha = 0")
total_plot5.scatter(mal_sing_pert_3, alpha = 0.5, marker='s', color='green', label = "GFs = 1, TNFalpha = 0")
i = 0
for i in range(len(mal_sing_pert_1)):
    total_plot5.line(mal_no_pert_1[0], mal_sing_pert_1[i], alpha = 0.5, marker='s', color='blue', linestyle="--")
    i += 1
i = 0
for i in range(len(mal_sing_pert_3)):
    total_plot5.line(mal_no_pert_3[0], mal_sing_pert_3[i], alpha = 0.5, marker='s', color='green', linestyle=":")
    i += 1
total_plot5.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot5.legend()
#total_plot5.show()

figure, total_plot6 = ternary.figure(scale=scale)
#total_plot1.boundary(linewidth=2.0)
total_plot6.gridlines(color="blue", multiple=0.1)
fontsize = 15
total_plot6.set_title("Phenotype change when give two perturbation in TNFalpha off", fontsize=fontsize)
total_plot6.left_axis_label("Apoptosis", fontsize=10)
total_plot6.right_axis_label("Proliferation", fontsize=10)
total_plot6.bottom_axis_label("Quiescent", fontsize=10)
total_plot6.scatter(mal_doub_pert_1, alpha = 0.5, marker='s', color='blue', label = "GFs = 0, TNFalpha = 0")
total_plot6.scatter(mal_doub_pert_3, alpha = 0.5, marker='s', color='green', label = "GFs = 1, TNFalpha = 0")
i = 0
for i in range(len(mal_doub_pert_1)):
    total_plot6.line(mal_no_pert_1[0], mal_doub_pert_1[i], alpha = 0.5, marker='s', color='blue', linestyle="--")
    i += 1
i = 0
for i in range(len(mal_doub_pert_3)):
    total_plot6.line(mal_no_pert_3[0], mal_doub_pert_3[i], alpha = 0.5, marker='s', color='green', linestyle=":")
    i += 1
total_plot6.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot6.legend()
#total_plot6.show()

figure, total_plot7 = ternary.figure(scale=scale)
#total_plot1.boundary(linewidth=2.0)
total_plot7.gridlines(color="blue", multiple=0.1)
fontsize =15
total_plot7.set_title("Phenotype change when give one perturbation in TNFalpha on", fontsize=fontsize)
total_plot7.left_axis_label("Apoptosis", fontsize=10)
total_plot7.right_axis_label("Proliferation", fontsize=10)
total_plot7.bottom_axis_label("Quiescent", fontsize=10)
total_plot7.scatter(mal_sing_pert_2, alpha = 0.5, marker='s', color='blue', label = "GFs = 0, TNFalpha = 1")
total_plot7.scatter(mal_sing_pert_4, alpha = 0.5, marker='s', color='green', label = "GFs = 1, TNFalpha = 1")
i = 0
for i in range(len(mal_sing_pert_2)):
    total_plot7.line(mal_no_pert_2[0], mal_sing_pert_2[i], alpha = 0.5, marker='s', color='blue', linestyle="--")
    i += 1
i = 0
for i in range(len(mal_sing_pert_4)):
    total_plot7.line(mal_no_pert_4[0], mal_sing_pert_4[i], alpha = 0.5, marker='s', color='green', linestyle=":")
    i += 1
total_plot7.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot7.legend()
#total_plot7.show()

figure, total_plot8 = ternary.figure(scale=scale)
#total_plot1.boundary(linewidth=2.0)
total_plot8.gridlines(color="blue", multiple=0.1)
fontsize = 15
total_plot8.set_title("Phenotype change when give two perturbation in TNFalpha on", fontsize=fontsize)
total_plot8.left_axis_label("Apoptosis", fontsize=10)
total_plot8.right_axis_label("Proliferation", fontsize=10)
total_plot8.bottom_axis_label("Quiescent", fontsize=10)
total_plot8.scatter(mal_doub_pert_2, alpha = 0.5, marker='s', color='blue', label = "GFs = 0, TNFalpha = 1")
total_plot8.scatter(mal_doub_pert_4, alpha = 0.5, marker='s', color='green', label = "GFs = 1, TNFalpha = 1")
i = 0
for i in range(len(mal_doub_pert_2)):
    total_plot8.line(mal_no_pert_2[0], mal_doub_pert_2[i], alpha = 0.5, marker='s', color='blue', linestyle="--")
    i += 1
i = 0
for i in range(len(mal_doub_pert_4)):
    total_plot8.line(mal_no_pert_4[0], mal_doub_pert_4[i], alpha = 0.5, marker='s', color='green', linestyle=":")
    i += 1
total_plot8.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot8.legend()
total_plot8.show()
set_trace()

scale = 1
figure, total_plot = ternary.figure(scale=scale)
#total_plot.boundary(linewidth=2.0)
total_plot.gridlines(color="blue", multiple=0.1)
fontsize = 15
total_plot.set_title("Total Distribution", fontsize=fontsize)
total_plot.left_axis_label("Apoptosis", fontsize=10)
total_plot.right_axis_label("Proliferation", fontsize=10)
total_plot.bottom_axis_label("Quiescent", fontsize=10)
total_plot.scatter(no_pert, alpha=0.5, marker='s', color='blue', label="No perturbation")
total_plot.scatter(sing_pert, alpha=0.5, marker='s', color='red', label="Single perturbation")
total_plot.scatter(doub_pert, alpha=0.5, marker='s', color='green', label="Double perturbation")
total_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
total_plot.legend()
figure.savefig('Total distribution.png')

figure, pert_no = ternary.figure(scale=scale)
#pert_no.boundary(linewidth=2.0)
pert_no.gridlines(color="blue", multiple=0.1)
pert_no.set_title("No perturbation", fontsize=fontsize)
pert_no.left_axis_label("Apoptosis", fontsize=10)
pert_no.right_axis_label("Proliferation", fontsize=10)
pert_no.bottom_axis_label("Quiescent", fontsize=10)
pert_no.scatter(no_pert, alpha=0.5, marker='s', color='blue', label="No perturbation")
pert_no.ticks(axis="lbr", multiple=0.1, linewidth=1)
pert_no.legend()
figure.savefig('No perturbation.png')

figure, pert_sing = ternary.figure(scale=scale)
#pert_sing.boundary(linewidth=2.0)
pert_sing.gridlines(color="blue", multiple=0.1)
pert_sing.set_title("Single perturbation", fontsize=fontsize)
pert_sing.left_axis_label("Apoptosis", fontsize=10)
pert_sing.right_axis_label("Proliferation", fontsize=10)
pert_sing.bottom_axis_label("Quiescent", fontsize=10)
pert_sing.scatter(sing_pert, alpha=0.5, marker='s', color='blue', label="Single perturbation")
pert_sing.ticks(axis="lbr", multiple=0.1, linewidth=1)
pert_sing.legend()
figure.savefig('Single perturbation.png')

figure, pert_doub = ternary.figure(scale=scale)
#pert_doub.boundary(linewidth=2.0)
pert_doub.gridlines(color="blue", multiple=0.1)
pert_doub.set_title("Double perturbation", fontsize=fontsize)
pert_doub.left_axis_label("Apoptosis", fontsize=10)
pert_doub.right_axis_label("Proliferation", fontsize=10)
pert_doub.bottom_axis_label("Quiescent", fontsize=10)
pert_doub.scatter(doub_pert, alpha=0.5, marker='s', color='blue', label="Double perturbation")
pert_doub.ticks(axis="lbr", multiple=0.1, linewidth=1)
pert_doub.legend()
figure.savefig('Double perturbation.png')

figure, ben_no_pert = ternary.figure(scale=scale)
#ben_no_pert.boundary(linewidth=2.0)
ben_no_pert.gridlines(color="blue", multiple=0.1)
ben_no_pert.set_title("Beign tumor cell with no perturbation", fontsize=fontsize)
ben_no_pert.left_axis_label("Apoptosis", fontsize=10)
ben_no_pert.right_axis_label("Proliferation", fontsize=10)
ben_no_pert.bottom_axis_label("Quiescent", fontsize=10)
ben_no_pert.scatter(ben_no_pert_1, alpha=0.5, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
ben_no_pert.scatter(ben_no_pert_2, alpha=0.5, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
ben_no_pert.scatter(ben_no_pert_3, alpha=0.5, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
ben_no_pert.scatter(ben_no_pert_4, alpha=0.5, marker='s', color='magenta', label="GFs = 1, TNFalpha = 1")
ben_no_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
ben_no_pert.legend()
figure.savefig('Benign tumor cell with no perturbation.png')

figure, ben_sing_pert = ternary.figure(scale=scale)
#ben_sing_pert.boundary(linewidth=2.0)
ben_sing_pert.gridlines(color="blue", multiple=0.1)
ben_sing_pert.set_title("Beign tumor cell with single perturbation", fontsize=fontsize)
ben_sing_pert.left_axis_label("Apoptosis", fontsize=10)
ben_sing_pert.right_axis_label("Proliferation", fontsize=10)
ben_sing_pert.bottom_axis_label("Quiescent", fontsize=10)
ben_sing_pert.scatter(ben_sing_pert_1, alpha=0.5, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
ben_sing_pert.scatter(ben_sing_pert_2, alpha=0.5, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
ben_sing_pert.scatter(ben_sing_pert_3, alpha=0.5, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
ben_sing_pert.scatter(ben_sing_pert_4, alpha=0.5, marker='s', color='magenta', label="GFs = 1, TNFalpha = 1")
ben_sing_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
ben_sing_pert.legend()
figure.savefig('Benign tumor cell with single perturbation.png')

figure, ben_doub_pert = ternary.figure(scale=scale)
#ben_doub_pert.boundary(linewidth=2.0)
ben_doub_pert.gridlines(color="blue", multiple=0.1)
ben_doub_pert.set_title("Beign tumor cell with double perturbation", fontsize=fontsize)
ben_doub_pert.left_axis_label("Apoptosis", fontsize=10)
ben_doub_pert.right_axis_label("Proliferation", fontsize=10)
ben_doub_pert.bottom_axis_label("Quiescent", fontsize=10)
ben_doub_pert.scatter(ben_doub_pert_1, alpha=0.5, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
ben_doub_pert.scatter(ben_doub_pert_2, alpha=0.5, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
ben_doub_pert.scatter(ben_doub_pert_3, alpha=0.5, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
ben_doub_pert.scatter(ben_doub_pert_4, alpha=0.5, marker='s', color='magenta', label="GFs = 1, TNFalpha = 1")
ben_doub_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
ben_doub_pert.legend()
figure.savefig('Benign tumor cell with double perturbation.png')

figure, mal_no_pert = ternary.figure(scale=scale)
#mal_no_pert.boundary(linewidth=2.0)
mal_no_pert.gridlines(color="blue", multiple=0.1)
mal_no_pert.set_title("Malignt tumor cell with no perturbation", fontsize=fontsize)
mal_no_pert.left_axis_label("Apoptosis", fontsize=10)
mal_no_pert.right_axis_label("Proliferation", fontsize=10)
mal_no_pert.bottom_axis_label("Quiescent", fontsize=10)
mal_no_pert.scatter(mal_no_pert_1, alpha=0.5, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
mal_no_pert.scatter(mal_no_pert_2, alpha=0.5, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
mal_no_pert.scatter(mal_no_pert_3, alpha=0.5, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
mal_no_pert.scatter(mal_no_pert_4, alpha=0.5, marker='s', color='magenta', label="GFs = 1, TNFalpha = 1")
mal_no_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
mal_no_pert.legend()
figure.savefig('Malignt tumor cell with no perturbation.png')

figure, mal_sing_pert = ternary.figure(scale=scale)
#mal_sing_pert.boundary(linewidth=2.0)
mal_sing_pert.gridlines(color="blue", multiple=0.1)
mal_sing_pert.set_title("Malignt tumor cell with single perturbation", fontsize=fontsize)
mal_sing_pert.left_axis_label("Apoptosis", fontsize=10)
mal_sing_pert.right_axis_label("Proliferation", fontsize=10)
mal_sing_pert.bottom_axis_label("Quiescent", fontsize=10)
mal_sing_pert.scatter(mal_sing_pert_1, alpha=0.5, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
mal_sing_pert.scatter(mal_sing_pert_2, alpha=0.5, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
mal_sing_pert.scatter(mal_sing_pert_3, alpha=0.5, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
mal_sing_pert.scatter(mal_sing_pert_4, alpha=0.5, marker='s', color='magenta', label="GFs = 1, TNFalpha = 1")
mal_sing_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
mal_sing_pert.legend()
figure.savefig('Malignt tumor cell with single perturbation.png')

figure, mal_doub_pert = ternary.figure(scale=scale)
#mal_doub_pert.boundary(linewidth=2.0)
mal_doub_pert.gridlines(color="blue", multiple=0.1)
mal_doub_pert.set_title("Malignt tumor cell with double perturbation", fontsize=fontsize)
mal_doub_pert.left_axis_label("Apoptosis", fontsize=10)
mal_doub_pert.right_axis_label("Proliferation", fontsize=10)
mal_doub_pert.bottom_axis_label("Quiescent", fontsize=10)
mal_doub_pert.scatter(mal_doub_pert_1, alpha=0.5, marker='s', color='blue', label="GFs = 0, TNFalpha = 0")
mal_doub_pert.scatter(mal_doub_pert_2, alpha=0.5, marker='s', color='red', label="GFs = 0, TNFalpha = 1")
mal_doub_pert.scatter(mal_doub_pert_3, alpha=0.5, marker='s', color='green', label="GFs = 1, TNFalpha = 0")
mal_doub_pert.scatter(mal_doub_pert_4, alpha=0.5, marker='s', color='magenta', label="GFs = 1, TNFalpha = 1")
mal_doub_pert.ticks(axis="lbr", multiple=0.1, linewidth=1)
mal_doub_pert.legend()
figure.savefig('Malignt tumor cell with double perturbation.png')

figure, ben_1_plot = ternary.figure(scale=scale)
#ben_1_plot.boundary(linewidth=2.0)
ben_1_plot.gridlines(color="blue", multiple=0.1)
ben_1_plot.set_title("Benign Distribution (GFs = 0. TNFalpha = 0)", fontsize=fontsize)
ben_1_plot.left_axis_label("Apoptosis", fontsize=10)
ben_1_plot.right_axis_label("Proliferation", fontsize=10)
ben_1_plot.bottom_axis_label("Quiescent", fontsize=10)
ben_1_plot.scatter(ben_no_pert_1, alpha=0.5, marker='s', color='blue', label="No perturbation")
ben_1_plot.scatter(ben_sing_pert_1, alpha=0.5, marker='s', color='red', label="Single perturbation")
ben_1_plot.scatter(ben_doub_pert_1, alpha=0.5, marker='s', color='green', label="Double perturbation")
ben_1_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
ben_1_plot.legend()
figure.savefig('Benign Distribution (GFs = 0. TNFalpha = 0).png')

figure, ben_2_plot = ternary.figure(scale=scale)
#ben_2_plot.boundary(linewidth=2.0)
ben_2_plot.gridlines(color="blue", multiple=0.1)
ben_2_plot.set_title("Benign Distribution (GFs = 0. TNFalpha = 1)", fontsize=fontsize)
ben_2_plot.left_axis_label("Apoptosis", fontsize=10)
ben_2_plot.right_axis_label("Proliferation", fontsize=10)
ben_2_plot.bottom_axis_label("Quiescent", fontsize=10)
ben_2_plot.scatter(ben_no_pert_2, alpha=0.5, marker='s', color='blue', label="No perturbation")
ben_2_plot.scatter(ben_sing_pert_2, alpha=0.5, marker='s', color='red', label="Single perturbation")
ben_2_plot.scatter(ben_doub_pert_2, alpha=0.5, marker='s', color='green', label="Double perturbation")
ben_2_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
ben_2_plot.legend()
figure.savefig('Benign Distribution (GFs = 0. TNFalpha = 1).png')

figure, ben_3_plot = ternary.figure(scale=scale)
#ben_3_plot.boundary(linewidth=2.0)
ben_3_plot.gridlines(color="blue", multiple=0.1)
ben_3_plot.set_title("Benign Distribution (GFs = 1. TNFalpha = 0)", fontsize=fontsize)
ben_3_plot.left_axis_label("Apoptosis", fontsize=10)
ben_3_plot.right_axis_label("Proliferation", fontsize=10)
ben_3_plot.bottom_axis_label("Quiescent", fontsize=10)
ben_3_plot.scatter(ben_no_pert_3, alpha=0.5, marker='s', color='blue', label="No perturbation")
ben_3_plot.scatter(ben_sing_pert_3, alpha=0.5, marker='s', color='red', label="Single perturbation")
ben_3_plot.scatter(ben_doub_pert_3, alpha=0.5, marker='s', color='green', label="Double perturbation")
ben_3_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
ben_3_plot.legend()
figure.savefig('Benign Distribution (GFs = 1. TNFalpha = 0).png')

figure, ben_4_plot = ternary.figure(scale=scale)
#ben_4_plot.boundary(linewidth=2.0)
ben_4_plot.gridlines(color="blue", multiple=0.1)
ben_4_plot.set_title("Benign Distribution (GFs = 1. TNFalpha = 1)", fontsize=fontsize)
ben_4_plot.left_axis_label("Apoptosis", fontsize=10)
ben_4_plot.right_axis_label("Proliferation", fontsize=10)
ben_4_plot.bottom_axis_label("Quiescent", fontsize=10)
ben_4_plot.scatter(ben_no_pert_4, alpha=0.5, marker='s', color='blue', label="No perturbation")
ben_4_plot.scatter(ben_sing_pert_4, alpha=0.5, marker='s', color='red', label="Single perturbation")
ben_4_plot.scatter(ben_doub_pert_4, alpha=0.5, marker='s', color='green', label="Double perturbation")
ben_4_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
ben_4_plot.legend()
figure.savefig('Benign Distribution (GFs = 1. TNFalpha = 1).png')

figure, mal_1_plot = ternary.figure(scale=scale)
#mal_1_plot.boundary(linewidth=2.0)
mal_1_plot.gridlines(color="blue", multiple=0.1)
mal_1_plot.set_title("Malignant Distribution (GFs = 0. TNFalpha = 0)", fontsize=fontsize)
mal_1_plot.left_axis_label("Apoptosis", fontsize=10)
mal_1_plot.right_axis_label("Proliferation", fontsize=10)
mal_1_plot.bottom_axis_label("Quiescent", fontsize=10)
mal_1_plot.scatter(mal_no_pert_1, alpha=0.5, marker='s', color='blue', label="No perturbation")
mal_1_plot.scatter(mal_sing_pert_1, alpha=0.5, marker='s', color='red', label="Single perturbation")
mal_1_plot.scatter(mal_doub_pert_1, alpha=0.5, marker='s', color='green', label="Double perturbation")
mal_1_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
mal_1_plot.legend()
figure.savefig('Malignant Distribution (GFs = 0. TNFalpha = 0).png')

figure, mal_2_plot = ternary.figure(scale=scale)
#mal_2_plot.boundary(linewidth=2.0)
mal_2_plot.gridlines(color="blue", multiple=0.1)
mal_2_plot.set_title("Malignant Distribution (GFs = 0. TNFalpha = 1)", fontsize=fontsize)
mal_2_plot.left_axis_label("Apoptosis", fontsize=10)
mal_2_plot.right_axis_label("Proliferation", fontsize=10)
mal_2_plot.bottom_axis_label("Quiescent", fontsize=10)
mal_2_plot.scatter(mal_no_pert_2, alpha=0.5, marker='s', color='blue', label="No perturbation")
mal_2_plot.scatter(mal_sing_pert_2, alpha=0.5, marker='s', color='red', label="Single perturbation")
mal_2_plot.scatter(mal_doub_pert_2, alpha=0.5, marker='s', color='green', label="Double perturbation")
mal_2_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
mal_2_plot.legend()
figure.savefig('Malignant Distribution (GFs = 0. TNFalpha = 1).png')

figure, mal_3_plot = ternary.figure(scale=scale)
#mal_3_plot.boundary(linewidth=2.0)
mal_3_plot.gridlines(color="blue", multiple=0.1)
mal_3_plot.set_title("Malignant Distribution (GFs = 1. TNFalpha = 0)", fontsize=fontsize)
mal_3_plot.left_axis_label("Apoptosis", fontsize=10)
mal_3_plot.right_axis_label("Proliferation", fontsize=10)
mal_3_plot.bottom_axis_label("Quiescent", fontsize=10)
mal_3_plot.scatter(mal_no_pert_3, alpha=0.5, marker='s', color='blue', label="No perturbation")
mal_3_plot.scatter(mal_sing_pert_3, alpha=0.5, marker='s', color='red', label="Single perturbation")
mal_3_plot.scatter(mal_doub_pert_3, alpha=0.5, marker='s', color='green', label="Double perturbation")
mal_3_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
mal_3_plot.legend()
figure.savefig('Malignant Distribution (GFs = 1. TNFalpha = 0).png')

figure, mal_4_plot = ternary.figure(scale=scale)
#mal_4_plot.boundary(linewidth=2.0)
mal_4_plot.gridlines(color="blue", multiple=0.1)
mal_4_plot.set_title("Malignant Distribution (GFs = 1. TNFalpha = 1)", fontsize=fontsize)
mal_4_plot.left_axis_label("Apoptosis", fontsize=10)
mal_4_plot.right_axis_label("Proliferation", fontsize=10)
mal_4_plot.bottom_axis_label("Quiescent", fontsize=10)
mal_4_plot.scatter(mal_no_pert_4, alpha=0.5, marker='s', color='blue', label="No perturbation")
mal_4_plot.scatter(mal_sing_pert_4, alpha=0.5, marker='s', color='red', label="Single perturbation")
mal_4_plot.scatter(mal_doub_pert_4, alpha=0.5, marker='s', color='green', label="Double perturbation")
mal_4_plot.ticks(axis="lbr", multiple=0.1, linewidth=1)
mal_4_plot.legend()
figure.savefig('Malignant Distribution (GFs = 1. TNFalpha = 1).png')
mal_4_plot.show()

set_trace()

#p1=(0.4, 0.3, 0.3)
#p2=(0.5, 0.5, 0)
#p3=(0.25, 0.5, 0.25)
#sim_plot.line(p1,p3,linewidth=3.,marker='s',color='green',linestyle=":")
#tax.plot(p1,linewidth=2.0,label="point")




#figure.savefig


set_trace()
# mutations = {
# 	'list': {
# 		'APC': {
# 			'function': 'LOF',
# 	    	'intensity': 0.5
# 	    },
# 	    'CTNNB1': {
# 	    	'function': 'GOF',
# 	    	'intensity': 1.0
# 	    }
# 	},
# 	'default_function': 'LOF'
# }
#
# drugs = {
# 	'list': {
# 		'MEKi': {
# 			'type': 'inhibitor',
# 	    	'dose': 0.5,
# 	    	'time_constant': 10
# 	    },
# 	},
# }
#
#
# def rule_mutation(state, name, cellline, value, p):
#     """ rule_mutation defines how mutation is appied into simulation. """
#
#
#     global mutations
#
#     if name in mutations[cellline]:
#
#         given_function = mutations[cellline][name]['function']
#
#         intensity = mutations[cellline][name]['intensity']
#
#         if given_function == 'UNKNOWN':
#             given_function = mutations['default_function']
#
#         if given_function == 'LOF':
#             if value == True:
#                 if random.random() < intensity:
#                     value = False
#
#         elif given_function == 'GOF':
#             if value == False:
#                 if random.random() < intensity:
#                     value = True
#
# # setattr( state, name, value )
# # setattr should be used only once and only in set_value().
#     return value
#
# def rule_drug(state, name, value, p):
#     "rule_drug"
#
#     pass
#
#
# def set_value2(state, name, value, p):
#     "Custom value setter"
#
#     dst_value1 = rule_mutation(state, name, src_value, p)
#
#     dst_value2 = rule_drug(state, name, src_value, p)
#
#     # Here, problem occurs if rule_mutation() and rule_drug() does not give
#     # same changes (src_value->dst_value1, src_value->dst_value2).
#
#     # This problem can be ignored if we ignore the case that src_value =
#     # dst_value. We consider src == dst as no effect.
#
#     if dst_value1 == dst_value2:
#         dst_value = dst_value1
#
#     else:
#         if src_value == dst_value1:
#             dst_value = dst_value2
#
#         elif src_value == dst_value2:
#             dst_value = dst_value1
#
#     # finally, we decided dst_value and then we set the attribute.
#     setattr(state, name, dst_value)
#
#     return value
#
#
# # hello set_value
# # create a custom value setter
# def set_value(state, name, value, p):
#     "Custom value setter"
#
#     inhibitor_strength = 0.16
#     # detect the node of interest
#     if name == 'D':
#         # print 'now setting node %s' % name
#         if value == True:
#             if random.random() < inhibitor_strength:
#                 value = False
#
#     # this sets the attribute
#     setattr(state, name, value)
#
#     return value
#
#
# def test_main():
#     text = """
#     A = True
#     B = Random
#     C = Random
#     D = Random
#
#     B* = A or C
#     C* = A and not D
#     D* = B and C
#     """
#
#     repeat = 1000
#     coll = util.Collector()
#     for i in range(repeat):
#         progressbar.update(i, repeat)
#         model = boolean2.Model(text, mode='async')
#         model.parser.RULE_SETVALUE = set_value
#         model.initialize()
#         model.iterate(steps=30)
#
#         # in this case we take all nodes
#         # one could just list a few nodes such as [ 'A', 'B', 'C' ]
#         nodes = model.nodes
#
#         # this collects states for each run
#         coll.collect(states=model.states, nodes=nodes)
#
#     # this step averages the values for each node
#     # returns a dictionary keyed by nodes and a list of values
#     # with the average state for in each timestep
#     avgs = coll.get_averages(normalize=True)
#
#     # make some shortcut to data to for easier plotting
#     valueB = avgs["B"]
#     valueC = avgs["C"]
#     valueD = avgs["D"]
#
#     p1, = plt.plot(valueB, 'ob-')
#     p2, = plt.plot(valueC, 'sr-')
#     p3, = plt.plot(valueD, '^g-')
#     plt.legend([p1, p2, p3], ["B", "C", "D"])
#     plt.show()
#     plt.savefig('test_mutation_output.png')

#cln=data_mutcna.columns[2]
#data_cln = cnv_data[cln]
# attrs = attr_data['basin_of_attraction']
# fmap = attr_data['fingerprint_map']
# mapkeys = attr_data['fingerprint_map_keys']
# attr_info = attr_data['attractor_info']
# data_MUTCNA = pd.DataFrame([], columns=['Cell Line'] + ['CCLE Mut'] + ['CCLE CNV AMP'] + ['CCLE CNV DEL']+ ['Network Mut'] + ['Network CNV AMP'] + ['Network CNV DEL'])
# data_MUTCNA.loc[i, 'CCLE Mut'] = len(data_sub_MUT)
# data_net = data_sub.filter(regex=gene_index)
# gene_index = gene.loc[j, 'node_name']
# therapy_data = therapy[therapy['Compound'].str.contains(drug)]
# util.update_progress(i, len(therapy['Compound']))
#sampleinfo = ccle.sampleinfo()
#total_data.to_csv('total_data.csv')
# mutcna.to_csv('output_cnvcol.csv')
# iloc : number loc : string index mutcna.index(gene names)
# res = sampleinfo['Site Primary']=='large_intestine'
# res = sampleinfo[ sampleinfo['Site Primary']=='large_intestine' ]
# mutcna.columns
# pd.DataFrame(data) : list to dataframe

set_trace()

