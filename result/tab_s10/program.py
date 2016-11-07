# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import json
import pickle
from os.path import dirname,join
from sbie_optdrug.dataset import filelist
import pandas as pd
from ipdb import set_trace
import sbie_optdrug
from sbie_optdrug.dataset import ccle
from termutil import progressbar

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#from sbie_optdrug import boolean2
import random

from boolean3_addon import attr_cy
import numpy as np

from boolean3 import Model
from boolean3_addon import attractor

""" requirements """
inputfile_a = join(dirname(__file__), '..','tab_s2','TABLE.S2.NODE-NAME.CSV')
inputfile_b = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s1.json')
inputfile_c = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s4.json')
inputfile_d = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s1.json')
inputfile_e = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s4.json')
inputfile_f = join(dirname(__file__), '..','tab_s5','TABLE.S5C.DRUG_data.json')
inputfile_g = join(dirname(__file__), '..','tab_s7','TABLE_S7A_FUMIA_PROCESSED.csv')
inputfile_h = join(dirname(__file__), '..','tab_s7','TABLE_S7C_INPUT_COMBINATIONS.json')
inputfile_i = join(dirname(__file__), '..','tab_s7','TABLE_S7D_SCANNING_RESULT.json')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE_S8A_aaa.csv')
#outputfile_b = join(dirname(__file__), 'TABLE.S8A.COPYNUMVAR_data_s4.json')
#outputfile_c = join(dirname(__file__), 'TABLE.S8B.MUTATION_data_s1.json')
#outputfile_d = join(dirname(__file__), 'TABLE.S8B.MUTATION_data_s4.json')
#outputfile_e = join(dirname(__file__), 'TABLE.S8C.DRUG_data.json')

config = {
    'program': 'template',
    'input': {
        'input_a': inputfile_a,
        'input_b': inputfile_b,
        'input_c': inputfile_c,
        'input_d': inputfile_d,
        'input_e': inputfile_e,
        'input_f': inputfile_f,
        'input_g': inputfile_g,
        'input_h': inputfile_h,
        'input_i': inputfile_i
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

    gene = pd.read_csv(config['input']['input_a'])
    copy_number_data_s1 = json.load(open(config['input']['input_b'], 'rb'))
    copy_number_data_s4 = json.load(open(config['input']['input_c'], 'rb'))
    mutation_data_s1 = json.load(open(config['input']['input_d'], 'rb'))
    mutation_data_s4 = json.load(open(config['input']['input_e'], 'rb'))
    drug_data = json.load(open(config['input']['input_f'], 'rb'))
    equation = pd.read_csv(config['input']['input_g'])
    input_condi = json.load(open(config['input']['input_h'], 'rb'))
    attractor_result = json.load(open(config['input']['input_i'], 'rb'))

    set_trace()




    print(0)


    #with open(config['output']['a'], 'w') as fobj:
        #fobj.write('hello')
