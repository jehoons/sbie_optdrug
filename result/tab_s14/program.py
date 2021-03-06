# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from os.path import dirname,join,exists
from sbie_optdrug.result import tab_s14
from ipdb import set_trace
import json
import pandas as pd
from tqdm import tqdm
#import pickle
import math
from itertools import combinations,product
from copy import deepcopy
from tqdm import tqdm
import numpy as np

#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#import random

#from boolean3_addon import attr_cy
#import numpy as np

#from boolean3 import Model
#from boolean3_addon import attractor

""" requirements """
inputfile_a = join(dirname(__file__), '..','tab_s13','TABLE.S13A.simulation_result.json')
inputfile_b = join(dirname(__file__), '..','tab_s13','fumia_network.csv')
#inputfile_c = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s4.json')
#inputfile_d = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s1.json')
#inputfile_e = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s4.json')
#inputfile_f = join(dirname(__file__), '..','tab_s5','TABLE.S5C.DRUG_data.json')
#inputfile_g = join(dirname(__file__), '..','tab_s7','untracked_Table_S7A_Fumia-processed.csv')
#inputfile_h = join(dirname(__file__), '..','tab_s7','untracked_Table_S7F-Input-combinations-APC.json')
#inputfile_i = join(dirname(__file__), '..','tab_s7','untracked_Table_S7G-Scanning-results-APC.json')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S14_total_attractor_input_condition.csv')
#outputfile_b = join(dirname(__file__), 'TABLE.S10B_total_attractor_input_condition.csv')
#outputfile_d = join(dirname(__file__), 'TABLE.S8B.MUTATION_data_s4.json')
#outputfile_e = join(dirname(__file__), 'TABLE.S8C.DRUG_data.json')

