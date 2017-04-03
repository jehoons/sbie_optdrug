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
outputfile_a = join(dirname(__file__), 'TABLE.S13A_fumia_weighted_sum_network_logic')
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


def run(config=None,force=force): #network model

    #origin_logic = get_data(file_name = 'fumia_2013.xlsx')
    set_trace()
    x1 = x2 + x3 - 1
    x2 = x1 - x2 + 1
    x3 = x2 - 1
    input_node = [x1, x2, x3]

    for i in range(len(input_node))

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
