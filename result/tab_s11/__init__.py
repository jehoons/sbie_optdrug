# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

__all__ = []

from os.path import join,dirname,exists
from os import makedirs
import pandas as pd
import json

def get_config():
    return config

def get_workdir():
    return join(dirname(__file__))

def get_savedir():
    savedir = join(dirname(__file__), 'untracked_output')
    if not exists(savedir):
        makedirs(savedir)

    return savedir

config = {
    'parameters': {
        },
    'input': {
        },
    'output': {
        # table 7 에서 input combination 데이터의 small version 추출하기
        'a': join(get_savedir(),'Table-S11A-Input-combinations-small.json'),
        # table 7 에서 scanning results 데이터의 small version 추출하기
        'b': join(get_savedir(),'Table-S11B-Scanning-results-small.json'),
        'c': join(get_savedir(),'Table-S11C-Attractors.csv'),
        }
    }
