from os.path import join,dirname
import pandas as pd 

__all__ = []

outputfilename = 'TABLE.S3.LOGICAL-EQUATIONS.TXT'

def load():     
    filename = join(dirname(__file__), outputfilename)
    return pd.read_csv(filename, names=['equation'])


