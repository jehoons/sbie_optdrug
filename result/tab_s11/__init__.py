# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

__all__ = []

from os.path import join,dirname,exists
import pandas as pd
import json

def get_config():
    return config 

def get_workdir():
    pass 

def get_savedir(): 
	savedir = join(dirname(__file__), 'untracked')
	if not exists(savedir): 
		os.makedirs(savedir)

	return savedir

# hallmark = {} 
# df_temp = pd.read_csv(HALLMARK_APOPTOSIS, skiprows=[1])
# hallmark['APOPTOSIS'] = df_temp[['HALLMARK_APOPTOSIS']].values.tolist()

# df_temp = pd.read_csv(HALLMARK_E2F_TARGETS, skiprows=[1])
# hallmark = df_temp[['HALLMARK_E2F_TARGETS']].values.tolist()

# df_temp = pd.read_csv(HALLMARK_G2M_CHECKPOINT, skiprows=[1])
# HALLMARK_APOPTOSIS = HALLMARK_APOPTOSIS[['HALLMARK_APOPTOSIS']].values.tolist()

# df_temp = pd.read_csv(HALLMARK_MITOTIC_SPINDLE, skiprows=[1])
# HALLMARK_APOPTOSIS = HALLMARK_APOPTOSIS[['HALLMARK_APOPTOSIS']].values.tolist()

# df_temp = pd.read_csv(HALLMARK_MYC_TARGETS_V1, skiprows=[1])
# HALLMARK_APOPTOSIS = HALLMARK_APOPTOSIS[['HALLMARK_APOPTOSIS']].values.tolist()

# df_temp = pd.read_csv(HALLMARK_MYC_TARGETS_V2, skiprows=[1])
# HALLMARK_APOPTOSIS = HALLMARK_APOPTOSIS[['HALLMARK_APOPTOSIS']].values.tolist()

# df_temp = pd.read_csv(HALLMARK_P53_PATHWAY, skiprows=[1])
# HALLMARK_APOPTOSIS = HALLMARK_APOPTOSIS[['HALLMARK_APOPTOSIS']].values.tolist()

# df_fumia = pd.read_csv(fumia_node_list, names=['fumia_node'])
# HALLMARK_APOPTOSIS = HALLMARK_APOPTOSIS[['HALLMARK_APOPTOSIS']].values.tolist()

config = {
    'parameters': {        

        },
    'tables': {
        'a': get_savedir() + '/Table-S11A-Fumia-nodes.txt', 
        'b': get_savedir() + '/MSigDB/HALLMARK_APOPTOSIS.txt'
		'c': get_savedir() + '/MSigDB/HALLMARK_E2F_TARGETS.txt'
		'd': get_savedir() + '/MSigDB/HALLMARK_G2M_CHECKPOINT.txt'
		'e': get_savedir() + '/MSigDB/HALLMARK_MITOTIC_SPINDLE.txt'
		'f': get_savedir() + '/MSigDB/HALLMARK_MYC_TARGETS_V1.txt'
		'g': get_savedir() + '/MSigDB/HALLMARK_MYC_TARGETS_V2.txt'
		'h': get_savedir() + '/MSigDB/HALLMARK_P53_PATHWAY.txt'	
    	}
    }

# # -*- coding: utf-8 -*-
# #*************************************************************************
# # Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# #
# # This file is part of {sbie_optdrug}.
# #*************************************************************************

# __all__ = []

# from os.path import join,dirname,exists
# from os import makedirs
# import pandas as pd
# import json

# def get_config():
#     return config

# def get_workdir():
#     return join(dirname(__file__))

# def get_savedir():
#     savedir = join(dirname(__file__), 'untracked_output')
#     if not exists(savedir):
#         makedirs(savedir)

#     return savedir

# config = {
#     'parameters': {
#         },
#     'input': {
#         },
#     'output': {
#         # table 7 에서 input combination 데이터의 small version 추출하기
#         'a': join(get_savedir(),'Table-S11A-Input-combinations-small.json'),
#         # table 7 에서 scanning results 데이터의 small version 추출하기
#         'b': join(get_savedir(),'Table-S11B-Scanning-results-small.json'),
#         'c': join(get_savedir(),'Table-S11C-Attractors.csv'),
#         }
#     }
