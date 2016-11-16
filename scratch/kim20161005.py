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
outputfile7 = join(dirname(tab_s10.__file__), 'TABLE.S8B_total_attractor_input_condition.csv')

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


benign_1 = simulation_data[(simulation_data['Input_GFs']==0)&(simulation_data['Input_Hypoxia']==0)&(simulation_data['Input_Mutagen']==0)&
(simulation_data['Input_Nutrients']==1)&(simulation_data['Input_TNFalpha']==0)]
benign_2 = simulation_data[(simulation_data['Input_GFs']==0)&(simulation_data['Input_Hypoxia']==0)&(simulation_data['Input_Mutagen']==0)&
(simulation_data['Input_Nutrients']==1)&(simulation_data['Input_TNFalpha']==1)]
benign_3 = simulation_data[(simulation_data['Input_GFs']==1)&(simulation_data['Input_Hypoxia']==0)&(simulation_data['Input_Mutagen']==0)&
(simulation_data['Input_Nutrients']==1)&(simulation_data['Input_TNFalpha']==0)]
benign_4 = simulation_data[(simulation_data['Input_GFs']==1)&(simulation_data['Input_Hypoxia']==0)&(simulation_data['Input_Mutagen']==0)&
(simulation_data['Input_Nutrients']==1)&(simulation_data['Input_TNFalpha']==1)]

malig_1 = simulation_data[(simulation_data['Input_GFs']==0)&(simulation_data['Input_Hypoxia']==1)&(simulation_data['Input_Mutagen']==1)&
(simulation_data['Input_Nutrients']==0)&(simulation_data['Input_TNFalpha']==0)]
malig_2 = simulation_data[(simulation_data['Input_GFs']==0)&(simulation_data['Input_Hypoxia']==1)&(simulation_data['Input_Mutagen']==1)&
(simulation_data['Input_Nutrients']==0)&(simulation_data['Input_TNFalpha']==1)]
malig_3 = simulation_data[(simulation_data['Input_GFs']==1)&(simulation_data['Input_Hypoxia']==1)&(simulation_data['Input_Mutagen']==1)&
(simulation_data['Input_Nutrients']==0)&(simulation_data['Input_TNFalpha']==0)]
malig_4 = simulation_data[(simulation_data['Input_GFs']==1)&(simulation_data['Input_Hypoxia']==1)&(simulation_data['Input_Mutagen']==1)&
(simulation_data['Input_Nutrients']==0)&(simulation_data['Input_TNFalpha']==1)]
#no_pert = simulation_data[(str(simulation_data['Perturbation1']) == 'nan')&(str(simulation_data['Perturbation2']) == 'nan')]
#no_pert1 = simulation_data[(str(simulation_data['Perturbation1']) == 'S_Gli')&(str(simulation_data['Perturbation2']) == 'nan')]
i = 0
no_pert = {}
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
    if (input_condi[1]==0)&(input_condi[2]==0)&(input_condi[3]==1):
        if (input_condi[0]==0)&(input_condi[4]==0):
            if str(sim_data['Perturbation1']) == 'nan':
                if str(sim_data['Perturbation2']) == 'nan':
                    ben_pert_no1 = [sim_data['Quiescent'],sim_data['Proliferation'],sim_data['Apoptosis']]
        elif (input_condi[0]==0)&(input_condi[4]==1):
            if str(sim_data['Perturbation1']) == 'nan':
                if str(sim_data['Perturbation2']) == 'nan':
                    ben_pert_no2 = [sim_data['Quiescent'],sim_data['Proliferation'],sim_data['Apoptosis']]
        elif (input_condi[0]==1)&(input_condi[4]==0):
            if str(sim_data['Perturbation1']) == 'nan':
                if str(sim_data['Perturbation2']) == 'nan':
                    ben_pert_no3 = [sim_data['Quiescent'],sim_data['Proliferation'],sim_data['Apoptosis']]
        elif (input_condi[0]==1)&(input_condi[4]==1):
            if str(sim_data['Perturbation1']) == 'nan':
                if str(sim_data['Perturbation2']) == 'nan':
                    ben_pert_no4 = [sim_data['Quiescent'],sim_data['Proliferation'],sim_data['Apoptosis']]
    elif (input_condi[1]==1)&(input_condi[2]==1)&(input_condi[3]==0):
        if (input_condi[0]==0)&(input_condi[4]==0):
            if str(sim_data['Perturbation1']) == 'nan':
                if str(sim_data['Perturbation2']) == 'nan':
                    malig_pert_no1 = [sim_data['Quiescent'],sim_data['Proliferation'],sim_data['Apoptosis']]
        elif (input_condi[0]==0)&(input_condi[4]==1):
            if str(sim_data['Perturbation1']) == 'nan':
                if str(sim_data['Perturbation2']) == 'nan':
                    malig_pert_no2 = [sim_data['Quiescent'],sim_data['Proliferation'],sim_data['Apoptosis']]
        elif (input_condi[0]==1)&(input_condi[4]==0):
            if str(sim_data['Perturbation1']) == 'nan':
                if str(sim_data['Perturbation2']) == 'nan':
                    malig_pert_no3 = [sim_data['Quiescent'],sim_data['Proliferation'],sim_data['Apoptosis']]
        elif (input_condi[0]==1)&(input_condi[4]==1):
            if str(sim_data['Perturbation1']) == 'nan':
                if str(sim_data['Perturbation2']) == 'nan':
                    malig_pert_no4 = [sim_data['Quiescent'],sim_data['Proliferation'],sim_data['Apoptosis']]

