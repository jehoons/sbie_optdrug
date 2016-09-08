# -*- coding: utf-8 -*-
#!/usr/bin/python 
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
# 
# This file is part of {pyhet}.
#*************************************************************************

# import pickle 
# from sbie_optdrug import filelist 
from pdb import set_trace
# import json
# import pandas as pd 
from sbie_optdrug.dataset import ccle


def test_ccle():
    
    ccle.check_intestine_cells()
    # 실행결과 - experiments: 535, cell: 63, drugs: 24
    
    data = ccle.mutcna()

    # set_trace()

    assert True

