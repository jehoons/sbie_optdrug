import pickle 
from sbie_optdrug import filelist 
from ipdb import set_trace
import json
import pandas as pd 
from sbie_optdrug.dataset import ccle
from sbie_optdrug.util import progressbar
from os.path import dirname,join,exists
from sbie_optdrug.model.published import fumia_network 


""" requirements """
# inputfile = join(dirname(__file__), 'logical_rule.txt')

""" results """
outputfile = join(dirname(__file__), 'TABLE.S3.LOGICAL-EQUATIONS.TXT')

config = {
    'program': 'Table S3', 
    'input': None, 
    'output': {
            'a': outputfile
            }
        }


def getconfig():

    return config


def run(config=None):
    
    res = fumia_network.to_logic(short=True)

    with open(config['output']['a'], 'w') as f: 
        f.write(res)

