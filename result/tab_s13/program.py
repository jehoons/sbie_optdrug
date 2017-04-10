# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from os.path import dirname,join,exists
from sbie_optdrug.result import tab_s13
from ipdb import set_trace
import json
import pandas as pd
from itertools import combinations,product
from copy import deepcopy
from tqdm import tqdm
import numpy as np

""" requirements """
inputfile_a = join(dirname(__file__), '..','tab_s13','fumia_network.csv')
#inputfile_b = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s1.json')
#inputfile_c = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s4.json')
#inputfile_d = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s1.json')
#inputfile_e = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s4.json')
#inputfile_f = join(dirname(__file__), '..','tab_s5','TABLE.S5C.DRUG_data.json')
#inputfile_g = join(dirname(__file__), '..','tab_s7','untracked_Table_S7A_Fumia-processed.csv')
#inputfile_h = join(dirname(__file__), '..','tab_s7','untracked_Table_S7F-Input-combinations-APC.json')
#inputfile_i = join(dirname(__file__), '..','tab_s7','untracked_Table_S7G-Scanning-results-APC.json')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S13A.simulation_result.json')
#outputfile_b = join(dirname(__file__), 'TABLE.S10B_total_attractor_input_condition.csv')
#outputfile_d = join(dirname(__file__), 'TABLE.S8B.MUTATION_data_s4.json')
#outputfile_e = join(dirname(__file__), 'TABLE.S8C.DRUG_data.json')

