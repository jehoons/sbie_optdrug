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

def get_config():
    return config 

def get_workdir():
    pass 

def get_savedir(): 
    pass 

config = {
    'parameters': {        
        },
    'Table': {
        'A': get_savedir() + '/Table-S11A-Fumia-nodes.txt'
    }
