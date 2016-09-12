import json
import pickle
from os.path import dirname,join,exists
from sbie_optdrug import filelist
import pandas as pd
from ipdb import set_trace
from sbie_optdrug.dataset import ccle
from sbie_optdrug.util import progressbar
from sbie_optdrug.result import tab_s1
from sbie_optdrug.result import tab_s2

inputfile = join(dirname(tab_s2.__file__), 'TABLE.S2.NODE-NAME.CSV')
outputfile = join(dirname(tab_s1.__file__), 'TABLE.S1A.MUTCNA_CRC_NET.CSV')
outputfile1 = join(dirname(tab_s1.__file__), 'TABLE.S1B.THERAPY_CRC_NET.CSV')
outputfile2 = join(dirname(tab_s1.__file__), 'TABLE.S1C.NUM_MUTCNA.CSV')
outputfile3 = join(dirname(tab_s1.__file__), 'TABLE.S1D.NUM_DRUG.CSV')

config = {
    'input': inputfile,
    'output': outputfile,
    'output1': outputfile1,
    'output2': outputfile2,
    'output3': outputfile3,
    }

mutcna = ccle.mutcna()
therapy = ccle.therapy()
mutcna_col = mutcna.filter(regex='LARGE_INTESTINE')
therapy_col = therapy[therapy['CCLE Cell Line Name'].str.contains("LARGE_INTESTINE")]
gene = pd.read_csv(config['input'])
data_mutcna = pd.read_csv(config['output'])
data_therapy = pd.read_csv(config['output1'])
data_num_mutcna = pd.read_csv(config['output2'])
data_num_therapy = pd.read_csv(config['output3'])

# attr_data = json.load(open('output.json','rb'))
# attrs = attr_data['basin_of_attraction']
# fmap = attr_data['fingerprint_map']
# mapkeys = attr_data['fingerprint_map_keys']
# attr_info = attr_data['attractor_info']
# outputfile = 'output1.json'
# json.dump(res, open(outputfile, 'w'), indent=1)
# data_MUTCNA = pd.DataFrame([], columns=['Cell Line'] + ['CCLE Mut'] + ['CCLE CNV AMP'] + ['CCLE CNV DEL']+ ['Network Mut'] + ['Network CNV AMP'] + ['Network CNV DEL'])
# data_MUTCNA.loc[i, 'CCLE Mut'] = len(data_sub_MUT)
# data_net = data_sub.filter(regex=gene_index)
# gene_index = gene.loc[j, 'node_name']
# therapy_data = therapy[therapy['Compound'].str.contains(drug)]
# util.update_progress(i, len(therapy['Compound']))








# data_MUTCNA = pd.DataFrame([], columns=['Cell Line'] + ['CCLE Mut'] + ['CCLE CNV AMP'] + ['CCLE CNV DEL']+ ['Network Mut'] + ['Network CNV AMP'] + ['Network CNV DEL'])
# i = 0
# for i in range(len(mutcna_col.columns)):
#     util.update_progress(i, len(mutcna_col.columns))
#     data_MUTCNA.loc[i, 'Cell Line'] = mutcna_col.columns[i]
#     data = mutcna_col[mutcna_col.columns[i]]
#     data_sub = data[data == 1]
#     data_sub_MUT = data_sub.filter(regex='_MUT')
#     data_sub_AMP = data_sub.filter(regex='_AMP')
#     data_sub_DEL = data_sub.filter(regex='_DEL')
#     data_MUTCNA.loc[i, 'CCLE Mut'] = len(data_sub_MUT)
#     data_MUTCNA.loc[i, 'CCLE CNV AMP'] = len(data_sub_AMP)
#     data_MUTCNA.loc[i, 'CCLE CNV DEL'] = len(data_sub_DEL)
#     j = 0
#     for j in gene.index:
#         gene_index = gene.loc[j, 'node_name']
#         data_net = data_sub.filter(regex=gene_index)
#         data_net_MUT = data_net.filter(regex='_MUT')
#         data_net_AMP = data_net.filter(regex='_AMP')
#         data_net_DEL = data_net.filter(regex='_DEL')
#         if j == 0:
#             data_MUTCNA.loc[i, 'Network Mut'] = len(data_net_MUT)
#             data_MUTCNA.loc[i, 'Network CNV AMP'] = len(data_net_AMP)
#             data_MUTCNA.loc[i, 'Network CNV DEL'] = len(data_net_DEL)
#         else:
#             num_net_mut = data_MUTCNA.loc[i, 'Network Mut']
#             num_net_amp = data_MUTCNA.loc[i, 'Network CNV AMP']
#             num_net_del = data_MUTCNA.loc[i, 'Network CNV DEL']
#             data_MUTCNA.loc[i, 'Network Mut'] = num_net_mut + len(data_net_MUT)
#             data_MUTCNA.loc[i, 'Network CNV AMP'] = num_net_amp + len(data_net_AMP)
#             data_MUTCNA.loc[i, 'Network CNV DEL'] = num_net_del + len(data_net_DEL)
#         # if data_sub.index[j].find(gene_index) > -1:
#         #     if data.index[j].find(gene_index) < data.index[j].find('_'):
#         #         if data.index[j].find('_MUT') > -1:
#         #             if data.iloc[j] == 1:
#         #                 num_netmut += 1
#         #         if data.index[j].find('_AMP') > -1:
#         #             if data.iloc[j] == 1:
#         #                 num_netamp += 1
#         #         if data.index[j].find('_DEL') > -1:
#         #             if data.iloc[j] == 1:
#         #                 num_netdel += 1
#         j += 1
#     i += 1
# data_MUTCNA.to_csv('data_MUTCNA_temp1.csv', index=False)


#sampleinfo = ccle.sampleinfo()
#total_data.to_csv('total_data.csv')
# mutcna.to_csv('output_cnvcol.csv')
# iloc : number loc : string index mutcna.index(gene names)
# res = sampleinfo['Site Primary']=='large_intestine'
# res = sampleinfo[ sampleinfo['Site Primary']=='large_intestine' ]
# mutcna.columns
# pd.DataFrame(data) : list to dataframe

set_trace()

# data = ccle.