config = {
    'input': {
        'input_a': inputfile_a,
        #'input_b': inputfile_b,
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

def run_a(config): #network model
    origin_file = config
    steps = 50
    input_num = 100000
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
    input_table = list(product([0, 1], repeat=len(input_nodes)))
    att_result = {}
    check_cyclic = 0
    for i in tqdm(range(len(input_table))):
        MUTAGEN = input_table[i][0]
        GFS = input_table[i][1]
        NUTRIENTS = input_table[i][2]
        TNF_A = input_table[i][3]
        HYPOXIA = input_table[i][4]
        curr_input = [MUTAGEN, GFS, NUTRIENTS, TNF_A, HYPOXIA]
        check_cyclic = 0
        for j in range(input_num):
            curr_free_state = [np.random.randint(2) for n in range(len(free_nodes))]
            curr_state = curr_input + curr_free_state
            trajectory = []
            for k in range(steps):
                trajectory = [curr_state]
                TGF_B = sgn(curr_state[32])
                DNA_DAMAGE = sgn(curr_state[0]+curr_state[70])
                P53_MDM2 = sgn(curr_state[42]+curr_state[59]-1)
                AMP_ATP = sgn(-curr_state[2]+1)
                NF1 = sgn(-curr_state[10]+1)
                PKC = sgn(curr_state[11]+curr_state[24])
                RTK = sgn(curr_state[1])
                RAGS = sgn(curr_state[2]-curr_state[4])
                RAS = sgn(-curr_state[9]+curr_state[11]+1)
                PI3K = sgn(curr_state[13]+curr_state[77])
                PTEN = sgn(1)
                PIP3 = sgn(curr_state[14]-curr_state[15]-curr_state[92]+1)
                PDK1 = sgn(curr_state[16]+curr_state[32]+curr_state[36])
                IKK = sgn(curr_state[10]+ curr_state[23]+ curr_state[31]-curr_state[35]-curr_state[42]+curr_state[81])
                NFKB = sgn(curr_state[16]+2*curr_state[18]-curr_state[75]+curr_state[95]-1)
                RAF = sgn(curr_state[10]+curr_state[13])
                ERK12 = sgn(curr_state[20])
                P90RSK = sgn(curr_state[17]+curr_state[21])
                AKT = sgn(curr_state[16]+curr_state[17]-1)
                WNT = sgn(-curr_state[42]+curr_state[85])
                DSH = sgn(curr_state[24])
                APC = sgn(curr_state[15]+1)
                GSK3 = sgn(-curr_state[22]-curr_state[23]-curr_state[25]-curr_state[31]+3)
                GSK3_APC = sgn(curr_state[26]+curr_state[27]-1)
                BCAT = sgn(-curr_state[28]-curr_state[42]+1)
                SLUG = sgn(-curr_state[7]+curr_state[19]+curr_state[83])
                MTOR = sgn(curr_state[12]+curr_state[23]+curr_state[41]-curr_state[71]-1)
                HIF1 = sgn(curr_state[4]+curr_state[31]-2*curr_state[34]-curr_state[35]+curr_state[36]-curr_state[42]-curr_state[68]+2)
                COX412 = sgn(curr_state[32])
                VHL = sgn(-curr_state[4]-curr_state[70]+1)
                PHDS = sgn(-curr_state[4]+curr_state[70]+1)
                MYC_MAX = sgn(-curr_state[5]+curr_state[37]+curr_state[38]-curr_state[39]-curr_state[62]-1)
                MYC = sgn(curr_state[19]+curr_state[21]-curr_state[32]+curr_state[48]+curr_state[69]+curr_state[83]+curr_state[85]-1)
                MAX = sgn(1)
                MXI1 = sgn(curr_state[32])
                TSC12 = sgn(-curr_state[20]-curr_state[21]-curr_state[22]-curr_state[23]+curr_state[32]+curr_state[42]+curr_state[71]+1)
                RHEB = sgn(-curr_state[40]+1)
                P53 = sgn(curr_state[32]-curr_state[43]-curr_state[59]+curr_state[88]+1)
                BCL2 = sgn(2*curr_state[19]-curr_state[42]-curr_state[44]-curr_state[45])
                BAX = sgn(-curr_state[32]+curr_state[42]-curr_state[43]+curr_state[67])
                BAD = sgn(-curr_state[20]-curr_state[22]-curr_state[23]-curr_state[32]+1)
                BCLXL = sgn(-curr_state[42]-curr_state[45]+1)
                RB = sgn(-curr_state[50]-curr_state[51]-curr_state[52]-curr_state[53]-curr_state[59]+2)
                E2F = sgn(-2*curr_state[47]-curr_state[50]-curr_state[51]+curr_state[48]+1)
                P14ARF = sgn(curr_state[13]+curr_state[36]+curr_state[48]-3)
                CYCA = sgn(curr_state[50]-curr_state[47]-curr_state[55]-curr_state[57]-curr_state[58]+curr_state[79]+curr_state[80])
                CYCB = sgn(-curr_state[42]-curr_state[54]-curr_state[55]-curr_state[57]-curr_state[58]+1)
                CYCD = sgn(curr_state[19]-2*curr_state[27]+curr_state[36]-curr_state[57]-curr_state[58]-curr_state[63]-curr_state[68]+curr_state[69]+curr_state[83]+curr_state[85])
                CYCE = sgn(-curr_state[47]+curr_state[48]-curr_state[50]-curr_state[57]-curr_state[58])
                CDH1 = sgn(-curr_state[50]-curr_state[51]+curr_state[55]+1)
                CDC20 = sgn(curr_state[51]-curr_state[54])
                UBCH10 = sgn(curr_state[50]+curr_state[51]-curr_state[54]+curr_state[55]+curr_state[56])
                P27 = sgn(-curr_state[23]+curr_state[32]-curr_state[36]-curr_state[50]-curr_state[51]-curr_state[52]+curr_state[61]+1)
                P21 = sgn(-curr_state[23]+curr_state[32]-curr_state[36]+curr_state[42]+curr_state[61]-curr_state[77]+1)
                MDM2 = sgn(curr_state[23]+curr_state[42]-curr_state[49]-curr_state[87]+1)
                SMAD = sgn(curr_state[3]+curr_state[5])
                SMAD_MIZ1 = sgn(curr_state[60]+curr_state[84]-1)
                SMAD_E2F = sgn(curr_state[60])
                P15 = sgn(curr_state[61]+curr_state[84])
                FADD = sgn(curr_state[3])
                CASP8 = sgn(curr_state[64])
                BAK = sgn(curr_state[65])
                JNK = sgn(curr_state[5])
                FOXO = sgn(-curr_state[23]+2)
                FOSJUN = sgn(curr_state[21]+curr_state[67])
                ROS = sgn(-curr_state[33]-curr_state[82])
                AMPK = sgn(-curr_state[1]+curr_state[8]+curr_state[32]+curr_state[87]+1)
                CYTOC_APAF1 = sgn(-curr_state[23]+curr_state[42]-curr_state[43]+curr_state[44]-curr_state[46]+curr_state[65]+curr_state[66])
                CASP9 = sgn(curr_state[72])
                APOP = sgn(curr_state[65]+curr_state[73])
                ECAD = sgn(-curr_state[19]-curr_state[30]-curr_state[95]+3)
                GLUT1 = sgn(curr_state[23]+curr_state[32]+curr_state[36]-1)
                HTERT = sgn(curr_state[9]+curr_state[19]+curr_state[23]+curr_state[32]+curr_state[36]-curr_state[42]-curr_state[61]-curr_state[90]-4)
                VEGF = sgn(curr_state[32]+curr_state[36])
                E2F_CYCE = sgn(curr_state[48]+curr_state[53]-1)
                CDH1_UBCH10 = sgn(curr_state[54]+curr_state[56]-1)
                TAK1 = sgn(curr_state[3])
                GSH = sgn(curr_state[19]+curr_state[36]+curr_state[58])
                TCF = sgn(curr_state[29]-curr_state[81])
                MIZ1 = sgn(-curr_state[36]+1)
                GLI = sgn(curr_state[85])
                P70 = sgn(curr_state[17]+curr_state[31])
                ATM_ATR = sgn(curr_state[6])
                CHK12 = sgn(curr_state[87])
                DNA_REPAIR = sgn(curr_state[87])
                EEF2K = sgn(curr_state[22]+curr_state[86])
                EEF2 = sgn(-curr_state[89]+1)
                P53_PTEN = sgn(curr_state[15]+curr_state[42]-1)
                LDHA = sgn(curr_state[32]+curr_state[36]-1)
                ACID_LACTIC = sgn(curr_state[93])
                SNAIL = sgn(curr_state[19]-curr_state[27]-curr_state[42]+curr_state[60]-1)
                next_state = [MUTAGEN, GFS, NUTRIENTS, TNF_A, HYPOXIA, TGF_B, DNA_DAMAGE, P53_MDM2, AMP_ATP,
                NF1, PKC, RTK, RAGS, RAS, PI3K, PTEN, PIP3, PDK1, IKK, NFKB, RAF, ERK12, P90RSK, AKT, WNT, DSH,
                APC, GSK3, GSK3_APC, BCAT, SLUG, MTOR, HIF1, COX412, VHL, PHDS, MYC_MAX, MYC, MAX, MXI1, TSC12,
                RHEB, P53, BCL2, BAX, BAD, BCLXL, RB, E2F, P14ARF, CYCA, CYCB, CYCD, CYCE, CDH1, CDC20, UBCH10,
                P27, P21, MDM2, SMAD, SMAD_MIZ1, SMAD_E2F, P15, FADD, CASP8, BAK, JNK, FOXO, FOSJUN, ROS, AMPK,
                CYTOC_APAF1, CASP9, APOP, ECAD, GLUT1, HTERT, VEGF, E2F_CYCE, CDH1_UBCH10, TAK1, GSH, TCF, MIZ1,
                GLI, P70, ATM_ATR, CHK12, DNA_REPAIR, EEF2K, EEF2, P53_PTEN, LDHA, ACID_LACTIC, SNAIL]
                for m in range(len(curr_input)):
                    on_states = []
                    off_states = []
                    if curr_input[m] == 0:
                        if m == 0:
                            if len(off_states) == 0: off_states = ['MUTAGEN']
                            else: off_states.append('MUTAGEN')
                        elif m == 1:
                            if len(off_states) == 0: off_states = ['GFS']
                            else: off_states.append('GFS')
                        elif m == 2:
                            if len(off_states) == 0: off_states = ['NUTRIENTS']
                            else: off_states.append('NUTRIENTS')
                        elif m == 3:
                            if len(off_states) == 0: off_states = ['TNF_alpha']
                            else: off_states.append('TNF_alpha')
                        elif m == 4:
                            if len(off_states) == 0: off_states = ['HYPOXIA']
                            else: off_states.append('HYPOXIA')
                    elif curr_input[m] == 1:
                        if m == 0:
                            if len(on_states) == 0: on_states = ['MUTAGEN']
                            else: on_states.append('MUTAGEN')
                        elif m == 1:
                            if len(on_states) == 0: on_states = ['GFS']
                            else: on_states.append('GFS')
                        elif m == 2:
                            if len(on_states) == 0: on_states = ['NUTRIENTS']
                            else: on_states.append('NUTRIENTS')
                        elif m == 3:
                            if len(on_states) == 0: on_states = ['TNF_alpha']
                            else: on_states.append('TNF_alpha')
                        elif m == 4:
                            if len(on_states) == 0: on_states = ['HYPOXIA']
                            else: on_states.append('HYPOXIA')
                if cmp(curr_state,next_state) == 0:
                    att = {i: {'on_states': on_states, 'off_states': off_states, 'attractor': next_state, 'type': 'point'}}
                    if len(att_result) == 0:
                        att_result = att
                    else:
                        att_result = dict(att_result.items() + att.items())
                    break
                elif cmp(curr_state,next_state) != 0:
                    if len(trajectory) == 1:
                        trajectory.append(next_state)
                    elif len(trajectory) > 1:
                        for l in range(len(trajectory)):
                            if cmp(next_state,trajectory[l]) == 0:
                                check_cyclic = 1
                                att = {i: {'on_states': on_states, 'off_states': off_states, 'attractor': trajectory[k:len(trajectory)], 'type': 'cyclic'}}
                                if len(att_result) == 0:
                                    att_result = att
                                else:
                                    att_result = dict(att_result.items() + att.items())
                            l += 1
                        trajectory.append(next_state)
                if check_cyclic == 1:
                    break
                curr_state = [MUTAGEN, GFS, NUTRIENTS, TNF_A, HYPOXIA, TGF_B, DNA_DAMAGE, P53_MDM2, AMP_ATP,
                NF1, PKC, RTK, RAGS, RAS, PI3K, PTEN, PIP3, PDK1, IKK, NFKB, RAF, ERK12, P90RSK, AKT, WNT, DSH,
                APC, GSK3, GSK3_APC, BCAT, SLUG, MTOR, HIF1, COX412, VHL, PHDS, MYC_MAX, MYC, MAX, MXI1, TSC12,
                RHEB, P53, BCL2, BAX, BAD, BCLXL, RB, E2F, P14ARF, CYCA, CYCB, CYCD, CYCE, CDH1, CDC20, UBCH10,
                P27, P21, MDM2, SMAD, SMAD_MIZ1, SMAD_E2F, P15, FADD, CASP8, BAK, JNK, FOXO, FOSJUN, ROS, AMPK,
                CYTOC_APAF1, CASP9, APOP, ECAD, GLUT1, HTERT, VEGF, E2F_CYCE, CDH1_UBCH10, TAK1, GSH, TCF, MIZ1,
                GLI, P70, ATM_ATR, CHK12, DNA_REPAIR, EEF2K, EEF2, P53_PTEN, LDHA, ACID_LACTIC, SNAIL]
                k += 1
            j += 1
        i += 1
    return att_result

def run_b(config=None, force=False):

    origin_network = pd.read_csv(config['input']['input_a'])
    outputfile = config['output']['output_a']
    if exists(outputfile) and force==False:
         return

    import time
    from multiprocessing import Pool
    p = Pool(60)
    attractor_result = p.map(run_a, origin_network['ID'])

    with open(outputfile, 'w') as fileout:
        json.dump({'scanning_results': attractor_result}, fileout, indent=3)
