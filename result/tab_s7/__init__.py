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

outputfile_a = join(dirname(__file__), 'TABLE.S7A.FUMIA_PROCESSED.csv')
outputfile_b = join(dirname(__file__), 'TABLE.S7B.ATTRACTORS.json')
outputfile_b_plot = join(dirname(__file__), 'TABLE.S7B.ATTRACTORS.png')

def load_a():
    df = pd.read_csv(outputfile_a, names=['equation'])
    
    return df

def load_b():
    with open(outputfile_b,'r') as f: 
        jsondata = json.load(f)    

    return jsondata

