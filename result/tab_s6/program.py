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

""" requirements """
inputfile_a = join(dirname(__file__), '..','tab_s2','TABLE.S2.NODE-NAME.CSV')
inputfile_b = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s1.json')
inputfile_c = join(dirname(__file__), '..','tab_s5','TABLE.S5A.COPYNUMVAR_data_s4.json')
inputfile_d = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s1.json')
inputfile_e = join(dirname(__file__), '..','tab_s5','TABLE.S5B.MUTATION_data_s4.json')
inputfile_f = join(dirname(__file__), '..','tab_s5','TABLE.S5C.DRUG_data.json')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S6A.COPYNUMVAR_data_s1.json')
outputfile_b = join(dirname(__file__), 'TABLE.S6A.COPYNUMVAR_data_s4.json')
outputfile_c = join(dirname(__file__), 'TABLE.S6B.MUTATION_data_s1.json')
outputfile_d = join(dirname(__file__), 'TABLE.S6B.MUTATION_data_s4.json')
outputfile_e = join(dirname(__file__), 'TABLE.S6C.DRUG_data.json')

config = {
    'program': 'template',
    'parameters': {
        'k1': 1,
        'k2': 2
    },
    'input': {
        'input_a': inputfile_a,
        'input_b': inputfile_b,
        'input_c': inputfile_c,
        'input_d': inputfile_d,
        'input_e': inputfile_e,
        'input_f': inputfile_f
        },
    'output': {
        'output_a': outputfile_a,
        'output_b': outputfile_b,
        'output_c': outputfile_c,
        'output_d': outputfile_d,
        'output_e': outputfile_e
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

    with open(config['output']['a'], 'w') as fobj:
        fobj.write('hello')
