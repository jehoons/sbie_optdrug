# -*- coding: utf-8 -*-
import pickle
from os.path import dirname,join,exists
from ipdb import set_trace
import json
import pandas as pd
import sbie_optdrug
from sbie_optdrug.dataset import filelist
from sbie_optdrug.dataset import ccle
from mytermutils import progressbar

""" requirements """
inputfile = join(dirname(__file__), '..', 'tab_s3', 'TABLE.S3.LOGICAL-EQUATIONS.TXT')

""" results """
outputfile = join(dirname(__file__), 'TABLE.S2.NODE-NAME.CSV')

config = {'input': inputfile, 'output': outputfile}


def getconfig():

    return config


def run(config=None):

    if config == None:
        config = getconf()

    # make node_name file from logical_rule.txt
    # 1. open the logical rule file to get the node name
    model = open(config['input'], "r+")
    # 2. make the dataframe of node name
    gene_name = pd.DataFrame([], columns=['gene_name'])
    loc = 0 # location of node_name
    while True:
        model_line = model.readline() # read the each line of model
        b = 0 # starting point of node
        f = 0 # finishing point of node
        if not model_line: break # finish when line is empty
        else: # if not get the node name and put it in node_name
            # in model, node name is S_TGFbeta *= logical rule
            b = model_line.find('_')+1 # starting point is after '_'
            f = model_line.find('*')-1 # finishing point is before '*'
            gene_rule = model_line[b:f] # get the node name
            gene_name.loc[loc, 'gene_name'] = gene_rule # put node name in node_name
            loc += 1 # change the location of node_name
    model.close()

    gene_name_1 = pd.DataFrame([], columns=['node_name'])
    # get more clear gene name
    # ex) 'beta_cat' -> 'Bcat' and 'Bcl_2' -> 'Bcl2'
    # remove the underbar('_') and change 'beta' to B
    i = 0 # location of gene_name and iteration
    for i in gene_name.index:
        progressbar.update(i, len(gene_name.index)) # check the time span
        gene = gene_name.loc[i, 'gene_name'] # get the node name
        while gene.find('_') > -1: # repeat when there is no '_' in node name
            loc = gene.find('_') # location of '_'
            fin = len(gene) # length of node name
            new = gene[0:loc]+gene[loc+1:fin] # remove the '_' and save it to new
            if new.find('_') > -1: # if there is '_' again, continue this process
                gene = new # change the node name to new
            else: # if there is no '_'
                gene = new # change the node name to new
                break # finish the while loop
        if gene.find('beta') > -1: # check if there is 'beta' in node name
            loc_b = gene.find('beta') # location of 'beta'
            fin_b = len(gene) # length of node name
            gene = gene[0:loc_b]+'B'+gene[loc_b+4:fin_b] # change the 'beta' to 'B'
        elif gene.find('Cyclin') > -1:
            loc_b = gene.find('Cyclin')  # location of 'cyclin'
            fin_b = len(gene)  # length of node name
            gene = gene[0:loc_b] + 'Cyc' + gene[loc_b+6:fin_b]  # change the 'cyclin' to 'Cyc'
        elif gene.find('Caspase') > -1:
            loc_b = gene.find('Caspase')  # location of 'caspase'
            fin_b = len(gene)  # length of node name
            gene = gene[0:loc_b] + 'Casp' + gene[loc_b+7:fin_b]  # change the 'caspase' to 'casp'
        # change the node to upper case and save the new node name in data frame
        gene_name_1.loc[i, 'node_name'] = gene.upper()
        i += 1 # change the location

    # get more clear gene name2
    # if gene name is too long and overlap with other gene name
    # if gene name is too long and is gene expression
    i = 0
    for i in gene_name_1.index:
        progressbar.update(i, len(gene_name_1.index))  # check the time span
        gene = gene_name_1.loc[i, 'node_name'] # get the gene name
        # find the overlapped gene
        temp = gene_name_1[gene_name_1['node_name'].str.contains(gene)]
        # if gene name is gene expression(apoptosis, dna repair, dna damage
        if len(gene) == 9:
            # make gene name to empty
            gene_name_1.loc[i, 'node_name'] = ''
        # if gene name is not empty
        if len(gene) > 1:
            # if there is overlapped gene
            if len(temp) > 1:
                # first one is tmp1, second one is tmp2
                tmp1 = temp.iloc[0]; tmp1 = tmp1['node_name']
                tmp2 = temp.iloc[1]; tmp2 = tmp2['node_name']
                # if difference between tmp1 and tmp2 is over one
                # find the location of longer gene name
                # make that gene name to empty
                if len(tmp1)+1 < len(tmp2):
                    t = gene_name_1[gene_name_1['node_name'] == tmp2].index.tolist()
                    gene_name_1.loc[t, 'node_name'] = ''
                if len(tmp1) > len(tmp2)+1:
                    t = gene_name_1[gene_name_1['node_name'] == tmp1].index.tolist()
                    gene_name_1.loc[t, 'node_name'] = ''
        i += 1 # change the location

    # get more clear gene name3
    # make new dataframe for node name
    node_name = pd.DataFrame([], columns=['node_name'])
    j = 0 # location of gene_name_1
    loc = 0 # location of node_name
    for j in gene_name_1.index:
        progressbar.update(j, len(gene_name_1.index))  # check the time span
        gene = gene_name_1.loc[j, 'node_name'] # get the gene name
        # if gene name is not empty
        if len(gene) > 1:
            # if gene name is same with specific name
            # change the node name
            if gene == 'AMPATP':
                node_name.loc[loc, 'node_name'] = 'AMP'
                loc += 1
                node_name.loc[loc, 'node_name'] = 'ATP'
                loc += 1
            elif gene == 'TSC1TSC2':
                node_name.loc[loc, 'node_name'] = 'TSC1'
                loc += 1
                node_name.loc[loc, 'node_name'] = 'TSC2'
                loc += 1
            elif gene == 'CYTOCAPAF1':
                node_name.loc[loc, 'node_name'] = 'CYTC'
                loc += 1
                node_name.loc[loc, 'node_name'] = 'APAF1'
                loc += 1
            elif gene == 'ATMATR':
                node_name.loc[loc, 'node_name'] = 'ATM'
                loc += 1
                node_name.loc[loc, 'node_name'] = 'ATR'
                loc += 1
            elif gene == 'CHK12':
                node_name.loc[loc, 'node_name'] = 'CHK1'
                loc += 1
                node_name.loc[loc, 'node_name'] = 'CHK2'
                loc += 1
            # if the other case, change the gene name
            else:
                node_name.loc[loc, 'node_name'] = gene
                loc += 1

        j += 1 # change the location of gene_name_1

    node_name.to_csv(config['output'], index=False) # save this data frame to csv
