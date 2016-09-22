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

copy_number_data = open('copy_number_data.json', 'w')
mutation_data = open('mutation_data.json', 'w')
mutcna_index = data_mutcna['Description']
mutcna = data_mutcna[data_mutcna.columns[2:]]
mutcna.index = mutcna_index
mutcna_MUT = mutcna[mutcna.index.str.contains('_MUT')]
mutcna_AMP = mutcna[mutcna.index.str.contains('_AMP')]
mutcna_DEL = mutcna[mutcna.index.str.contains('_DEL')]

#mutcna_MUT = mutcna.filter(regex='_MUT')
#mutcna_AMP = mutcna.filter(regex='_AMP')
#mutcna_DEL = mutcna.filter(regex='_DEL')
i = 0
cnd = {}
mut = {}
for i in range(len(mutcna.columns)):
    progressbar.update(i, len(mutcna.columns))
    cln = mutcna.columns[i]
    if (len(cln) != 0) & (cln != 'Description'):
        cnd_add = {cln: {}}
        mut_add = {cln: {}}
        mutcna_MUT_cln = mutcna_MUT[cln]
        mutcna_AMP_cln = mutcna_AMP[cln]
        mutcna_DEL_cln = mutcna_DEL[cln]
        mutcna_MUT_cln_data = mutcna_MUT_cln[mutcna_MUT_cln==1]
        mutcna_AMP_cln_data = mutcna_AMP_cln[mutcna_AMP_cln==1]
        mutcna_DEL_cln_data = mutcna_DEL_cln[mutcna_DEL_cln==1]
        if len(cnd) == 0:
            cnd = cnd_add
            mut = mut_add
        else:
            cnd = dict(cnd.items() + cnd_add.items())
            mut = dict(mut.items() + mut_add.items())
        j = 0
        node_data_cnv = {}
        node_data_mut = {}
        for j in gene.index:
            name = gene.loc[j,'node_name']
            node_data_cnv_add = {name: {'function': ''}}
            node_data_mut_add = {name: {'function': ''}}
            if len(mutcna_MUT_cln_data) != 0:
                mutcna_MUT_cln_data_node = mutcna_MUT_cln_data[mutcna_MUT_cln_data.index.str.contains(name)]
                if len(mutcna_MUT_cln_data_node) != 0:
                    if len(node_data_mut) == 0:
                        node_data_mut_add[name]['function'] = 'MUT'
                        node_data_mut = node_data_mut_add
                    else:
                        node_data_mut_add[name]['function'] = 'MUT'
                        node_data_mut = dict(node_data_mut.items() + node_data_mut_add.items())

            if len(mutcna_AMP_cln_data) != 0:
                mutcna_AMP_cln_data_node = mutcna_AMP_cln_data[mutcna_AMP_cln_data.index.str.contains(name)]
                if len(mutcna_AMP_cln_data_node) != 0:
                    if len(node_data_cnv) == 0:
                        node_data_cnv_add[name]['function'] = 'AMP'
                        node_data_cnv = node_data_cnv_add
                    else:
                        node_data_cnv_add[name]['function'] = 'AMP'
                        node_data_cnv = dict(node_data_cnv.items() + node_data_cnv_add.items())

            if len(mutcna_DEL_cln_data) != 0:
                mutcna_DEL_cln_data_node = mutcna_DEL_cln_data[mutcna_DEL_cln_data.index.str.contains(name)]
                if len(mutcna_DEL_cln_data_node) != 0:
                    if len(node_data_cnv) == 0:
                        node_data_cnv_add[name]['function'] = 'DEL'
                        node_data_cnv = node_data_cnv_add
                    else:
                        node_data_cnv_add[name]['function'] = 'DEL'
                        node_data_cnv = dict(node_data_cnv.items() + node_data_cnv_add.items())
            j += 1
        cnd[cln] = node_data_cnv
        mut[cln] = node_data_mut
    i += 1

json.dump(cnd, copy_number_data, indent = 3, sort_keys = True)
json.dump(mut, mutation_data, indent = 3, sort_keys = True)
copy_number_data.close()
mutation_data.close()

#cnvdata = {cl1: {}, cl2: {}}
#name = gene.loc[0,'node_name']
#name1 = gene.loc[1,'node_name']
#cnvdata[cl1] = {name: {'function': "AMP", 'copy_number': 10}, name1: {'function': "DEL", 'copy_number': 2}}
#cnvdata[cl2] = {name: {'function': "AMP", 'copy_number': 10}, name1: {'function': "DEL", 'copy_number': 2}}

#name = {'function': "AMP", 'copy_number': 10}
#name1 = {'function': "DEL", 'copy_number': 2}

#c = json.dumps('gene.iloc[1]:{"function": "LOF", "intensity": 1.0}')


# outputfile = 'output1.json'
# json.dump(res, open(outputfile, 'w'), indent=1)
# attr_data = json.load(open('output.json','rb'))
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

