import json
from os.path import exists
from boolean3_addon import attr_cy, to_logic
from pdb import set_trace
from numpy.random import random
import itertools
import pytest 

from pdb import set_trace
from boolean3_addon import to_logic 
from os.path import exists,dirname
from sbie_optdrug.result_season2 import tab_s1
import pandas as pd 


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
    if len(seq) == 5: 
        for i,j in zip(seq, ['0010', '0011', '1011', '1010', '1110']):
            if i != j:
                return 'Q'
        else :
            return 'P'

    elif len(seq) == 8:
        for i,j in zip(seq, ['0011', '1011', '1010', '1110', '0010', '1010', '1110', '0010']):
            if i != j:
                return 'Q'
        else :
            return 'P'

    else: 
        return 'Q'


def attach_phenotype(result):
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
            result['simul_result']['attractors'][att]['phenotype_data'] = seq

        elif att_type == 'point':
            att_str = state_key[att_value]
            cycstatus = check_cyclin(state_key[att_value], lbls)
            State_Apoptosis = att_str[lbls.index('State_Apoptosis')]
            if State_Apoptosis == '1':
                result['simul_result']['attractors'][att]['phenotype'] = 'A'
            elif cycstatus == '0000': 
                result['simul_result']['attractors'][att]['phenotype'] = 'Q'
            else: 
                result['simul_result']['attractors'][att]['phenotype'] = 'Unknown'

    return result


def attractor_summary(data):
    # data
    A, P, Q, U = 0, 0, 0, 0

    for att in data['simul_result']['attractors']: 
        this_attr = data['simul_result']['attractors'][att]
        if this_attr['phenotype'] == 'A':
            A += this_attr['ratio'] 
        elif this_attr['phenotype'] == 'P':
            P += this_attr['ratio']
        elif this_attr['phenotype'] == 'Q':
            Q += this_attr['ratio']             
        else: 
            U += this_attr['ratio']                                     

    return A, P, Q, U


@pytest.mark.skip(reason='')
def test_1():    
    results = []    
    input_string = '00000'
    for i,s in enumerate(['State_Mutagen', 'State_GFs','State_Nutrients',
                            'State_TNFalpha','State_Hypoxia']):    
        template[s] = True if input_string[i] == '1' else False

    inputs = [ template ]

    for sim_input in inputs:
        on_states = [] 
        off_states = [] 
        for lbl in sim_input:
            if sim_input[lbl] == True: 
                on_states.append(lbl)
            else: 
                off_states.append(lbl)

        res = attr_cy.run(samples=1000, steps=60, debug=False, 
                            on_states=on_states, off_states=off_states)

        res = attach_phenotype({'input_condition':sim_input, 'simul_result': res})
        results.append(res)

    json.dump(results, open(file_test1, 'w'), indent=4)


@pytest.mark.skip(reason='')
def test_2():
    results = []    
    input_string = '11100'
    for i,s in enumerate(['State_Mutagen', 'State_GFs','State_Nutrients',
                            'State_TNFalpha','State_Hypoxia']):    
        template[s] = True if input_string[i] == '1' else False

    inputs = [ template ]

    for sim_input in inputs:
        on_states = [] 
        off_states = [] 
        for lbl in sim_input:
            if sim_input[lbl] == True: 
                on_states.append(lbl)
            else: 
                off_states.append(lbl)

        res = attr_cy.run(samples=1000, steps=60, debug=False, 
                            on_states=on_states, off_states=off_states)

        res = attach_phenotype({'input_condition':sim_input, 'simul_result': res})
        results.append(res)

    json.dump(results, open(file_test2, 'w'), indent=4)


# @pytest.mark.skip(reason='')
def test_all(force):
    if exists(file_b1) and force == False:
        return;

    inputs = [ {
        'State_Mutagen' : State_Mutagen, 
        'State_GFs': State_GFs,
        'State_Nutrients': State_Nutrients,
        'State_TNFalpha': State_TNFalpha,
        'State_Hypoxia': State_Hypoxia,
        'State_Gli': False,
        } for State_Mutagen,State_GFs,State_Nutrients,State_TNFalpha,State_Hypoxia \
            in itertools.product([False,True], repeat=5)]

    results = []
    
    from tqdm import tqdm 

    for sim_input in tqdm(inputs):
        on_states = [] 
        off_states = [] 
        for lbl in sim_input:
            if sim_input[lbl] == True: 
                on_states.append(lbl)
            else: 
                off_states.append(lbl)

        res = attr_cy.run(samples=10000, steps=60, debug=False, 
                            on_states=on_states, off_states=off_states)
        res = attach_phenotype({'input_condition':sim_input, 'simul_result': res})
        results.append(res)

    json.dump(results, open(file_b1, 'w'), indent=4)


# @pytest.mark.skip(reason='')
def test_summary_32results():
    with open(file_b1,'r') as fin:
        res32 = json.load(fin)

    df0 = pd.DataFrame([], columns=['input','phenotype','ratio'])
    inplabels = ['State_Mutagen', 'State_GFs','State_Nutrients', 'State_TNFalpha','State_Hypoxia']
    k = 0 
    for res in res32:
        res = attach_phenotype(res)
        inpcond = res['input_condition']        
        inputstring = "".join(["1" if inpcond[x] else "0" for x in inplabels])
        attrs = res['simul_result']['attractors']
        for att in attrs: 
            phenotype = attrs[att]['phenotype']
            ratio = attrs[att]['ratio']
            # fobj.write('%s,%s,%f\n'%(inputstring,phenotype,ratio))
            df0.loc[k] = {
                'input':inputstring,
                'phenotype':phenotype,
                'ratio': ratio
                }
            k += 1
                
    df0.groupby(['input','phenotype']).sum().to_csv(file_b2)


# input 
file_a2 = dirname(tab_s1.__file__) + '/a/a2-fumia-model-processed-weighted-sum.txt'

# output 
file_test1 = dirname(tab_s1.__file__) + '/b/update1-test1-simul-result-with-00000.json'
file_test2 = dirname(tab_s1.__file__) + '/b/update1-test2-simul-result-with-11100.json'
file_b1 = dirname(tab_s1.__file__) + '/b/update1-b1-simul-result-with-32-conditions.json'
file_b2 = dirname(tab_s1.__file__) + '/b/update1-b2-simul-result-table-summary.csv'

with open(file_a2, 'r') as fobj:
    lines = fobj.readlines()
    lines2 = [] 
    for lin in lines: 
        lin = lin.strip()
        if lin[0] == '#': 
            continue 
        right = lin.split('=')[1].strip()
        if right == 'input':            
            lines2.append( lin.split('=')[0].strip() + '=' + 'False') 
        else: 
            lines2.append(lin)

    modeltext = "\n".join(lines2)

attr_cy.build(modeltext, weighted_sum=True)
import pyximport; pyximport.install()
cycs = ['State_CycA','State_CycB','State_CycD','State_CycE']

template = {
    'State_Mutagen' : False,
    'State_GFs': False,
    'State_Nutrients': False,
    'State_TNFalpha': False,
    'State_Hypoxia': False,
    'State_Gli': False,
    }

