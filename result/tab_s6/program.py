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

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S6A.json')


config = {
    'program': 'template',
    'parameters': {
        'k1': 1,
        'k2': 2
    },
    'input': {

        },
    'output': {

        }
    }


def getconfig():

    return config


def run(config=None):

    with open(config['output']['a'], 'w') as fobj:
        fobj.write('hello')
