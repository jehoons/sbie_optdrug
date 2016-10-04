# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from os.path import dirname,join
from util import progressbar
from pdb import set_trace

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

""" requirements """
inputfile_a = join(dirname(__file__), 'TABLE.SXX.INPUTDATA.CSV')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.SXX.OUTPUTDATA.CSV')

config = {
    'program': 'template', 
    'parameters': {
        'k1': 1, 
        'k2': 2
        }, 
    'input': {
        'a': inputfile_a
        }, 
    'output': {
        'a': outputfile_a
        }
    }


def getconfig():

    return config


def run(config=None):

    with open(config['output']['a'], 'w') as fobj:
        fobj.write('hello')

