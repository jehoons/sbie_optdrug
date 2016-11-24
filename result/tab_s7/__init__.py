# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

__all__ = []

from os.path import join,dirname
import pandas as pd
import json

# """ requirements """
# inputfile_a = join(dirname(__file__), 'TABLE.SXX.INPUTDATA.CSV')

# """ results """
# outputfile_a = join(dirname(__file__), 'TABLE.SXX.OUTPUTDATA.CSV')

# fumia simulation model - boolean network
OUTFILE_A = join(dirname(__file__), 'untracked_Table_S7A_Fumia-processed.csv')
OUTFILE_B = join(dirname(__file__), 'untracked_Table_S7B-Attractors.json')
OUTFILE_B_PLOT = join(dirname(__file__), 'untracked_Table_S7B-Attractors.png')
OUTFILE_C = join(dirname(__file__), 'untracked_Table_S7C-Input-combinations.json')
OUTFILE_D = join(dirname(__file__), 'untracked_Table_S7D-Scanning-results.json')
# fumia simulation model - for visualizing regulation network 
OUTFILE_E = join(dirname(__file__), 'untracked_Table_S7E_Fumia-regulation-network.csv')

config = {
    'parameters': {
        'samples': 10000,
        'steps': 30,
        'on_states': [],
        'off_states': [],
        'input_nodes': ['S_Mutagen', 'S_GFs', 'S_Nutrients', 'S_TNFalpha', 'S_Hypoxia']
        },
    'input': {
        # 'a': inputfile_a
        },
    'output': {
        'a': OUTFILE_A,
        'b': OUTFILE_B,
        'b_plot': OUTFILE_B_PLOT,
        'c': OUTFILE_C,
        'd': OUTFILE_D,
        'e': OUTFILE_E
        }
    }

def load_a():
    df = pd.read_csv(OUTFILE_A, names=['equation'])

    return df


def load_b():
    with open(OUTFILE_B,'r') as f:
        jsondata = json.load(f)

    return jsondata


def load_c():
    with open(OUTFILE_C,'r') as f:
        jsondata = json.load(f)

    return jsondata


def load_d():
    with open(OUTFILE_D,'r') as f:
        jsondata = json.load(f)

    return jsondata
