import json
import pickle
from os.path import dirname,join
import pandas as pd
from ipdb import set_trace
import sbie_optdrug
from sbie_optdrug.dataset import ccle,filelist
from termutil import progressbar


""" requirements """
inputfile = join(dirname(__file__), '..','tab_s2','TABLE.S2.NODE-NAME.CSV')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S1A.MUTCNA_CRC_NET.CSV')
outputfile_b = join(dirname(__file__), 'TABLE.S1B.THERAPY_CRC_NET.CSV')
outputfile_c = join(dirname(__file__), 'TABLE.S1C.NUM_MUTCNA.CSV')
outputfile_d = join(dirname(__file__), 'TABLE.S1D.NUM_DRUG.CSV')
outputfile_e = join(dirname(__file__), 'TABLE.S1E.LOF_GOF_INDV.CSV')

config = {
    'input': inputfile,
    'output_a': outputfile_a,
    'output_b': outputfile_b,
    'output_c': outputfile_c,
    'output_d': outputfile_d,
    'output_e': outputfile_e
    }


def getconfig():

    return config


def run(config=None):

    # Bring data from filelist
    mutcna = ccle.mutcna()
    therapy = ccle.therapy()
    mutcna_col = mutcna.filter(regex='LARGE_INTESTINE')
    therapy_col = therapy[therapy['CCLE Cell Line Name'].str.contains("LARGE_INTESTINE")]
    gene = pd.read_csv(config['input'])
    del_list = ['PKC', 'IKK', 'ERK', 'P90', 'P27', 'P15', 'P70', 'GLUT1', 'GSH']

    # Select data that has 'LARGE INTESTINE' and same gene name with network
    i = 0
    for i in gene.index:
        progressbar.update(i, gene.shape[0])
        gene_index = gene.loc[i,'node_name']
        data_mut = mutcna_col[mutcna_col.index.str.contains(gene_index)]
        data_therapy = therapy_col[therapy_col['Target'].str.contains(gene_index)]
        if i == 0:
            total_mut = data_mut
            total_therapy = data_therapy
        else:
            if gene_index == 'AMP':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if (gene_name.find('AMPD') > -1) & (gene_name.find(gene_index) < gene_name.find('_')):
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'NF1':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) == 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'RTK':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) > 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'RAS':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) > -1:
                        if (gene_name.find('DIRAS') > -1) | (gene_name.find('ERAS') > -1) | \
                                (gene_name.find('HRAS') > -1) | (gene_name.find('KRAS') > -1) | \
                                (gene_name.find('MRAS') > -1) | (gene_name.find('NKI') > -1) | \
                                (gene_name.find('NRAS') > -1) | (gene_name.find('RAS') == 0) | (gene_name.find('RRAS') > -1):
                            temp = data_mut.ix[[j], :]
                            if len(data_mut_cor) == 0:
                                data_mut_cor = temp
                            else:
                                data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'RAF':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if (gene_name.find(gene_index) > -1) & (gene_name.find('TRAF') == -1) & (gene_name.find('PRAF') == -1):
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'APC':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if (gene_name.find(gene_index) == 0) | (gene_name.find('SAPCD') > -1):
                        if gene_name.find('APCS') == -1:
                            temp = data_mut.ix[[j], :]
                            if len(data_mut_cor) == 0:
                                data_mut_cor = temp
                            else:
                                data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'TSC2':
                j = 0
                data_mut_cor = []
                gene_list = ['TSC2_MUT', 'TSC2_AMP', 'TSC2_DEL']
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name in gene_list:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'P53':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if (gene_name.find('TP53') == 0) | (gene_name.find('WRAP53') == 0):
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'BAD':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) == 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'RB':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) == 0:
                        if (gene_name.find('RBC') == -1) & (gene_name.find('RBF') == -1) & \
                                (gene_name.find('RBK') == -1) & (gene_name.find('RBM') == -1) & \
                                (gene_name.find('RBP') == -1) & (gene_name.find('RBX') == -1):
                            temp = data_mut.ix[[j], :]
                            if len(data_mut_cor) == 0:
                                data_mut_cor = temp
                            else:
                                data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'E2F':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) == 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'P14':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find('RPP14') == 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'CDH1':
                j = 0
                data_mut_cor = []
                gene_list = ['CDH1_MUT', 'CDH1_AMP', 'CDH1_DEL', 'PCDH1_MUT', 'PCDH1_AMP', 'PCDH1_DEL']
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name in gene_list:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'P21':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find('RPP21') > -1:
                        if gene_name.find('ARPP21') == -1:
                            temp = data_mut.ix[[j], :]
                            if len(data_mut_cor) == 0:
                                data_mut_cor = temp
                            else:
                                data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'BAK':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) == 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'ROS':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) == 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'TCF':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) == 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'ATM':
                j = 0
                data_mut_cor = []
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name.find(gene_index) == 0:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'ATR':
                j = 0
                data_mut_cor = []
                gene_list = ['ATR_MUT', 'ATR_AMP', 'ATR_DEL', 'ATRIP_MUT', 'ATRIP_AMP', 'ATRIP_DEL']
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name in gene_list:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index == 'EEF2':
                j = 0
                data_mut_cor = []
                gene_list = ['EEF2_MUT', 'EEF2_AMP', 'EEF2_DEL']
                for j in range(len(data_mut.index)):
                    gene_name = data_mut.index[j]
                    if gene_name in gene_list:
                        temp = data_mut.ix[[j], :]
                        if len(data_mut_cor) == 0:
                            data_mut_cor = temp
                        else:
                            data_mut_cor = data_mut_cor.append(temp)
                    j += 1
                data_mut = data_mut_cor
            elif gene_index in del_list:
                continue
            total_mut = pd.concat([total_mut, data_mut])
            total_therapy = pd.concat([total_therapy, data_therapy])
        i += 1

    total_mut.to_csv(config['output_a'])
    total_therapy.to_csv(config['output_b'], index=False)

    # Count the number of Mutation, amplification, deletion gene
    # and the number of gene that correspond with network
    data_MUTCNA = pd.DataFrame([], columns=['Cell Line', 'CCLE Mut', 'CCLE CNV AMP',
        'CCLE CNV DEL', 'Network Mut', 'Network CNV AMP', 'Network CNV DEL',
        'Ratio of Mut', 'Ratio of CNV AMP', 'Ratio of CNV DEL'])
    i = 0
    for i in range(len(mutcna_col.columns)):
        progressbar.update(i, len(mutcna_col.columns))
        data_MUTCNA.loc[i, 'Cell Line'] = mutcna_col.columns[i]
        data = mutcna_col[mutcna_col.columns[i]]
        data_total = data[data == 1]
        data_total_MUT = data_total.filter(regex='_MUT')
        data_total_AMP = data_total.filter(regex='_AMP')
        data_total_DEL = data_total.filter(regex='_DEL')
        data_MUTCNA.loc[i, 'CCLE Mut'] = len(data_total_MUT)
        data_MUTCNA.loc[i, 'CCLE CNV AMP'] = len(data_total_AMP)
        data_MUTCNA.loc[i, 'CCLE CNV DEL'] = len(data_total_DEL)
        data_net = total_mut[mutcna_col.columns[i]]
        data_net_sub = data_net[data_net == 1]
        data_net_MUT = data_net_sub.filter(regex='_MUT')
        data_net_AMP = data_net_sub.filter(regex='_AMP')
        data_net_DEL = data_net_sub.filter(regex='_DEL')
        data_MUTCNA.loc[i, 'Network Mut'] = len(data_net_MUT)
        data_MUTCNA.loc[i, 'Network CNV AMP'] = len(data_net_AMP)
        data_MUTCNA.loc[i, 'Network CNV DEL'] = len(data_net_DEL)
        i += 1

    # calculate the ratio of network data in ccle data
    i = 0
    for i in range(len(mutcna_col.columns)):
        progressbar.update(i, len(mutcna_col.columns))

        if data_MUTCNA.loc[i, 'CCLE Mut'] != 0:
            data_MUTCNA.loc[i, 'Ratio of Mut'] = float(data_MUTCNA.loc[i,
                'Network Mut'])/float(data_MUTCNA.loc[i, 'CCLE Mut'])*100

        elif data_MUTCNA.loc[i, 'CCLE Mut'] == 0:
            data_MUTCNA.loc[i, 'Ratio of Mut'] = 0

        if data_MUTCNA.loc[i, 'CCLE CNV AMP'] != 0:
            data_MUTCNA.loc[i, 'Ratio of CNV AMP'] = float(data_MUTCNA.loc[i,
                'Network CNV AMP'])/float(data_MUTCNA.loc[i, 'CCLE CNV AMP'])*100

        elif data_MUTCNA.loc[i, 'CCLE CNV AMP'] == 0:
            data_MUTCNA.loc[i, 'Ratio of CNV AMP'] = 0

        if data_MUTCNA.loc[i, 'CCLE CNV DEL'] != 0:
            data_MUTCNA.loc[i, 'Ratio of CNV DEL'] = float(data_MUTCNA.loc[i,
                'Network CNV DEL'])/float(data_MUTCNA.loc[i, 'CCLE CNV DEL'])*100

        elif data_MUTCNA.loc[i, 'CCLE CNV DEL'] == 0:
            data_MUTCNA.loc[i, 'Ratio of CNV DEL'] = 0

        i += 1

    # calculate the average of each ratio
    data_MUTCNA.loc[i, 'Ratio of Mut'] = \
        sum(data_MUTCNA['Ratio of Mut'][0:i])/len(mutcna_col.columns)

    data_MUTCNA.loc[i, 'Ratio of CNV AMP'] = \
        sum(data_MUTCNA['Ratio of CNV AMP'][0:i])/len(mutcna_col.columns)

    data_MUTCNA.loc[i, 'Ratio of CNV DEL'] = \
        sum(data_MUTCNA['Ratio of CNV DEL'][0:i])/len(mutcna_col.columns)

    data_MUTCNA.to_csv(config['output_c'], index=False)

    # Count the number of drug and the data that have cell line name
    # with 'LARGE_INTESTINE' and same gene name with network

    data_Drug = pd.DataFrame([], columns=['Drug', 'Target', 'Total Cell line number',
        'Number of Large intestine', 'Target in Network'])

    num = pd.DataFrame([], columns=['Number of data in each drug'])
    i = 0
    loc = 0
    for i in range(len(therapy['Compound'])):
        progressbar.update(i, len(therapy['Compound']))
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
                    data_Drug.loc[loc-1, 'Total Cell line number'] = i - num.loc[
                        loc-2, 'Number of data in each drug']

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

    data_Drug.loc[loc-1, 'Total Cell line number'] = i - num.loc[loc-2,
        'Number of data in each drug']

    data_Drug.to_csv(config['output_d'], index=False)
