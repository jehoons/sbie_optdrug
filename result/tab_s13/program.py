# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from os.path import dirname,join
#from termutil import progressbar
from pdb import set_trace
import pyexcel

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


def run(config=None):

    origin_logic = pyexcel.get_array(file_name = config['input']['input_a'])
    #copy_number_data_s1 = json.load(open(config['input']['input_b'], 'rb'))
    #copy_number_data_s4 = json.load(open(config['input']['input_c'], 'rb'))
    #mutation_data_s1 = json.load(open(config['input']['input_d'], 'rb'))
    #mutation_data_s4 = json.load(open(config['input']['input_e'], 'rb'))
    #drug_data = json.load(open(config['input']['input_f'], 'rb'))
    #equation = pd.read_csv(config['input']['input_g'])
    #input_condi = json.load(open(config['input']['input_h'], 'rb'))
    #attractor_result = json.load(open(config['input']['input_i'], 'rb'))

    # get the node & logic and make node = logic file
    # resolve current state -> next state, and attractor
    # state sampling

    set_trace()
