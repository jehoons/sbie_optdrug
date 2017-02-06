# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.jehoon@gmail.com>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import numpy
from os.path import exists
from sbie_optdrug.result.tab_s10 import program
from sbie_optdrug.result import tab_s7 
from ipdb import set_trace
import json

def search(inputpattern, testdata): 
    for node in inputpattern:
        value = inputpattern[node]
        search_result = True
        if value == True:
            if node in testdata['parameters']['on_states']:
                continue 
            else: 
                search_result = False
                break 
        else:
            if node in testdata['parameters']['off_states']:
                continue 
            else: 
                search_result = False
                break

    return search_result

s7conf = tab_s7.get_config()
table_s7f = json.load(open(s7conf['output']['f'], 'r'))

# 주어진 table-s7f에 대해서 inputpattern에 매칭하는 결과를 찾는다.

inputpattern = {'S_Mutagen': True, 
    'S_GFs': True, 
    'S_Nutrients': False, 
    'S_TNFalpha': False, 
    'S_Hypoxia': False
    }

for testdata in table_s7f['configs']:
    # testdata = table_s7f['configs'][record]
    res = search(inputpattern, testdata)
    if res:
        print(res)

set_trace()