set_trace()
scale = 1
figure, bengign_no_per = ternary.figure(scale = scale)

bengign_no_per.boundary(linewidth = 2.0)
bengign_no_per.gridlines(color = "blue", multiple = 0.05)

fontsize = 20
bengign_no_per.set_title("Benign tumor with no perturbation", fontsize = fontsize)
bengign_no_per.left_axis_label("Quiescent", fontsize = 15)
bengign_no_per.right_axis_label("Apoptosis", fontsize=15)
bengign_no_per.bottom_axis_label("Proliferation", fontsize=15)

bengign_no_per.scatter([ben_pert_no1,ben_pert_no2,ben_pert_no3,ben_pert_no4],marker='s', color='red', label="Red Squares")
bengign_no_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
bengign_no_per.legend()
figure.savefig('Benign_with_no_perturbation.png')
#bengign_no_per.show()


figure, malig_no_per = ternary.figure(scale = scale)

malig_no_per.boundary(linewidth = 2.0)
malig_no_per.gridlines(color = "blue", multiple = 0.05)

fontsize = 20
malig_no_per.set_title("Malignant tumor with no perturbation", fontsize = fontsize)
malig_no_per.left_axis_label("Quiescent", fontsize = 15)
malig_no_per.right_axis_label("Apoptosis", fontsize=15)
malig_no_per.bottom_axis_label("Proliferation", fontsize=15)

malig_no_per.scatter([malig_pert_no1,malig_pert_no2,malig_pert_no3,malig_pert_no4],marker='s', color='red', label="Red Squares")
malig_no_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
malig_no_per.legend()
figure.savefig('Malignant_with_no_perturbation.png')


figure, bengign_per = ternary.figure(scale = scale)

ben_drug1_data = simulation_data.iloc[17979]
ben_drug1 = [ben_drug1_data['Quiescent'],ben_drug1_data['Proliferation'],ben_drug1_data['Apoptosis']]

ben_drug2_data = simulation_data.iloc[17375]
ben_drug2 = [ben_drug2_data['Quiescent'],ben_drug2_data['Proliferation'],ben_drug2_data['Apoptosis']]

ben_drug3_data = simulation_data.iloc[17943]
ben_drug3 = [ben_drug3_data['Quiescent'],ben_drug3_data['Proliferation'],ben_drug3_data['Apoptosis']]


bengign_per.boundary(linewidth = 2.0)
bengign_per.gridlines(color = "blue", multiple = 0.05)

fontsize = 20
bengign_per.set_title("Benign tumor with perturbation", fontsize = fontsize)
bengign_per.left_axis_label("Quiescent", fontsize = 15)
bengign_per.right_axis_label("Apoptosis", fontsize=15)
bengign_per.bottom_axis_label("Proliferation", fontsize=15)

bengign_per.line(ben_pert_no1, ben_drug1,linewidth=3.,marker='s',color='green')
bengign_per.line(ben_pert_no1, ben_drug2,linewidth=3.,marker='s',color='red',linestyle=":")
bengign_per.line(ben_pert_no1, ben_drug3,linewidth=3.,marker='s',color='blue',linestyle=":")
bengign_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
bengign_per.legend()
figure.savefig('Benign_with_perturbation.png')
#bengign_per.show()

figure, malig_per = ternary.figure(scale = scale)

malig_drug1_data = simulation_data.iloc[72374]
malig_drug1 = [malig_drug1_data['Quiescent'],malig_drug1_data['Proliferation'],malig_drug1_data['Apoptosis']]

malig_drug2_data = simulation_data.iloc[105891]
malig_drug2 = [malig_drug2_data['Quiescent'],malig_drug2_data['Proliferation'],malig_drug2_data['Apoptosis']]

malig_drug3_data = simulation_data.iloc[106926]
malig_drug3 = [malig_drug3_data['Quiescent'],malig_drug3_data['Proliferation'],malig_drug3_data['Apoptosis']]


malig_per.boundary(linewidth = 2.0)
malig_per.gridlines(color = "blue", multiple = 0.05)

fontsize = 20
malig_per.set_title("Malignant tumor with perturbation", fontsize = fontsize)
malig_per.left_axis_label("Quiescent", fontsize = 15)
malig_per.right_axis_label("Apoptosis", fontsize=15)
malig_per.bottom_axis_label("Proliferation", fontsize=15)

malig_per.scatter([malig_pert_no1, malig_drug1],marker='D', color='green')
malig_per.line(malig_pert_no1, malig_drug2,linewidth=3.,marker='s',color='red',linestyle=":")
malig_per.line(malig_pert_no1, malig_drug3,linewidth=3.,marker='s',color='blue',linestyle=":")
malig_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
malig_per.legend()
figure.savefig('Malignant_with_perturbation.png')
#malig_per.show()

scale = 1
figure, no_per = ternary.figure(scale = scale)

no_per.boundary(linewidth = 2.0)
no_per.gridlines(color = "blue", multiple = 0.05)

fontsize = 20
no_per.set_title("No perturbation", fontsize = fontsize)
no_per.left_axis_label("Quiescent", fontsize = 15)
no_per.right_axis_label("Apoptosis", fontsize=15)
no_per.bottom_axis_label("Proliferation", fontsize=15)

no_per.scatter(no_pert,marker='s', color='red', label="Red Squares")
no_per.ticks(axis="lbr", multiple=0.1, linewidth=1)
no_per.legend()
figure.savefig('No_perturbation.png')
no_per.show()
#malig_no_per.show()


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

