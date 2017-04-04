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
#from pyexcel-xlsx import get_data
#from termutil import progressbar

""" requirements """
inputfile_a = join(dirname(__file__), '..','tab_s13','fumia_2013.xlsx')
#inputfile_b = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s1.json')
#inputfile_c = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s4.json')
#inputfile_d = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s1.json')
#inputfile_e = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s4.json')
#inputfile_f = join(dirname(__file__), '..','tab_s5','TABLE.S5C.DRUG_data.json')
#inputfile_g = join(dirname(__file__), '..','tab_s7','untracked_Table_S7A_Fumia-processed.csv')
#inputfile_h = join(dirname(__file__), '..','tab_s7','untracked_Table_S7F-Input-combinations-APC.json')
#inputfile_i = join(dirname(__file__), '..','tab_s7','untracked_Table_S7G-Scanning-results-APC.json')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S13A.Toy_model.json')
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

def run(config=None): #network model

    #origin_logic = get_data(file_name = 'fumia_2013.xlsx')
    #attractor_result = open(config['output']['output_a'], 'w')
    steps = 10
    x1 = x2 = x3 = 0
    input_nodes = [x1, x2, x3]
    table = list(product([0, 1], repeat=len(input_nodes)))
    att_result = {}
    check_cyclic = 0
    for i in range(len(table)):
        x1 = table[i][0]
        x2 = table[i][1]
        x3 = table[i][2]
        curr_state = [x1,x2,x3]
        trajectory = [curr_state]
        check_cyclic = 0
        for j in range(steps):
            print(curr_state)
            x1 = sgn(curr_state[1] + curr_state[2] - 1)
            x2 = sgn(curr_state[0] - curr_state[1] + 1)
            x3 = sgn(curr_state[1])
            next_state = [x1, x2, x3]
            print('->')
            print(next_state)
            if cmp(curr_state,next_state) == 0:
                att = {i: {'input': table[i], 'attractor': next_state, 'type': 'point'}}
                if len(att_result) == 0:
                    print('a')
                    att_result = att
                else:
                    att_result = dict(att_result.items() + att.items())
                    print('b')
                break
            elif cmp(curr_state,next_state) != 0:
                if len(trajectory) == 1:
                    trajectory.append(next_state)
                    print('c')
                elif len(trajectory) > 1:
                    for k in range(len(trajectory)):
                        if cmp(next_state,trajectory[k]) == 0:
                            check_cyclic = 1
                            att = {i: {'input': table[i], 'attractor': trajectory[k:len(trajectory)], 'type': 'cyclic'}}
                            if len(att_result) == 0:
                                att_result = att
                                print('d')
                            else:
                                att_result = dict(att_result.items() + att.items())
                                print('e')
                    trajectory.append(next_state)
            print(check_cyclic)
            if check_cyclic == 1:
                print('f')
                break
            curr_state = [x1, x2, x3]
            j += 1
        print('---')
        i += 1
    set_trace()
    #json.dump(att_result, attractor_result, indent=3, sort_keys=True)
    #attractor_result.close()


    # get the node & logic and make node = logic file
    # resolve current state -> next state, and attractor
    # state sampling

    #set_trace()

#def run_b(config=None): #get attractor

    #traj = []
    #for i in range(1000 # step)
        #traj(t) = network model result
        #if traj(t) = before one
            #point attractor
        #else
            #cyclic attractor

    #set_trace()

#def run_c(config=None): #get phenotype

    #att = []
    #for i in range(att)
        #att(i) ->

    #set_trace()
