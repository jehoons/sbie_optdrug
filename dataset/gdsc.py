# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {pyhet}.
#*************************************************************************

import pickle
from sbie_optdrug.dataset import filelist
import json
import pandas as pd

import ipdb

import ascii 

rawfiles = filelist.gdsc_v50['raw']

# print rawfiles.keys()

df = pd.read_csv( rawfiles['gdsc_manova_output_w5'] )

ipdb.set_trace()
