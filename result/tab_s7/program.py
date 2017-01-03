# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import json,re
from ipdb import set_trace
from termutil import progressbar
from os import system
from os.path import dirname,join,exists
from boolean3_addon import attr_cy
import numpy as np

from sbie_optdrug.result import tab_s3
from sbie_optdrug.result import tab_s7
from boolean3 import Model
from boolean3_addon import attractor
import pandas as pd

if not exists('engine.pyx'):
    data = tab_s7.load_a()
    model = "\n".join( data['equation'].values.tolist() )
    attr_cy.build(model)

import pyximport; pyximport.install()
import engine


def getconfig():
    "return config object"
    return tab_s7.config


def run_a(config=None, force=False):
    "푸미아네트워크 이큐에이션을 준비한다."
    if exists(config['output']['a']) and force==False:
        return

    data = tab_s3.load()
    eq_list = data['equation'].values.tolist()

    node_set = set()
    for eq in eq_list:
        text2 = eq.replace('and', ' ')
        text2 = text2.replace('or', ' ')
        text2 = text2.replace('not', ' ')
        text2 = text2.replace('*=', ' ')
        nodes = set(text2.split(' '))
        node_set = node_set.union(nodes)

    for el in ['', '0', '1', 'True', 'False']:
        if el in node_set:
            node_set.remove(el)

    datadict = {}

    for node in node_set:
        if node == '':
            continue
        data = { 'type': 'normal', 'value': None }
        datadict[node] = data
    init_list = []

    for node in node_set:
        init_list.append('%s=Random' % node)

    alleq = init_list + eq_list
    model_string = "\n".join(init_list + eq_list)

    with open(config['output']['a'], 'w') as f:
        f.write(model_string)

    df0 = pd.DataFrame([], columns=['node'])
    df0['node'] = list(node_set)
    df0.to_csv('untracked_fumia_node_set.csv', index=False)


def run_b(config=None, force=False):
    "모델의 베이신크기를 계산."
    outputfile = config['output']['b']
    if exists(outputfile) and force==False:
        return

    data = tab_s7.load_a()
    model = "\n".join( data['equation'].values.tolist() )

    samples = config['parameters']['samples']
    steps = config['parameters']['steps']
    on_states = config['parameters']['on_states']
    off_states = config['parameters']['off_states']

    attr_cy.build(model, on_states=on_states, off_states=off_states)
    result_data = attr_cy.run(samples=samples, steps=steps, debug=True)
    # on_states=[], off_states=[]
    json.dump(result_data, open(outputfile, 'w'), indent=4)


def run_b_plot(config=None, force=False):
    "draw figure"
    outputfile = config['output']['b_plot']
    if exists(outputfile) and force==False:
        return

    result_data = tab_s7.load_b()
    ratio_list = []
    labels = []
    for attrk in result_data['attractors'].keys():
        r = result_data['attractors'][attrk]['ratio']
        ratio_list.append(r)
        labels.append(attrk)

    fig, ax = plt.subplots()

    ax.bar(np.arange(len(ratio_list)), ratio_list)
    ax.set_xticklabels(labels)
    plt.savefig(outputfile)


def run_c(config=None, force=False):
    '''입력의 조합들을 생성한다. 두개의 노드를 동시에 타겟할 수 있다고 가정하였다.
    타겟을 하지 않은 조건을 포함하였다.'''
    from itertools import combinations,product
    from copy import deepcopy

    outputfile = config['output']['c']
    if exists(outputfile) and force==False:
         return

    result_data = tab_s7.load_b()
    nodes = result_data['labels']
    input_nodes = config['parameters']['input_nodes']

    free_nodes = set(nodes) - set(input_nodes)
    free_nodes = list(set(free_nodes))
    combi1 = [c for c in combinations(free_nodes, 1)]
    combi2 = [c for c in combinations(free_nodes, 2)]
    combi3 = [c for c in combinations(free_nodes, 3)]

    combi = combi1 + combi2 + [()]

    table = list(product([False, True], repeat=len(input_nodes)))

    config_list = []
    for k,inp in enumerate(table):
        progressbar.update(k, len(table))
        for com in combi:
            on_states = []
            off_states = []
            off_states = off_states + [c for c in com]
            for i,t in enumerate(inp):
                if t :
                    on_states.append( input_nodes[i] )
                else:
                    off_states.append( input_nodes[i] )

            config1 = deepcopy(config)
            config1['parameters']['on_states'] = deepcopy(on_states)
            config1['parameters']['off_states'] = deepcopy(off_states)
            config_list.append(deepcopy(config1))

    with open(outputfile, 'w') as outfile:
        json.dump({'configs': config_list, 'num_configs': len(config_list)},
            outfile, indent=4)


