import pickle 
from pyhet import filelist 
from ipdb import set_trace
import json
import pandas as pd 
from pyhet.dataset import ccle
from pyhet import util

mutcna = ccle.mutcna()
therapy = ccle.therapy()
mutcna_col = mutcna.filter(regex='LARGE_INTESTINE')
therapy_col = therapy[therapy['CCLE Cell Line Name'].str.contains("LARGE_INTESTINE")]
gene = pd.read_csv('node_name.csv')
# model = open('logical_rule.txt',"r+")
# model.close()


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
#
# data_Drug = pd.DataFrame([], columns=['Drug']+['Target']+['Number of Cell line']+['Number of Large intestine']+['Target in network'])
# num = pd.DataFrame([],columns=['Number of data in each drug'])
# i = 0
# loc = 0
# for i in range(len(therapy['Compound'])):
#     util.update_progress(i, len(therapy['Compound']))
#     drug = therapy.loc[i,'Compound']
#     target = therapy.loc[i, 'Target']
#     j = 0
#     k = 0
#     num_LI = 0
#     if i == 0:
#         therapy_data = therapy[therapy['Compound'].str.contains(drug)]
#         data_CL = therapy_data['CCLE Cell Line Name']
#         data_Drug.loc[loc, 'Drug'] = drug
#         data_Drug.loc[loc, 'Target'] = target
#         for j in range(len(data_CL)):
#             if data_CL.iloc[j].find('LARGE_INTESTINE') > -1:
#                 num_LI += 1
#             j += 1
#         for k in gene.index:
#             gene_index = gene.loc[k, 'node_name']
#             if target.find(gene_index) > -1:
#                 data_Drug.loc[loc, 'target in network'] = gene_index
#         data_Drug.loc[loc, 'Number of Large intestine'] = num_LI
#         loc += 1
#     else:
#         if drug != therapy.loc[i-1, 'Compound']:
#             num.loc[loc-1, 'Number of data in each drug'] = i
#             therapy_data = therapy[therapy['Compound'].str.contains(drug)]
#             data_CL = therapy_data['CCLE Cell Line Name']
#             data_Drug.loc[loc, 'Drug'] = drug
#             data_Drug.loc[loc, 'Target'] = target
#             if loc == 1:
#                 data_Drug.loc[loc-1, 'Total Cell line number'] = i
#             else:
#                 data_Drug.loc[loc-1, 'Total Cell line number'] = i - num.loc[loc-2, 'Number of data in each drug']
#             for j in range(len(data_CL)):
#                 if data_CL.iloc[j].find('LARGE_INTESTINE') > -1:
#                     num_LI += 1
#                 j += 1
#             for k in gene.index:
#                 gene_index = gene.loc[k, 'node_name']
#                 if target.find(gene_index) > -1:
#                     data_Drug.loc[loc, 'target in network'] = gene_index
#             data_Drug.loc[loc, 'Number of Large intestine'] = num_LI
#             loc += 1
#     i += 1
# data_Drug.loc[loc-1, 'Total Cell line number'] = i - num.loc[loc-2, 'Number of data in each drug']
# data_Drug.to_csv('data_Drug.csv', index=False)
#
#
# # Count the number of drug and the data that have cell line name
# # with 'LARGE_INTESTINE' and same gene name with network
# data_Drug = pd.DataFrame([], columns=['Drug']+['Target']+['Total Cell line number']+['Number of Large intestine']+['Target in network'])
# num = pd.DataFrame([],columns=['Number of data in each drug'])
# i = 0
# loc = 0
# for i in range(len(therapy['Compound'])):
#     util.update_progress(i, len(therapy['Compound']))
#     drug = therapy.loc[i,'Compound']
#     target = therapy.loc[i, 'Target']
#     j = 0
#     k = 0
#     num_LI = 0
#     if i == 0:
#         therapy_data = therapy[therapy['Compound'].str.contains(drug)]
#         data_CL = therapy_data['CCLE Cell Line Name']
#         data_Drug.loc[loc, 'Drug'] = drug
#         data_Drug.loc[loc, 'Target'] = target
#         for j in range(len(data_CL)):
#             if data_CL.iloc[j].find('LARGE_INTESTINE') > -1:
#                 num_LI += 1
#             j += 1
#         for k in gene.index:
#             gene_index = gene.loc[k, 'node_name']
#             if target.find(gene_index) > -1:
#                 data_Drug.loc[loc, 'target in network'] = gene_index
#         data_Drug.loc[loc, 'Number of Large intestine'] = num_LI
#         loc += 1
#     else:
#         if drug != therapy.loc[i-1, 'Compound']:
#             num.loc[loc-1, 'Number of data in each drug'] = i
#             therapy_data = therapy[therapy['Compound'].str.contains(drug)]
#             data_CL = therapy_data['CCLE Cell Line Name']
#             data_Drug.loc[loc, 'Drug'] = drug
#             data_Drug.loc[loc, 'Target'] = target
#             if loc == 1:
#                 data_Drug.loc[loc-1, 'Total Cell line number'] = i
#             else:
#                 data_Drug.loc[loc-1, 'Total Cell line number'] = i - num.loc[loc-2, 'Number of data in each drug']
#             for j in range(len(data_CL)):
#                 if data_CL.iloc[j].find('LARGE_INTESTINE') > -1:
#                     num_LI += 1
#                 j += 1
#             for k in gene.index:
#                 gene_index = gene.loc[k, 'node_name']
#                 if target.find(gene_index) > -1:
#                     data_Drug.loc[loc, 'target in network'] = gene_index
#             data_Drug.loc[loc, 'Number of Large intestine'] = num_LI
#             loc += 1
#     i += 1
# data_Drug.loc[loc-1, 'Total Cell line number'] = i - num.loc[loc-2, 'Number of data in each drug']
# data_Drug.to_csv('data_Num_Drug.csv', index=False)

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

