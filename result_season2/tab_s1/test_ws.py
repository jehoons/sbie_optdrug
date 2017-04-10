import json
from os.path import exists
from boolean3_addon import attr_cy, to_logic
from pdb import set_trace
from numpy.random import random
import itertools
import pytest 

model = """
State_Mutagen=True
State_GFs=True
State_Nutrients=True
State_TNFalpha=True
State_Hypoxia=True
State_Gli=True
State_TGFbeta = Random
State_DnaDamage = Random
State_p53_Mdm2 = Random
State_AMP_ATP = Random
State_NF1 = Random
State_PKC = Random
State_RTK = Random
State_RAGS = Random
State_Ras = Random
State_PI3K = Random
State_PTEN = Random
State_PIP3 = Random
State_PDK1 = Random
State_IKK = Random
State_NFkappaB = Random
State_RAF = Random
State_ERK = Random
State_p90 = Random
State_AKT = Random
State_WNT = Random
State_Dsh = Random
State_APC = Random
State_GSK_3 = Random
State_GSK_3_APC = Random
State_beta_cat = Random
State_Slug = Random
State_mTOR = Random
State_HIF1 = Random
State_COX412 = Random
State_VHL = Random
State_PHDs = Random
State_Myc_Max = Random
State_Myc = Random
State_Max = Random
State_MXI1 = Random
State_TSC1_TSC2 = Random
State_RHEB = Random
State_p53 = Random
State_Bcl_2 = Random
State_BAX = Random
State_BAD = Random
State_Bcl_XL = Random
State_Rb = Random
State_E2F = Random
State_p14 = Random
State_CycA = Random
State_CycB = Random
State_CycD = Random
State_CycE = Random
State_cdh1 = Random
State_cdc20 = Random
State_UbcH10 = Random
State_p27 = Random
State_p21 = Random
State_Mdm2 = Random
State_Smad = Random
State_SmadMiz_1 = Random
State_SmadE2F = Random
State_p15 = Random
State_FADD = Random
State_Caspase8 = Random
State_Bak = Random
State_JNK = Random
State_FOXO = Random
State_FosJun = Random
State_ROS = Random
State_AMPK = Random
State_Cytoc_APAF1 = Random
State_Caspase9 = Random
State_Apoptosis = Random
State_E_cadh = Random
State_Glut_1 = Random
State_hTERT = Random
State_VEGF = Random
State_E2F_CyclinE = Random
State_cdh1_UbcH10 = Random
State_TAK1 = Random
State_GSH = Random
State_TCF = Random
State_Miz_1 = Random
State_p70 = Random
State_ATM_ATR = Random
State_CHK1_2 = Random
State_DNARepair = Random
State_eEF2K = Random
State_eEF2 = Random
State_p53_PTEN = Random
State_LDHA = Random
State_AcidLactic = Random
State_Snail = Random
State_Mutagen = State_Mutagen
State_GFs = State_GFs
State_Nutrients = State_Nutrients
State_TNFalpha = State_TNFalpha
State_Hypoxia = State_Hypoxia
State_Gli = State_Gli
State_TGFbeta *= sign(+State_HIF1)
State_DnaDamage *= sign(+State_Mutagen+State_ROS)
State_p53_Mdm2 *= sign(+State_p53+State_Mdm2-1)
State_AMP_ATP *= sign(-State_Nutrients+1)
State_NF1 *= sign(-State_PKC+1)
State_PKC *= sign(+State_RTK+State_WNT)
State_RTK *= sign(+State_GFs)
State_RAGS *= sign(+State_Nutrients-State_Hypoxia)
State_Ras *= sign(-State_NF1+State_RTK+1)
State_PI3K *= sign(+State_Ras+State_hTERT)
State_PTEN *= 1
State_PIP3 *= sign(+State_PI3K-State_PTEN-State_p53_PTEN+1)
State_PDK1 *= sign(+State_PIP3+State_HIF1+State_Myc_Max)
State_IKK *= sign(+State_PKC+State_AKT+State_mTOR-State_PHDs-State_p53+State_TAK1)
State_NFkappaB *= sign(+State_PIP3+2*State_IKK-State_E_cadh+State_Snail-1)
State_RAF *= sign(+State_PKC+State_Ras)
State_ERK *= sign(+State_RAF)
State_p90 *= sign(+State_PDK1+State_ERK)
State_AKT *= sign(+State_PIP3+State_PDK1-1)
State_WNT *= sign(-State_p53+State_Gli)
State_Dsh *= sign(+State_WNT)
State_APC *= sign(+State_PTEN+1)
State_GSK_3 *= sign(-State_p90-State_AKT-State_Dsh-State_mTOR+3)
State_GSK_3_APC *= sign(+State_APC+State_GSK_3-1)
State_beta_cat *= sign(-State_GSK_3_APC-State_p53+1)
State_Slug *= sign(-State_p53_Mdm2+State_NFkappaB+State_TCF)
State_mTOR *= sign(+State_RAGS+State_AKT+State_RHEB-State_AMPK-1)
State_HIF1 *= sign(+State_Hypoxia+State_mTOR-2*State_VHL-State_PHDs+State_Myc_Max-State_p53-State_FOXO+2)
State_COX412 *= sign(+State_HIF1)
State_VHL *= sign(-State_Hypoxia-State_ROS+1)
State_PHDs *= sign(-State_Hypoxia+State_ROS+1)
State_Myc_Max *= sign(-State_TGFbeta+State_Myc+State_Max-State_MXI1-State_SmadE2F-1)
State_Myc *= sign(+State_NFkappaB+State_ERK-State_HIF1+State_E2F+State_FosJun+State_TCF+State_Gli-1)
State_Max *= 1
State_MXI1 *= sign(+State_HIF1)
State_TSC1_TSC2 *= sign(-State_RAF-State_ERK-State_p90-State_AKT+State_HIF1+State_p53+State_AMPK+1)
State_RHEB *= sign(-State_TSC1_TSC2+1)
State_p53 *= sign(+State_HIF1-State_Bcl_2-State_Mdm2+State_CHK1_2+1)
State_Bcl_2 *= sign(+2*State_NFkappaB-State_p53-State_BAX-State_BAD)
State_BAX *= sign(-State_HIF1+State_p53-State_Bcl_2+State_JNK)
State_BAD *= sign(-State_RAF-State_p90-State_AKT-State_HIF1+1)
State_Bcl_XL *= sign(-State_p53-State_BAD+1)
State_Rb *= sign(-State_CycA-State_CycB-State_CycD-State_CycE-State_Mdm2+2)
State_E2F *= sign(-2*State_Rb-State_CycA-State_CycB+State_E2F+1)
State_p14 *= sign(+State_Ras+State_Myc_Max+State_E2F-3)
State_CycA *= sign(+State_CycA-State_Rb-State_cdc20-State_p27-State_p21+State_E2F_CyclinE+State_cdh1_UbcH10)
State_CycB *= sign(-State_p53-State_cdh1-State_cdc20-State_p27-State_p21+1)
State_CycD *= sign(+State_NFkappaB-2*State_GSK_3+State_Myc_Max-State_p27-State_p21-State_p15-State_FOXO+State_FosJun+State_TCF+State_Gli)
State_CycE *= sign(-State_Rb+State_E2F-State_CycA-State_p27-State_p21)
State_cdh1 *= sign(-State_CycA-State_CycB+State_cdc20+1)
State_cdc20 *= sign(+State_CycB-State_cdh1)
State_UbcH10 *= sign(+State_CycA+State_CycB-State_cdh1+State_cdc20+State_UbcH10)
State_p27 *= sign(-State_AKT+State_HIF1-State_Myc_Max-State_CycA-State_CycB-State_CycD+State_SmadMiz_1+1)
State_p21 *= sign(-State_AKT+State_HIF1-State_Myc_Max+State_p53+State_SmadMiz_1-State_hTERT+1)
State_Mdm2 *= sign(+State_AKT+State_p53-State_p14-State_ATM_ATR+1)
State_Smad *= sign(+State_TNFalpha+State_TGFbeta)
State_SmadMiz_1 *= sign(+State_Smad+State_Miz_1-1)
State_SmadE2F *= sign(+State_Smad)
State_p15 *= sign(+State_SmadMiz_1+State_Miz_1)
State_FADD *= sign(+State_TNFalpha)
State_Caspase8 *= sign(+State_FADD)
State_Bak *= sign(+State_Caspase8)
State_JNK *= sign(+State_TGFbeta)
State_FOXO *= sign(-State_AKT+2)
State_FosJun *= sign(+State_ERK+State_JNK)
State_ROS *= sign(-State_COX412-State_GSH)
State_AMPK *= sign(-State_GFs+State_AMP_ATP+State_HIF1+State_ATM_ATR+1)
State_Cytoc_APAF1 *= sign(-State_AKT+State_p53-State_Bcl_2+State_BAX-State_Bcl_XL+State_Caspase8+State_Bak)
State_Caspase9 *= sign(+State_Cytoc_APAF1)
State_Apoptosis *= sign(+State_Caspase8+State_Caspase9)
State_E_cadh *= sign(-State_NFkappaB-State_Slug-State_Snail+3)
State_Glut_1 *= sign(+State_AKT+State_HIF1+State_Myc_Max-1)
State_hTERT *= sign(+State_NF1+State_NFkappaB+State_AKT+State_HIF1+State_Myc_Max-State_p53-State_SmadMiz_1-State_eEF2-4)
State_VEGF *= sign(+State_HIF1+State_Myc_Max)
State_E2F_CyclinE *= sign(+State_E2F+State_CycE-1)
State_cdh1_UbcH10 *= sign(+State_cdh1+State_UbcH10-1)
State_TAK1 *= sign(+State_TNFalpha)
State_GSH *= sign(+State_NFkappaB+State_Myc_Max+State_p21)
State_TCF *= sign(+State_beta_cat-State_TAK1)
State_Miz_1 *= sign(-State_Myc_Max+1)
State_p70 *= sign(+State_PDK1+State_mTOR)
State_ATM_ATR *= sign(+State_DnaDamage)
State_CHK1_2 *= sign(+State_ATM_ATR)
State_DNARepair *= sign(+State_ATM_ATR)
State_eEF2K *= sign(+State_p90+State_p70)
State_eEF2 *= sign(-State_eEF2K+1)
State_p53_PTEN *= sign(+State_PTEN+State_p53-1)
State_LDHA *= sign(+State_HIF1+State_Myc_Max-1)
State_AcidLactic *= sign(+State_LDHA)
State_Snail *= sign(+State_NFkappaB-State_GSK_3-State_p53+State_Smad-1)
"""