def myengine(config):
    samples = config['parameters']['samples']
    steps = config['parameters']['steps']
    on_states = config['parameters']['on_states']
    off_states = config['parameters']['off_states']

    result = engine.main(samples=samples, steps=steps, debug=False, \
        progress=False, on_states=on_states, off_states=off_states)

    result['parameters'] = {
        'samples': samples,
        'steps': steps
        }

    return result


def run_d(config=None, force=False):

    outputfile = config['output']['d']
    if exists(outputfile) and force==False:
         return

    data = json.load(open('TABLE_S7C_INPUT_COMBINATIONS.json','r'))

    import time
    from multiprocessing import Pool
    p = Pool(60)
    scanning_result = p.map(myengine, data['configs'])

    with open(outputfile, 'w') as fileout:
        json.dump({'scanning_results': scanning_result}, fileout, indent=1)


def run_e(config=None, force=False):
    from io import StringIO
    fumia_2013_regulation_data = StringIO('''ID,Source,Target,Type,Reference,
    1,input,Mutagenic,activation,,
    2,input,GFs,activation,,
    3,input,Nutrients,activation,,
    4,input,TNF-alpha,activation,,
    5,input,Hypoxia,activation,,
    6,HIF1,TGF-beta,activation,,
    7,Mutagen,DNA_Damage,activation,,
    8,ROS,DNA_Damage,activation,,
    9,p53,p53/Mdm2,activation,,
    10,Mdm2,p53/Mdm2,activation,,
    11,Nutrients,AMP/ATP,inhibition,,
    12,PKC,NF1,inhibition,,
    13,RTK,PKC,activation,,
    14,WNT,PKC,activation,,
    15,GFs,RTK,activation,,
    16,Nutrients,RAGS,activation,,
    17,Hypoxia,RAGS,inhibition,,
    18,NF1,Ras,inhibition,,
    19,RTK,Ras,activation,,
    20,Ras,PI3K,activation,,
    21,hTERT,PI3K,activation,,
    22,1,PTEN,activation,,
    23,PI3K,PIP3,activation,,
    24,PTEN,PIP3,inhibition,,
    25,p53/PTEN,PIP3,inhibition,,
    26,PIP3,PDK1,activation,,
    27,HIF1,PDK1,activation,,
    28,Myc/Max,PDK1,activation,,
    29,PKC,IKK,activation,,
    30,AKT,IKK,activation,,
    31,mTOR,IKK,activation,,
    32,PHDs,IKK,inhibition,,
    33,p53,IKK,inhibition,,
    34,TAK1,IKK,activation,,
    35,PIP3,NF-kappaB,activation,,
    36,IKK,NF-kappaB,activation,,
    37,E-cadherin,NF-kappaB,inhibition,,
    38,Snail,NF-kappaB,activation,,
    39,PKC,RAF,activation,,
    40,Ras,RAF,activation,,
    41,RAF,ERK-1/2,activation,,
    42,PDK1,p90RSK,activation,,
    43,ERK-1/2,p90RSK,activation,,
    44,PIP3,AKT,activation,,
    45,PDK1,AKT,activation,,
    46,p53,WNT,inhibition,,
    47,Gli,WNT,activation,,
    48,WNT,Dsh,activation,,
    49,PTEN,APC,activation,,
    50,p90,GSK-3,inhibition,,
    51,AKT,GSK-3,inhibition,,
    52,Dsh,GSK-3,inhibition,,
    53,mTOR,GSK-3,inhibition,,
    54,APC,GSK-3/APC,activation,,
    55,GSK-3,GSK-3/APC,activation,,
    56,GSK-3/APC,beta-catenin,inhibition,,
    57,p53,beta-catenin,inhibition,,
    58,p53/Mdm2,Slug,inhibition,,
    59,NF-kappaB,Slug,activation,,
    60,TCF,Slug,activation,,
    61,RAGS,mTOR,activation,,
    62,AKT,mTOR,activation,,
    63,RHEB,mTOR,activation,,
    64,AMPK,mTOR,inhibition,,
    65,Hypoxia,HIF1,activation,,
    66,mTOR,HIF1,activation,,
    67,VHL,HIF1,inhibition,,
    68,PHDs,HIF1,inhibition,,
    69,Myc/Max,HIF1,activation,,
    70,p53,HIF1,inhibition,,
    71,FOXO,HIF1,inhibition,,
    72,HIF1,COX412,activation,,
    73,Hypoxia,VHL,inhibition,,
    74,ROS,VHL,inhibition,,
    75,Hypoxia,PHDs,inhibition,,
    76,ROS,PHDs,activation,,
    77,TGF-alpha,Myc/Max,inhibition,,
    78,Myc,Myc/Max,activation,,
    79,Max,Myc/Max,activation,,
    80,MXI1,Myc/Max,inhibition,,
    81,SmadE2F,Myc/Max,inhibition,,
    82,NF-kappaB,Myc,activation,,
    83,ERK,Myc,activation,,
    84,HIF1,Myc,inhibition,,
    85,E2F,Myc,activation,,
    86,FosJun,Myc,activation,,
    87,TCF,Myc,activation,,
    88,Gli,Myc,activation,,
    89,1,Max,activation,,
    90,HIF1,MXI1,activation,,
    91,RAF,TSC1/2,inhibition,,
    92,ERK-1/2,TSC1/2,inhibition,,
    93,p90,TSC1/2,inhibition,,
    94,AKT,TSC1/2,inhibition,,
    95,HIF1,TSC1/2,activation,,
    96,p53,TSC1/2,activation,,
    97,AMPK,TSC1/2,activation,,
    98,TSC1/2,RHEB,inhibition,,
    99,HIF1,p53,activation,,
    100,Bcl-2,p53,inhibition,,
    101,Mdm2,p53,inhibition,,
    102,CHK1/2,p53,activation,,
    103,NF-kappaB,Bcl-2,activation,,
    104,p53,Bcl-2,inhibition,,
    105,BAX,Bcl-2,inhibition,,
    106,BAD,Bcl-2,inhibition,,
    107,HIF1,BAX,inhibition,,
    108,p53,BAX,activation,,
    109,Bcl-2,BAX,inhibition,,
    110,JNK,BAX,activation,,
    111,RAF,BAD,inhibition,,
    112,p90,BAD,inhibition,,
    113,AKT,BAD,inhibition,,
    114,HIF1,BAD,inhibition,,
    115,p53,Bcl-XL,inhibition,,
    116,BAD,Bcl-XL,inhibition,,
    117,CyclinA,Rb,inhibition,,
    118,CyclinB,Rb,inhibition,,
    119,CyclinD,Rb,inhibition,,
    120,CyclinE,Rb,inhibition,,
    121,Mdm2,Rb,inhibition,,
    122,Rb,E2F,inhibition,,
    123,CyclinA,E2F,inhibition,,
    124,CyclinB,E2F,inhibition,,
    125,E2F,E2F,activation,,
    126,Ras,p14ARF,activation,,
    127,Myc/Max,p14ARF,activation,,
    128,E2F,p14ARF,activation,,
    129,CyclinA,CyclinA,activation,,
    130,Rb,CyclinA,inhibition,,
    131,cdc20,CyclinA,inhibition,,
    132,p27,CyclinA,inhibition,,
    133,p21,CyclinA,inhibition,,
    134,E2F/CyclinE,CyclinA,activation,,
    135,cdh1/UbcH10,CyclinA,activation,,
    136,p53,CyclinB,inhibition,,
    137,cdh1,CyclinB,inhibition,,
    138,cdc20,CyclinB,inhibition,,
    139,p27,CyclinB,inhibition,,
    140,p21,CyclinB,inhibition,,
    141,NF-kappaB,CyclinD,activation,,
    142,GSK-3,CyclinD,inhibition,,
    143,Myc/Max,CyclinD,activation,,
    144,p27,CyclinD,inhibition,,
    145,p21,CyclinD,inhibition,,
    146,p15,CyclinD,inhibition,,
    147,FOXO,CyclinD,inhibition,,
    148,FosJun,CyclinD,activation,,
    149,TCF,CyclinD,activation,,
    150,Gli,CyclinD,activation,,
    151,Rb,CyclinE,inhibition,,
    152,E2F,CyclinE,activation,,
    153,CyclinA,CyclinE,inhibition,,
    154,p27,CyclinE,inhibition,,
    155,p21,CyclinE,inhibition,,
    156,CyclinA,cdh1,inhibition,,
    157,CyclinB,cdh1,inhibition,,
    158,cdc20,cdh1,activation,,
    159,CyclinB,cdc20,activation,,
    160,cdh1,cdc20,inhibition,,
    161,CyclinA,UbcH10,activation,,
    162,CyclinB,UbcH10,activation,,
    163,cdh1,UbcH10,inhibition,,
    164,cdc20,UbcH10,activation,,
    165,UbcH10,UbcH10,activation,,
    166,AKT,p27,inhibition,,
    167,HIF1,p27,activation,,
    168,Myc/Max,p27,inhibition,,
    169,CyclinA,p27,inhibition,,
    170,CyclinB,p27,inhibition,,
    171,CyclinD,p27,inhibition,,
    172,Smad/Miz-1,p27,activation,,
    173,AKT,p21,inhibition,,
    174,HIF1,p21,activation,,
    175,Myc/Max,p21,inhibition,,
    176,p53,p21,activation,,
    177,Smad/Miz-1,p21,activation,,
    178,hTERT,p21,inhibition,,
    179,AKT,Mdm2,activation,,
    180,p53,Mdm2,activation,,
    181,p14ARF,Mdm2,inhibition,,
    182,ATM/ATR,Mdm2,inhibition,,
    183,TNF-alpha,Smad,activation,,
    184,TGF-beta,Smad,activation,,
    185,Smad,Smad/Miz-1,activation,,
    186,Miz-1,Smad/Miz-1,activation,,
    187,Smad,Smad/E2F,activation,,
    188,Smad/Miz-1,p15,activation,,
    189,Miz-1,p15,activation,,
    190,TNF-alpha,FADD,activation,,
    191,FADD,Caspase8,activation,,
    192,Caspase8,Bak,activation,,
    193,TGF-beta,JNK,activation,,
    194,AKT,FOXO,inhibition,,
    195,ERK-1/2,FosJun,activation,,
    196,JNK,FosJun,activation,,
    197,COX412,ROS,inhibition,,
    198,GSH,ROS,inhibition,,
    199,GFs,AMPK,inhibition,,
    200,AMP/ATP,AMPK,activation,,
    201,HIF1,AMPK,activation,,
    202,ATM/ATR,AMPK,activation,,
    203,AKT,Cytoc/APAF1,inhibition,,
    204,p53,Cytoc/APAF1,activation,,
    205,Bcl-2,Cytoc/APAF1,inhibition,,
    206,BAX,Cytoc/APAF1,activation,,
    207,Bcl-XL,Cytoc/APAF1,inhibition,,
    208,Caspase8,Cytoc/APAF1,activation,,
    209,Bak,Cytoc/APAF1,activation,,
    210,Cytoc/APAF1,Caspase9,activation,,
    211,Caspase8,Apoptosis,activation,,
    212,Caspase9,Apoptosis,activation,,
    213,NF-kappaB,E-cadherin,inhibition,,
    214,Slug,E-cadherin,inhibition,,
    215,Snail,E-cadherin,inhibition,,
    216,AKT,Glut-1,activation,,
    217,HIF1,Glut-1,activation,,
    218,Myc/Max,Glut-1,activation,,
    219,NF1,hTERT,activation,,
    220,NF-kappaB,hTERT,activation,,
    221,AKT,hTERT,activation,,
    222,HIF1,hTERT,activation,,
    223,Myc/Max,hTERT,activation,,
    224,p53,hTERT,inhibition,,
    225,Smad/Miz-1,hTERT,inhibition,,
    226,eEF2,hTERT,inhibition,,
    227,HIF1,VEGF,activation,,
    228,Myc/Max,VEGF,activation,,
    229,E2F,E2F/CyclinE,activation,,
    230,CyclinE,E2F/CyclinE,activation,,
    231,cdh1,cdh1/UbcH10,activation,,
    232,UbcH10,cdh1/UbcH10,activation,,
    233,TNF-alpha,TAK1,activation,,
    234,NF-kappaB,GSH,activation,,
    235,Myc/Max,GSH,activation,,
    236,p21,GSH,activation,,
    237,beta-catenin,TCF,activation,,
    238,TAK1,TCF,inhibition,,
    239,Myc/Max,Miz-1,inhibition,,
    240,input,Gli,activation,,
    241,PDK1,p70,activation,,
    242,mTOR,p70,activation,,
    243,DNA_Damage,ATM/ATR,activation,,
    244,ATM/ATR,CHK1/2,activation,,
    245,ATM/ATR,DNA_Repair,activation,,
    246,p90,eEF2K,activation,,
    247,p70,eEF2K,activation,,
    248,eEF2K,eEF2,inhibition,,
    249,PTEN,p53/PTEN,activation,,
    250,p53,p53/PTEN,activation,,
    251,HIF1,LDHA,activation,,
    252,Myc/Max,LDHA,activation,,
    253,LDHA,Acid_Lactic,activation,,
    254,NF-kappaB,Snail,activation,,
    255,GSK-3,Snail,inhibition,,
    256,p53,Snail,inhibition,,
    257,Smad,Snail,activation,,
    ''')


    mydict = '''Acid_Lactic   S_AcidLactic
    AKT   S_AKT
    AMP/ATP   S_AMP_ATP
    AMPK  S_AMPK
    APC   S_APC
    Apoptosis     S_Apoptosis
    ATM/ATR   S_ATM_ATR
    BAD   S_BAD
    Bak   S_Bak
    BAX   S_BAX
    Bcl-2     S_Bcl_2
    Bcl-XL    S_Bcl_XL
    beta-catenin  S_beta_cat
    Caspase8  S_Caspase8
    Caspase9  S_Caspase9
    cdc20     S_cdc20
    cdh1  S_cdh1
    cdh1/UbcH10   S_cdh1_UbcH10
    CHK1/2    S_CHK1_2
    COX412    S_COX412
    CyclinA   S_CycA
    CyclinB   S_CycB
    CyclinD   S_CycD
    CyclinE   S_CycE
    Cytoc/APAF1   S_Cytoc_APAF1
    DNA_Damage    S_DnaDamage
    DNA_Repair    S_DNARepair
    Dsh   S_Dsh
    E2F   S_E_cadh
    E2F/CyclinE   S_E2F
    E-cadherin    S_E2F_CyclinE
    eEF2  S_eEF2
    eEF2K     S_eEF2K
    ERK   S_ERK
    FADD  S_FADD
    FosJun    S_FosJun
    FOXO  S_FOXO
    GFs   S_GFs
    Gli   S_Gli
    Glut-1    S_Glut_1
    GSH   S_GSH
    GSK-3     S_GSK_3
    GSK-3/APC     S_GSK_3_APC
    HIF1  S_HIF1
    hTERT     S_hTERT
    Hypoxia   S_Hypoxia
    IKK   S_IKK
    JNK   S_JNK
    LDHA  S_LDHA
    Max   S_Max
    Mdm2  S_Mdm2
    Miz-1     S_Miz_1
    mTOR  S_mTOR
    Mutagen   S_Mutagen
    MXI1  S_MXI1
    Myc   S_Myc
    Myc/Max   S_Myc_Max
    NF-kappaB     S_NF_kB
    NF1   S_NF1
    Nutrients     S_Nutrients
    p14ARF    S_p14
    p15   S_p15
    p21   S_p21
    p27   S_p27
    p53   S_p53
    p53/Mdm2  S_p53_Mdm2
    p53/PTEN  S_p53_PTEN
    p70   S_p70
    p90   S_p90
    PDK1  S_PDK1
    PHDs  S_PHDs
    PI3K  S_PI3K
    PIP3  S_PIP3
    PKC   S_PKC
    PTEN  S_PTEN
    RAF   S_RAF
    RAGS  S_RAGS
    Ras   S_Ras
    Rb    S_Rb
    RHEB  S_RHEB
    ROS   S_ROS
    RTK   S_RTK
    Slug  S_Slug
    Smad  S_Smad
    SmadE2F   S_SmadE2F
    Smad/Miz-1    S_SmadMiz_1
    Snail     S_Snail
    TAK1  S_TAK1
    TCF   S_TCF
    TGF-beta  S_TGFbeta
    TNF-alpha     S_TNFalpha
    TSC1/2    S_TSC1_TSC2
    UbcH10    S_UbcH10
    VEGF  S_VEGF
    VHL   S_VHL
    WNT   S_WNT
    '''

    outputfile = config['output']['e']

    dict_elm = mydict.split('\n')
    mydict2 = {}
    for elm in dict_elm:
        elm = elm.strip()
        if elm == '': continue
        words = elm.split()
        mydict2[words[0]] = words[1]

    mydict2['input'] = 'input'
    df0 = pd.read_csv('untracked_fumia_node_set.csv')
    df1 = pd.read_csv(fumia_2013_regulation_data, index_col='ID')

    df1['found_in_boolnet'] = False
    for link in df1.index:
        # 소스, 타겟이 모두 boolnet에 포함되어 있는 경우.
        if (df1.loc[link, 'Source'] in mydict2) and (df1.loc[link, 'Target'] in mydict2) :
            df1.loc[link, 'Source'] = mydict2[ df1.loc[link, 'Source'] ]
            df1.loc[link, 'Target'] = mydict2[ df1.loc[link, 'Target'] ]
            df1.loc[link, 'found_in_boolnet'] = True

    df2 = df1.loc[df1['found_in_boolnet'], ['Source', 'Target', 'Type']]
    df2.reset_index(inplace=True)
    df2 = df2[['Source','Target','Type']]
    df2.to_csv(outputfile, index=False)

    # set_trace()

