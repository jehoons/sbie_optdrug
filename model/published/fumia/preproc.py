# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from os.path import dirname, join, exists
import re 
from pdb import set_trace

def preproc():

    inputfile = join(dirname(__file__), 'fumia_network.txt')

    with open(inputfile, 'r') as f: 
        txtdata = f.readlines()

    txtdata = re.sub('%.*\n', '\n', "\n".join(txtdata))
    txtdata = re.sub('[ ;]', '', txtdata)
    txtdata = txtdata.replace('(t)', '')
    txtdata = txtdata.replace('(t+1)', '')

    txtdataArr = txtdata.split('\n')

    txtdataArr2 = [] 
    for line in txtdataArr: 
        if line != '': 
            txtdataArr2.append(line)

    print("\n".join(txtdataArr2))


if __name__ == '__main__':

    preproc() 