def remove_dup(test_list):
    prev = '' 
    output_list = [] 
    for el in test_list:
        if el == prev: 
            continue 
        else: 
            output_list.append(el)
            prev = el 

    return output_list


def check_cyclin(a_state_in_cyc, lbls): 
    global cycs
    rr = [lbls.index(s) for s in cycs]
    res0 = [ a_state_in_cyc[si] for k,si in enumerate(rr)]
    return "".join(res0)


def check_cyclin_seq(att_value, state_key, lbls):
    global cycs
    cyc_att = [state_key[x] for x in att_value]
    cyc_seq = [] 
    for S in cyc_att: 
        res0 = check_cyclin(S,lbls)
        cyc_seq.append("".join(res0))

    rem = remove_dup(cyc_seq)

    return rem

def check_cyclic_phenotype(seq):
    if len(seq) != 5: 
        return 'Q'
    else: 
        for i,j in zip(seq, ['0010', '0011', '1011', '1010', '1110']):
            if i != j:
                return 'Q'
            
        return 'P'

def check_simul_result(result):

# from the paper: 
# Considering the effects of mutations, reported on the next subsection, 
# they include the following basic
# cell phenotypes: 
# apoptotic, characterized by active caspases;
# glycolytic, with H1f1 activated under normoxia; 
# immortalized in which hTert is active; 
# migratory, associated to inactivate Ecadherin;
# mutator, corresponding to inactive Atm/Atr proteins in the presence of DNA damage; 
# proliferative, in which cyclins are activated along the cell cycle in the correct sequence; 
# and quiescent, with cyclins inactive or activated in a wrong sequence.