def run_f(config=None, force=False):
    # run_c 에 대해서, APC 등의 변이를 추가한다.
    from itertools import combinations,product
    from copy import deepcopy

    outputfile = config['output']['f']
    if exists(outputfile) and force==False:
         return

    result_data = tab_s7.load_b()
    nodes = result_data['labels']
    input_nodes = config['parameters']['input_nodes']

    free_nodes = set(nodes) - set(input_nodes)
    free_nodes = list(set(free_nodes))

    free_nodes.remove('S_GSK_3_APC')
    free_nodes.remove('S_APC')

    combi1 = [c for c in combinations(free_nodes, 1)]
    combi2 = [c for c in combinations(free_nodes, 2)]
    combi3 = [c for c in combinations(free_nodes, 3)]

    combi = combi1 + combi2 + [()]

    # input condition의 combinations 를 생성한다.
    table = list(product([False, True], repeat=len(input_nodes)))

    config_list = []
    for k,inp in enumerate(table):
        progressbar.update(k, len(table))
        for com in combi:
            on_states = []
            off_states = ['S_GSK_3_APC', 'S_APC']
            off_states = off_states + [c for c in com]
            for i,t in enumerate(inp):
                # t - 각 입력조건을 의미
                if t :
                    # 입력이 true 인경우, on_states에 추가
                    on_states.append( input_nodes[i] )
                else:
                    # 입력이 false 인경우, off_states에 추가
                    off_states.append( input_nodes[i] )

            config1 = deepcopy(config)
            config1['parameters']['on_states'] = deepcopy(on_states)
            config1['parameters']['off_states'] = deepcopy(off_states)
            config_list.append(deepcopy(config1))

    with open(outputfile, 'w') as outfile:
        json.dump({'configs': config_list, 'num_configs': len(config_list)},
            outfile, indent=4)

def run_g(config=None, force=False):

    outputfile = config['output']['g']
    if exists(outputfile) and force==False:
         return

    data = json.load(open('untracked_Table_S7F-Input-combinations-APC.json','r'))

    import time
    from multiprocessing import Pool
    p = Pool(60)
    scanning_result = p.map(myengine, data['configs'])

    with open(outputfile, 'w') as fileout:
        json.dump({'scanning_results': scanning_result}, fileout, indent=1)
