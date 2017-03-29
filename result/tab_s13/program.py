# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from os.path import dirname,join
from termutil import progressbar
from pdb import set_trace

""" requirements """
inputfile_a = join(dirname(__file__), 'TABLE.SXX.INPUTDATA.CSV')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.SXX.OUTPUTDATA.CSV')

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

    with open(config['output']['a'], 'w') as fobj:
        fobj.write('hello')
