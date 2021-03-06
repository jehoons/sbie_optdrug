import pickle 
from pyhet import filelist 
from ipdb import set_trace
import json
import pandas as pd 
from pyhet.dataset import ccle
from pyhet import util

# Bring data from filelist
mutcna = ccle.mutcna()
therapy = ccle.therapy()
mutcna_col = mutcna.filter(regex='LARGE_INTESTINE')
therapy_col = therapy[therapy['CCLE Cell Line Name'].str.contains("LARGE_INTESTINE")]
gene = pd.read_csv('node_name.csv')

# Select data that has 'LARGE INTESTINE' and same gene name with network
i = 0
for i in gene.index:
    util.update_progress(i, gene.shape[0])
    gene_index = gene.loc[i,'node_name']
    data_mut = mutcna_col[mutcna_col.index.str.contains(gene_index)]
    data_therapy = therapy_col[therapy_col['Target'].str.contains(gene_index)]
    if i == 0:
        total_mut = data_mut
        total_therapy = data_therapy
    else:
        if gene_index == 'AMP':
            j = 0
            for j in range(len(data_mut.index)):
                gene_name = data_mut.index[j]
                if gene_name.find(gene_index) < gene_name.find('_'):
                    temp = data_mut.ix[[j], :]
                    if j == 0:
                        data_mut_cor = temp
                    else:
                        data_mut_cor = data_mut_cor.append(temp)
                j += 1
            data_mut = data_mut_cor
        total_mut = pd.concat([total_mut, data_mut])
        total_therapy = pd.concat([total_therapy, data_therapy])
    i += 1
total_mut.to_csv('MUTCNA_CRC_NET.csv')
total_therapy.to_csv('therapy_CRC_NET.csv', index=False)

# Count the number of Mutation, amplification, deletion gene
# and the number of gene that correspond with network
data_MUTCNA = pd.DataFrame([], columns=['Cell Line'] + ['CCLE Mut'] + ['CCLE CNV AMP'] + ['CCLE CNV DEL']+
                                       ['Network Mut'] + ['Network CNV AMP'] + ['Network CNV DEL'] +
                                       ['Ratio of Mut'] + ['Ratio of CNV AMP'] + ['Ratio of CNV DEL'])
i = 0
for i in range(len(mutcna_col.columns)):
    util.update_progress(i, len(mutcna_col.columns))
    data_MUTCNA.loc[i, 'Cell Line'] = mutcna_col.columns[i]
    data = mutcna_col[mutcna_col.columns[i]]
    data_sub = data[data == 1]
    data_sub_MUT = data_sub.filter(regex='_MUT')
    data_sub_AMP = data_sub.filter(regex='_AMP')
    data_sub_DEL = data_sub.filter(regex='_DEL')
    data_MUTCNA.loc[i, 'CCLE Mut'] = len(data_sub_MUT)
    data_MUTCNA.loc[i, 'CCLE CNV AMP'] = len(data_sub_AMP)
    data_MUTCNA.loc[i, 'CCLE CNV DEL'] = len(data_sub_DEL)
    j = 0
    for j in gene.index:
        gene_index = gene.loc[j, 'node_name']
        data_net = data_sub.filter(regex=gene_index)
        data_net_AMP = data_sub_AMP.filter(regex=gene_index)
        data_net_MUT = data_sub_MUT.filter(regex=gene_index)
        data_net_DEL = data_sub_DEL.filter(regex=gene_index)
        if gene_index == 'AMP':
            k = 0
            data_net_sub = []
            for k in range(len(data_sub_AMP.index)):
                gene_name = data_sub_AMP.index[k]
                if gene_name.find(gene_index) < gene_name.find('_'):
                    temp = data_sub_AMP[data_sub_AMP.index.str.contains(gene_name)]
                    if len(data_net_sub) == 0:
                        data_net_sub = temp
                    else:
                        data_net_sub = pd.concat([data_net_sub, temp])
                k += 1
            data_net_AMP = data_net_sub

        if j == 0:
            data_MUTCNA.loc[i, 'Network Mut'] = len(data_net_MUT)
            data_MUTCNA.loc[i, 'Network CNV AMP'] = len(data_net_AMP)
            data_MUTCNA.loc[i, 'Network CNV DEL'] = len(data_net_DEL)
        elif j != 0 :
            num_net_mut = data_MUTCNA.loc[i, 'Network Mut']
            num_net_amp = data_MUTCNA.loc[i, 'Network CNV AMP']
            num_net_del = data_MUTCNA.loc[i, 'Network CNV DEL']
            data_MUTCNA.loc[i, 'Network Mut'] = num_net_mut + len(data_net_MUT)
            data_MUTCNA.loc[i, 'Network CNV AMP'] = num_net_amp + len(data_net_AMP)
            data_MUTCNA.loc[i, 'Network CNV DEL'] = num_net_del + len(data_net_DEL)
        j += 1
    i += 1

