import json
import pickle
from os.path import dirname,join,exists
from sbie_optdrug import filelist
import pandas as pd
from ipdb import set_trace
from sbie_optdrug.dataset import ccle
from sbie_optdrug.result import tab_s1
from sbie_optdrug.result import tab_s2
from sbie_optdrug.result import tab_s5

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sbie_optdrug import boolean2
from sbie_optdrug.boolean2 import util
from sbie_optdrug.util import progressbar
import random

inputfile = join(dirname(tab_s2.__file__), 'TABLE.S2.NODE-NAME.CSV')
outputfile = join(dirname(tab_s1.__file__), 'TABLE.S1A.MUTCNA_CRC_NET.CSV')
outputfile1 = join(dirname(tab_s1.__file__), 'TABLE.S1B.THERAPY_CRC_NET.CSV')
outputfile2 = join(dirname(tab_s1.__file__), 'TABLE.S1C.NUM_MUTCNA.CSV')
outputfile3 = join(dirname(tab_s1.__file__), 'TABLE.S1D.NUM_DRUG.CSV')
#outputfile4 = join(dirname(tab_s5.__file__), 'TABLE.S5A.COPYNUMVAR_data.json')
#outputfile5 = join(dirname(tab_s5.__file__), 'TABLE.S5B.MUTATION_data.json')
#outputfile6 = join(dirname(tab_s5.__file__), 'TABLE.S5C.DRUG_data.json')

config = {
    'input': inputfile,
    'output': outputfile,
    'output1': outputfile1,
    'output2': outputfile2,
    'output3': outputfile3,
    #'output4': outputfile4,
    #'output5': outputfile5,
    #'output6': outputfile6,
    }

ccle_mutcna = ccle.mutcna()
ccle_therapy = ccle.therapy()
mutcna_col = ccle_mutcna.filter(regex='LARGE_INTESTINE')
ccle_therapy_col = ccle_therapy[ccle_therapy['CCLE Cell Line Name'].str.contains("LARGE_INTESTINE")]

gene = pd.read_csv(config['input'])
data_mutcna = pd.read_csv(config['output'])
data_therapy = pd.read_csv(config['output1'])
data_num_mutcna = pd.read_csv(config['output2'])
data_num_drug = pd.read_csv(config['output3'])
#cnv_data = json.load(open(config['output4']),'rb')
#mutation_data = json.load(open(config['output5']),'rb')
#drug_data = json.load(open(config['output6']),'rb')



#cln=data_mutcna.columns[2]
#data_cln = cnv_data[cln]
# attrs = attr_data['basin_of_attraction']
# fmap = attr_data['fingerprint_map']
# mapkeys = attr_data['fingerprint_map_keys']
# attr_info = attr_data['attractor_info']
# data_MUTCNA = pd.DataFrame([], columns=['Cell Line'] + ['CCLE Mut'] + ['CCLE CNV AMP'] + ['CCLE CNV DEL']+ ['Network Mut'] + ['Network CNV AMP'] + ['Network CNV DEL'])
# data_MUTCNA.loc[i, 'CCLE Mut'] = len(data_sub_MUT)
# data_net = data_sub.filter(regex=gene_index)
# gene_index = gene.loc[j, 'node_name']
# therapy_data = therapy[therapy['Compound'].str.contains(drug)]
# util.update_progress(i, len(therapy['Compound']))
#sampleinfo = ccle.sampleinfo()
#total_data.to_csv('total_data.csv')
# mutcna.to_csv('output_cnvcol.csv')
# iloc : number loc : string index mutcna.index(gene names)
# res = sampleinfo['Site Primary']=='large_intestine'
# res = sampleinfo[ sampleinfo['Site Primary']=='large_intestine' ]
# mutcna.columns
# pd.DataFrame(data) : list to dataframe

set_trace()

