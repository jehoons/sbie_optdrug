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
        'input_g': inputfile_g
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

    set_trace()


    def rule_mutation(state, name, value, clname, listname, p):
        """ rule_mutation defines how mutation is appied into simulation. """
        if name in listname[clname]:
            given_function = listname[clname][name]['function']
            intensity = listname[clname][name]['intensity']
            #if given_function == 'GOFLOF':
            #    given_function = mutations['default_function']
            if given_function == 'LOF':
                if value == True:
                    if random.random() < intensity:
                        value = False
            elif given_function == 'GOF':
                if value == False:
                    if random.random() < intensity:
                        value = True
        return value

    def rule_drug(state, name, value, clname, listname, p):
        if name in listname[clname]:
            target = listname[clname]
            given_function = listname[clname][name]['function']
            intensity = listname[clname][name]['intensity']
            #if given_function == 'GOFLOF':
            #    given_function = mutations['default_function']
            if given_function == 'LOF':
                if value == True:
                    if random.random() < intensity:
                        value = False
            elif given_function == 'GOF':
                if value == False:
                    if random.random() < intensity:
                        value = True
        return value

    def set_value2(state, name, src_value, clname, listname, p):
        "Custom value setter"
        dst_value1 = rule_mutation(state, name, src_value, clname, listname, p)
        dst_value2 = rule_drug(state, name, src_value, clname, listname, p)
        # Here, problem occurs if rule_mutation() and rule_drug() does not give
        # same changes (src_value->dst_value1, src_value->dst_value2).
        # This problem can be ignored if we ignore the case that src_value =
        # dst_value. We consider src == dst as no effect.
        if dst_value1 == dst_value2:
            dst_value = dst_value1
        else:
            if src_value == dst_value1:
                dst_value = dst_value2
            elif src_value == dst_value2:
                dst_value = dst_value1
        # finally, we decided dst_value and then we set the attribute.
        setattr(state, name, dst_value)
        return dst_value

    print(0)




    set_trace()

    #with open(config['output']['a'], 'w') as fobj:
        #fobj.write('hello')