# calculate the ratio of network data in ccle data
i = 0
for i in range(len(mutcna_col.columns)):
    util.update_progress(i, len(mutcna_col.columns))
    if data_MUTCNA.loc[i, 'CCLE Mut'] != 0:
        data_MUTCNA.loc[i, 'Ratio of Mut'] = float(data_MUTCNA.loc[i, 'Network Mut'])/float(data_MUTCNA.loc[i, 'CCLE Mut'])*100
    elif data_MUTCNA.loc[i, 'CCLE Mut'] == 0:
        data_MUTCNA.loc[i, 'Ratio of Mut'] = 0

    if data_MUTCNA.loc[i, 'CCLE CNV AMP'] != 0:
        data_MUTCNA.loc[i, 'Ratio of CNV AMP'] = float(data_MUTCNA.loc[i, 'Network CNV AMP'])/float(data_MUTCNA.loc[i, 'CCLE CNV AMP'])*100
    elif data_MUTCNA.loc[i, 'CCLE CNV AMP'] == 0:
        data_MUTCNA.loc[i, 'Ratio of CNV AMP'] = 0

    if data_MUTCNA.loc[i, 'CCLE CNV DEL'] != 0:
        data_MUTCNA.loc[i, 'Ratio of CNV DEL'] = float(data_MUTCNA.loc[i, 'Network CNV DEL'])/float(data_MUTCNA.loc[i, 'CCLE CNV DEL'])*100
    elif data_MUTCNA.loc[i, 'CCLE CNV DEL'] == 0:
        data_MUTCNA.loc[i, 'Ratio of CNV DEL'] = 0
    i += 1
# calculate the average of each ratio
data_MUTCNA.loc[i, 'Ratio of Mut'] = sum(data_MUTCNA['Ratio of Mut'][0:i])/len(mutcna_col.columns)
data_MUTCNA.loc[i, 'Ratio of CNV AMP'] = sum(data_MUTCNA['Ratio of CNV AMP'][0:i])/len(mutcna_col.columns)
data_MUTCNA.loc[i, 'Ratio of CNV DEL'] = sum(data_MUTCNA['Ratio of CNV DEL'][0:i])/len(mutcna_col.columns)
data_MUTCNA.to_csv('data_Num_MUTCNA.csv', index=False)

# Count the number of drug and the data that have cell line name
# with 'LARGE_INTESTINE' and same gene name with network
data_Drug = pd.DataFrame([], columns=['Drug']+['Target']+['Total Cell line number']+
                                     ['Number of Large intestine']+['Target in Network'])
num = pd.DataFrame([], columns=['Number of data in each drug'])
i = 0
loc = 0
for i in range(len(therapy['Compound'])):
    util.update_progress(i, len(therapy['Compound']))
    drug = therapy.loc[i,'Compound']
    target = therapy.loc[i, 'Target']
    j = 0
    k = 0
    num_LI = 0
    if i == 0:
        therapy_data = therapy[therapy['Compound'].str.contains(drug)]
        data_CL = therapy_data['CCLE Cell Line Name']
        data_Drug.loc[loc, 'Drug'] = drug
        data_Drug.loc[loc, 'Target'] = target
        for j in range(len(data_CL)):
            if data_CL.iloc[j].find('LARGE_INTESTINE') > -1:
                num_LI += 1
            j += 1
        for k in gene.index:
            gene_index = gene.loc[k, 'node_name']
            if target.find(gene_index) > -1:
                data_Drug.loc[loc, 'target in network'] = gene_index
        data_Drug.loc[loc, 'Number of Large intestine'] = num_LI
        loc += 1
    else:
        if drug != therapy.loc[i-1, 'Compound']:
            num.loc[loc-1, 'Number of data in each drug'] = i
            therapy_data = therapy[therapy['Compound'].str.contains(drug)]
            data_CL = therapy_data['CCLE Cell Line Name']
            data_Drug.loc[loc, 'Drug'] = drug
            data_Drug.loc[loc, 'Target'] = target
            if loc == 1:
                data_Drug.loc[loc-1, 'Total Cell line number'] = i
            else:
                data_Drug.loc[loc-1, 'Total Cell line number'] = i - num.loc[loc-2, 'Number of data in each drug']
            for j in range(len(data_CL)):
                if data_CL.iloc[j].find('LARGE_INTESTINE') > -1:
                    num_LI += 1
                j += 1
            for k in gene.index:
                gene_index = gene.loc[k, 'node_name']
                if target.find(gene_index) > -1:
                    data_Drug.loc[loc, 'Target in Network'] = gene_index
            data_Drug.loc[loc, 'Number of Large intestine'] = num_LI
            loc += 1
    i += 1
data_Drug.loc[loc-1, 'Total Cell line number'] = i - num.loc[loc-2, 'Number of data in each drug']
data_Drug.to_csv('data_Num_Drug.csv', index=False)

set_trace()