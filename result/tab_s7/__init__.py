__all__ = []

from os.path import join,dirname
import pandas as pd 

# """ requirements """
# inputfile_a = join(dirname(__file__), 'TABLE.SXX.INPUTDATA.CSV')

# """ results """
# outputfile_a = join(dirname(__file__), 'TABLE.SXX.OUTPUTDATA.CSV')

outputfile_a = join(dirname(__file__), 'TABLE.S7A.FUMIA_PROCESSED.csv')
outputfile_b = join(dirname(__file__), 'TABLE.S7B.ATTRACTORS.json')

def load_a():
    df = pd.read_csv(outputfile_a, names=['equation'])
    
    return df

def load_b():
    with open(outputfile_b,'r') as f: 
        jsondata = json.load(f)    

    return jsondata