config = {
    'program': 'template',
    'input': {
        'input_a': inputfile_a,
        'input_b': inputfile_b,
        #'input_c': inputfile_c,
        #'input_d': inputfile_d,
        #'input_e': inputfile_e,
        #'input_f': inputfile_f,
        #'input_g': inputfile_g,
        #'input_h': inputfile_h,
        #'input_i': inputfile_i
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

def sgn(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    elif x < 0:
        return 0

def run(config=None):

    steps = 50
    input_num = 10000
    MUTAGEN = GFS = NUTRIENTS = TNF_A = HYPOXIA = 0
    TGF_B = DNA_DAMAGE = P53_MDM2 = AMP_ATP = NF1 = PKC = RTK = RAGS = RAS = PI3K = PTEN = 0
    PIP3 = PDK1 = IKK = NFKB = RAF = ERK12 = P90RSK = AKT = WNT = DSH = APC = GSK3 = GSK3_APC = 0
    BCAT = SLUG = MTOR = HIF1 = COX412 = VHL = PHDS = MYC_MAX = MYC = MAX = MXI1 = TSC12 = RHEB = 0
    P53 = BCL2 = BAX = BAD = BCLXL = RB = E2F = P14ARF = CYCA = CYCB = CYCD = CYCE = CDH1 = CDC20 = 0
    UBCH10 = P27 = P21 = MDM2 = SMAD = SMAD_MIZ1 = SMAD_E2F = P15 = FADD = CASP8 = BAK = JNK = FOXO = 0
    FOSJUN = ROS = AMPK = CYTOC_APAF1 = CASP9 = APOP = ECAD = GLUT1 = HTERT = VEGF = E2F_CYCE = 0
    CDH1_UBCH10 = TAK1 = GSH = TCF = MIZ1 = GLI = P70 = ATM_ATR = CHK12 = DNA_REPAIR = EEF2K = 0
    EEF2 = P53_PTEN = LDHA = ACID_LACTIC = SNAIL = 0
    input_nodes = [MUTAGEN, GFS, NUTRIENTS, TNF_A, HYPOXIA]
    free_nodes = [TGF_B, DNA_DAMAGE, P53_MDM2, AMP_ATP, NF1, PKC, RTK, RAGS, RAS, PI3K, PTEN,
    PIP3, PDK1, IKK, NFKB, RAF, ERK12, P90RSK, AKT, WNT, DSH, APC, GSK3, GSK3_APC, BCAT, SLUG,
    MTOR, HIF1, COX412, VHL, PHDS, MYC_MAX, MYC, MAX, MXI1, TSC12, RHEB, P53, BCL2, BAX, BAD,
    BCLXL, RB, E2F, P14ARF, CYCA, CYCB, CYCD, CYCE, CDH1, CDC20, UBCH10, P27, P21, MDM2, SMAD,
    SMAD_MIZ1, SMAD_E2F, P15, FADD, CASP8, BAK, JNK, FOXO, FOSJUN, ROS, AMPK, CYTOC_APAF1,
    CASP9, APOP, ECAD, GLUT1, HTERT, VEGF, E2F_CYCE, CDH1_UBCH10, TAK1, GSH, TCF, MIZ1, GLI,
    P70, ATM_ATR, CHK12, DNA_REPAIR, EEF2K, EEF2, P53_PTEN, LDHA, ACID_LACTIC, SNAIL]
    total_states = [MUTAGEN, GFS, NUTRIENTS, TNF_A, HYPOXIA, TGF_B, DNA_DAMAGE, P53_MDM2, AMP_ATP,
    NF1, PKC, RTK, RAGS, RAS, PI3K, PTEN, PIP3, PDK1, IKK, NFKB, RAF, ERK12, P90RSK, AKT, WNT, DSH,
    APC, GSK3, GSK3_APC, BCAT, SLUG, MTOR, HIF1, COX412, VHL, PHDS, MYC_MAX, MYC, MAX, MXI1, TSC12,
    RHEB, P53, BCL2, BAX, BAD, BCLXL, RB, E2F, P14ARF, CYCA, CYCB, CYCD, CYCE, CDH1, CDC20, UBCH10,
    P27, P21, MDM2, SMAD, SMAD_MIZ1, SMAD_E2F, P15, FADD, CASP8, BAK, JNK, FOXO, FOSJUN, ROS, AMPK,
    CYTOC_APAF1, CASP9, APOP, ECAD, GLUT1, HTERT, VEGF, E2F_CYCE, CDH1_UBCH10, TAK1, GSH, TCF, MIZ1,
    GLI, P70, ATM_ATR, CHK12, DNA_REPAIR, EEF2K, EEF2, P53_PTEN, LDHA, ACID_LACTIC, SNAIL]
    input_table = list(product([0, 1], repeat=len(input_nodes)))
    total_attractor_info = {}
    #att_result = {}
    for i in tqdm(range(len(input_table))):
        curr_input = input_nodes
        curr_input[0] = input_table[i][0]
        curr_input[1] = input_table[i][1]
        curr_input[2] = input_table[i][2]
        curr_input[3] = input_table[i][3]
        curr_input[4] = input_table[i][4]
        on_states = []
        off_states = []
        att_result = {}
        point_att = []
        cyclic_att = []
        att_num = 0
        for m in range(len(curr_input)):
            if m == 0:
                states = 'MUTAGEN'
            elif m == 1:
                states = 'GFS'
            elif m == 2:
                states = 'NUTRIENTS'
            elif m == 3:
                states = 'TNF_alpha'
            elif m == 4:
                states = 'HYPOXIA'
            if curr_input[m] == 0:
                if len(off_states) == 0:
                    off_states = [states]
                else:
                    off_states.append(states)
            elif curr_input[m] == 1:
                if len(on_states) == 0:
                    on_states = [states]
                else:
                    on_states.append(states)
        att_input_condi = {'on_states': on_states, 'off_states': off_states, 'attractor_info': {}}
        for j in range(input_num):
            curr_free_state = [np.random.randint(2) for n in range(len(free_nodes))]
            curr_state = list(input_table[i]) + curr_free_state
            trajectory = []
            next_state = total_states
            check_cyclic = 0
            check_cyclic_same = 0
            check_point_same = 0
            trajectory = ["".join(str(n) for n in curr_state)]
            for k in range(steps):
                next_state[0] = curr_state[0]
                next_state[1] = curr_state[1]
                next_state[2] = curr_state[2]
                next_state[3] = curr_state[3]
                next_state[4] = curr_state[4]
                next_state[5] = sgn(curr_state[32])
                next_state[6] = sgn(curr_state[0]+curr_state[70])
                next_state[7] = sgn(curr_state[42]+curr_state[59]-1)
                next_state[8] = sgn(-curr_state[2]+1)
                next_state[9] = sgn(-curr_state[10]+1)
                next_state[10] = sgn(curr_state[11]+curr_state[24])
                next_state[11] = sgn(curr_state[1])
                next_state[12] = sgn(curr_state[2]-curr_state[4])
                next_state[13] = sgn(-curr_state[9]+curr_state[11]+1)
                next_state[14] = sgn(curr_state[13]+curr_state[77])
                next_state[15] = sgn(1)
                next_state[16] = sgn(curr_state[14]-curr_state[15]-curr_state[92]+1)
                next_state[17] = sgn(curr_state[16]+curr_state[32]+curr_state[36])
                next_state[18] = sgn(curr_state[10]+curr_state[23]+curr_state[31]-curr_state[35]-curr_state[42]+curr_state[81])
                next_state[19] = sgn(curr_state[16]+2*curr_state[18]-curr_state[75]+curr_state[95]-1)
                next_state[20] = sgn(curr_state[10]+curr_state[13])
                next_state[21] = sgn(curr_state[20])
                next_state[22] = sgn(curr_state[17]+curr_state[21])
                next_state[23] = sgn(curr_state[16]+curr_state[17]-1)
                next_state[24] = sgn(-curr_state[42]+curr_state[85])
                next_state[25] = sgn(curr_state[24])
                next_state[26] = sgn(curr_state[15]+1)
                next_state[27] = sgn(-curr_state[22]-curr_state[23]-curr_state[25]-curr_state[31]+3)
                next_state[28] = sgn(curr_state[26]+curr_state[27]-1)
                next_state[29] = sgn(-curr_state[28]-curr_state[42]+1)
                next_state[30] = sgn(-curr_state[7]+curr_state[19]+curr_state[83])
                next_state[31] = sgn(curr_state[12]+curr_state[23]+curr_state[41]-curr_state[71]-1)
                next_state[32] = sgn(curr_state[4]+curr_state[31]-2*curr_state[34]-curr_state[35]+curr_state[36]-curr_state[42]-curr_state[68]+2)
                next_state[33] = sgn(curr_state[32])
                next_state[34] = sgn(-curr_state[4]-curr_state[70]+1)
                next_state[35] = sgn(-curr_state[4]+curr_state[70]+1)
                next_state[36] = sgn(-curr_state[5]+curr_state[37]+curr_state[38]-curr_state[39]-curr_state[62]-1)
                next_state[37] = sgn(curr_state[19]+curr_state[21]-curr_state[32]+curr_state[48]+curr_state[69]+curr_state[83]+curr_state[85]-1)
                next_state[38] = sgn(1)
                next_state[39] = sgn(curr_state[32])
                next_state[40] = sgn(-curr_state[20]-curr_state[21]-curr_state[22]-curr_state[23]+curr_state[32]+curr_state[42]+curr_state[71]+1)
                next_state[41] = sgn(-curr_state[40]+1)
                next_state[42] = sgn(curr_state[32]-curr_state[43]-curr_state[59]+curr_state[88]+1)
                next_state[43] = sgn(2*curr_state[19]-curr_state[42]-curr_state[44]-curr_state[45])
                next_state[44] = sgn(-curr_state[32]+curr_state[42]-curr_state[43]+curr_state[67])
                next_state[45] = sgn(-curr_state[20]-curr_state[22]-curr_state[23]-curr_state[32]+1)
                next_state[46] = sgn(-curr_state[42]-curr_state[45]+1)
                next_state[47] = sgn(-curr_state[50]-curr_state[51]-curr_state[52]-curr_state[53]-curr_state[59]+2)
                next_state[48] = sgn(-2*curr_state[47]-curr_state[50]-curr_state[51]+curr_state[48]+1)
                next_state[49] = sgn(curr_state[13]+curr_state[36]+curr_state[48]-3)
                next_state[50] = sgn(curr_state[50]-curr_state[47]-curr_state[55]-curr_state[57]-curr_state[58]+curr_state[79]+curr_state[80])
                next_state[51] = sgn(-curr_state[42]-curr_state[54]-curr_state[55]-curr_state[57]-curr_state[58]+1)
                next_state[52] = sgn(curr_state[19]-2*curr_state[27]+curr_state[36]-curr_state[57]-curr_state[58]-curr_state[63]-curr_state[68]+curr_state[69]+curr_state[83]+curr_state[85])
                next_state[53] = sgn(-curr_state[47]+curr_state[48]-curr_state[50]-curr_state[57]-curr_state[58])
                next_state[54] = sgn(-curr_state[50]-curr_state[51]+curr_state[55]+1)
                next_state[55] = sgn(curr_state[51]-curr_state[54])
                next_state[56] = sgn(curr_state[50]+curr_state[51]-curr_state[54]+curr_state[55]+curr_state[56])
                next_state[57] = sgn(-curr_state[23]+curr_state[32]-curr_state[36]-curr_state[50]-curr_state[51]-curr_state[52]+curr_state[61]+1)
                next_state[58] = sgn(-curr_state[23]+curr_state[32]-curr_state[36]+curr_state[42]+curr_state[61]-curr_state[77]+1)
                next_state[59] = sgn(curr_state[23]+curr_state[42]-curr_state[49]-curr_state[87]+1)
                next_state[60] = sgn(curr_state[3]+curr_state[5])
                next_state[61] = sgn(curr_state[60]+curr_state[84]-1)
                next_state[62] = sgn(curr_state[60])
                next_state[63] = sgn(curr_state[61]+curr_state[84])
                next_state[64] = sgn(curr_state[3])
                next_state[65] = sgn(curr_state[64])
                next_state[66] = sgn(curr_state[65])
                next_state[67] = sgn(curr_state[5])
                next_state[68] = sgn(-curr_state[23]+2)
                next_state[69] = sgn(curr_state[21]+curr_state[67])
                next_state[70] = sgn(-curr_state[33]-curr_state[82])
                next_state[71] = sgn(-curr_state[1]+curr_state[8]+curr_state[32]+curr_state[87]+1)
                next_state[72] = sgn(-curr_state[23]+curr_state[42]-curr_state[43]+curr_state[44]-curr_state[46]+curr_state[65]+curr_state[66])
                next_state[73] = sgn(curr_state[72])
                next_state[74] = sgn(curr_state[65]+curr_state[73])
                next_state[75] = sgn(-curr_state[19]-curr_state[30]-curr_state[95]+3)
                next_state[76] = sgn(curr_state[23]+curr_state[32]+curr_state[36]-1)
                next_state[77] = sgn(curr_state[9]+curr_state[19]+curr_state[23]+curr_state[32]+curr_state[36]-curr_state[42]-curr_state[61]-curr_state[90]-4)
                next_state[78] = sgn(curr_state[32]+curr_state[36])
                next_state[79] = sgn(curr_state[48]+curr_state[53]-1)
                next_state[80] = sgn(curr_state[54]+curr_state[56]-1)
                next_state[81] = sgn(curr_state[3])
                next_state[82] = sgn(curr_state[19]+curr_state[36]+curr_state[58])
                next_state[83] = sgn(curr_state[29]-curr_state[81])
                next_state[84] = sgn(-curr_state[36]+1)
                next_state[85] = sgn(curr_state[85])
                next_state[86] = sgn(curr_state[17]+curr_state[31])
                next_state[87] = sgn(curr_state[6])
                next_state[88] = sgn(curr_state[87])
                next_state[89] = sgn(curr_state[87])
                next_state[90] = sgn(curr_state[22]+curr_state[86])
                next_state[91] = sgn(-curr_state[89]+1)
                next_state[92] = sgn(curr_state[15]+curr_state[42]-1)
                next_state[93] = sgn(curr_state[32]+curr_state[36]-1)
                next_state[94] = sgn(curr_state[93])
                next_state[95] = sgn(curr_state[19]-curr_state[27]-curr_state[42]+curr_state[60]-1)
                if curr_state == next_state:
                    point_att_ele = "".join(str(n) for n in next_state)
                    att = {'attractor': point_att_ele, 'type': 'point', 'basin_size': 1}
                    if len(point_att) == 0:
                        point_att = [point_att_ele]
                        att_result[att_num] = att
                        att_num += 1
                        set_trace()
                    else:
                        for point_list in range(len(point_att)):
                            if point_att_ele == point_att[point_list]:
                                for att_list_po in range(len(att_result)):
                                    att_element = att_result[att_list_po]
                                    if att == att_element:
                                        att_result[att_list_po]['basin_size'] += 1
                                        check_point_same = 1
                                        set_trace()
                                        break
                                    att_list_po += 1
                            if check_point_same == 1:
                                set_trace()
                                break
                            point_list += 1
                        if check_point_same != 1:
                            point_att.append(point_att_ele)
                            att_result[att_num] = att
                            att_num += 1
                            set_trace()
                    break
                elif curr_state != next_state:
                    if len(trajectory) == 1:
                        trajectory.append("".join(str(n) for n in next_state))
                        set_trace()
                    elif len(trajectory) > 1:
                        for traj in range(len(trajectory)):
                            if "".join(str(n) for n in next_state) == trajectory[traj]:
                                cyc_att_ele = trajectory[traj:len(trajectory)]
                                att = {'attractor': cyc_att_ele, 'type': 'cyclic', 'basin_size': 1, 'cyclic_size': len(cyc_att_ele)}
                                if len(cyclic_att) == 0:
                                    cyclic_att = [cyc_att_ele]
                                    att_result[att_num] = att
                                    att_num += 1
                                    set_trace()
                                    break
                                else:
                                    for cyclic_list in range(len(cyclic_att)):
                                        if cyc_att_ele == cyclic_att[cyclic_list]:
                                            for att_list_cyc in range(len(att_result)):
                                                att_element = att_result[att_list_cyc]
                                                if att == att_element:
                                                    att_result[att_list_cyc]['basin_size'] += 1
                                                    check_cyclic_same = 1
                                                    set_trace()
                                                    break
                                                att_list_cyc += 1
                                        if check_cyclic_same == 1:
                                            set_trace()
                                            break
                                        cyclic_list += 1
                                    if check_cyclic_same != 1:
                                        cyclic_att.append(cyc_att_ele)
                                        att_result[att_num] = att
                                        att_num += 1
                                        set_trace()
                                check_cyclic = 1
                                break
                            traj += 1
                        trajectory.append("".join(str(n) for n in next_state))
                if check_cyclic == 1:
                    set_trace()
                    break
                curr_state = next_state
                #set_trace()
                k += 1
            j += 1
        att_input_condi[i]['attractor_info'] = att_result
        if len(total_attractor_info) == 0:
            total_attractor_info = att_input_condi
            set_trace()
        else:
            total_attractor_info[i] = att_input_condi
            set_trace()
        i += 1




    att_result = json.load(open(config['input']['input_a'], 'rb'))
    origin_network = pd.read_csv(config['input']['input_b'])
    attractor
    nodes_set = []
    input_num = 100000
    set_trace()
    i = 0
    for i in range(len(origin_network['Output'])):
        nodes_set.append(origin_network['Output'][i])
        i += 1

    #nodes_set = [MUTAGEN, GFS, NUTRIENTS, TNF_A, HYPOXIA, TGF_B, DNA_DAMAGE, P53_MDM2, AMP_ATP,
    #NF1, PKC, RTK, RAGS, RAS, PI3K, PTEN, PIP3, PDK1, IKK, NFKB, RAF, ERK12, P90RSK, AKT, WNT, DSH,
    #APC, GSK3, GSK3_APC, BCAT, SLUG, MTOR, HIF1, COX412, VHL, PHDS, MYC_MAX, MYC, MAX, MXI1, TSC12,
    #RHEB, P53, BCL2, BAX, BAD, BCLXL, RB, E2F, P14ARF, CYCA, CYCB, CYCD, CYCE, CDH1, CDC20, UBCH10,
    #P27, P21, MDM2, SMAD, SMAD_MIZ1, SMAD_E2F, P15, FADD, CASP8, BAK, JNK, FOXO, FOSJUN, ROS, AMPK,
    #CYTOC_APAF1, CASP9, APOP, ECAD, GLUT1, HTERT, VEGF, E2F_CYCE, CDH1_UBCH10, TAK1, GSH, TCF, MIZ1,
    #GLI, P70, ATM_ATR, CHK12, DNA_REPAIR, EEF2K, EEF2, P53_PTEN, LDHA, ACID_LACTIC, SNAIL]

    i = 0
    for i in range(len(nodes_set)):
        label_node = label[i]
        if label_node == 'APOP':
            apop = i
        elif label_node == 'CYCA':
            pro_qui_1 = i
        elif label_node == 'CYCB':
            pro_qui_2 = i
        elif label_node == 'CYCD':
            pro_qui_3 = i
        elif label_node == 'CYCE':
            pro_qui_4 = i
        i += 1

    set_trace()

    i = 0
    for i in range(32):
        att_info = attractor_result[input_num*i:input_num*(i+1)-1]
        att_total = att_info.get['attractor']
        basin_size  = 0
        total_attractor_info = {'input_condition': {'on_states': '', 'off_states': ''}, 'total_attractors': {}}
        total_attractor_info['input_condition']['on_states'] = att_info[1000000*i]['on_states']
        total_attractor_info['input_condition']['off_states'] = att_info[1000000*i]['off_states']
        for j in range(len(att_total)-1):
            if att_total[j] == att_total[j+1]:
                basin_size += 1
            elif att_total[j] != att_total[j+1]:
                att_input_condi = att_total[j]
                attractor_info = {'attractor': att_total[j], 'basin_size': basin_size, 'attractor_type': att_info[j]['type'], 'phenotype': ''}
                basin_size = 0
                if att_info[j]['type'] == 'point':
                    if att_input_condi[apop] == 1:
                        attractor_info['phenotype'] = 'Apoptosis'
                    #else:
                        #attractor_info['phenotype'] = 'Quiescent'
                elif att_info[j]['type'] == 'cyclic':
                    for k in range(len(att_total[j])):
                        att_cycle = att_total[j][k]
                        if k == 0 & att_cycle[pro_qui_3] == 1:
                            if k == 1 & att_cycle[pro_qui_4] == 1:
                                if k == 2 & att_cycle[pro_qui_1] == 1:
                                    if k == 3 & att_cycle[pro_qui_2] == 1:
                                        attractor_info['phenotype'] = 'proliferation'
                        else:
                            attractor_info['phenotype'] = 'Quiescent'
                        k += 1
                total_attractor_info['total_attractors'] = attractor_info # make this information append
            j += 1
        i += 1
