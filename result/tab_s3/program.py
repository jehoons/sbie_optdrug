import pickle 
from sbie_optdrug import filelist 
from ipdb import set_trace
import json
import pandas as pd 
from sbie_optdrug.dataset import ccle
from sbie_optdrug.util import progressbar
from os.path import dirname,join,exists

""" requirements """
# inputfile = join(dirname(__file__), 'logical_rule.txt')

""" results """
outputfile = join(dirname(__file__), 'TABLE.S3.LOGICAL-EQUATIONS.TXT')

config = {'input': None, 'output': outputfile}


def getconfig():

    return config


def run(config=None):
    
    pass 

