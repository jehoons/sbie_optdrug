import pickle
from ipdb import set_trace
import json
import pandas as pd
from os.path import dirname,join,exists
import sbie_optdrug
from sbie_optdrug.dataset import ccle,filelist
# from termutil import progressbar


# from sbie_optdrug.model.published import fumia_network

""" requirements """
# inputfile = join(dirname(__file__), 'logical_rule.txt')

""" results """

from sbie_optdrug.result import tab_s3

outputfile = tab_s3.outputfilename

config = {
    'output': {
            'a': outputfile
            }
        }


def getconfig():

    return config


def run(config=None):

    # do nothing
    # this is done by misc/rule2logic.py

    pass