# 위키를 살펴보면, 
# https://en.wikipedia.org/wiki/Cyclin
# D는 항상 켜져 있어야 하고, 
# E, A, B 순서로 켜져야 한다는 것을 알 수 있다.
    simul_result = result['simul_result']
    input_cond = result['input_condition']

    print('input:\n', input_cond)
    atts = simul_result['attractors']
    lbls = simul_result['labels']
    state_key = simul_result['state_key']

    for att in atts:            
        att_value = atts[att]['value']
        att_type = atts[att]['type']
        if att_type == 'cyclic':
            seq = check_cyclin_seq(att_value, state_key, lbls)
            result['simul_result']['attractors'][att]['phenotype'] = \
                check_cyclic_phenotype(seq)

        elif att_type == 'point':
            att_str = state_key[att_value]
            State_Apoptosis = att_str[lbls.index('State_Apoptosis')]
            # print('[point]')
            # print('apopt: ', State_Apoptosis)
            # print('cycstate: ', check_cyclin(att_str, lbls))
            result['simul_result']['attractors'][att]['phenotype'] = \
                    'A' if State_Apoptosis == '1' else 'Unknown'

    return result


def test_01100():

    results = []    
    
    input_string = '01100'
    # (carcinogens, growth factors, nutrient supply, growth suppressors, hypoxia)

    template = {
        'State_Mutagen' : False,
        'State_GFs': False,
        'State_Nutrients': False,
        'State_TNFalpha': False,
        'State_Hypoxia': False,
        'State_Gli': True,
        } 

    for i,s in enumerate(['State_Mutagen', 'State_GFs','State_Nutrients','State_TNFalpha','State_Hypoxia']):
        template[s] = True if input_string[i] == '1' else False

    # set_trace()

    inputs = [ template ]

    # inputs = [ {
    #     'State_Mutagen' : State_Mutagen, 
    #     'State_GFs': True,
    #     'State_Nutrients': True,
    #     'State_TNFalpha': State_TNFalpha,
    #     'State_Hypoxia': State_Hypoxia,
    #     'State_Gli': True,
    #     } for State_Mutagen,State_TNFalpha,State_Hypoxia in itertools.product([False,True], repeat=3)]

    for sim_input in inputs:
        on_states = [] 
        off_states = [] 
        # print (sim_input)
        for lbl in sim_input:
            if sim_input[lbl] == True: 
                on_states.append(lbl)
            else: 
                off_states.append(lbl)

        res = attr_cy.run(samples=1000, steps=50, debug=False, on_states=on_states,
            off_states=off_states)
        # print(repr(res))
        results.append({'input_condition':sim_input, 'simul_result': res})

    json.dump(results, open('fumia_simul_ws.json', 'w'), indent=4)

    results[0] = check_simul_result(results[0])

    # check
    P = 0.0 
    for att in results[0]['simul_result']['attractors']: 
        this_attr = results[0]['simul_result']['attractors'][att]
        if this_attr['phenotype'] == 'P':
            P += this_attr['ratio'] 

    assert P == 1.0


cycs = ['State_CycA','State_CycB','State_CycD','State_CycE']

model = model.strip()
attr_cy.build(model, weighted_sum=True)
import pyximport; pyximport.install()

