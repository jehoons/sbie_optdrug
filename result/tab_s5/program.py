# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import json
import pickle
from os.path import dirname,join
from sbie_optdrug.dataset import filelist
import pandas as pd
from ipdb import set_trace
import sbie_optdrug
from sbie_optdrug.dataset import ccle
from termutil import progressbar


""" requirements """
inputfile_a = join(dirname(__file__), '..','tab_s2','TABLE.S2.NODE-NAME.CSV')
inputfile_b = join(dirname(__file__), '..','tab_s1','TABLE.S1A.MUTCNA_CRC_NET.CSV')
inputfile_c = join(dirname(__file__), '..','tab_s1','TABLE.S1B.THERAPY_CRC_NET.CSV')


""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S5A.COPYNUMVAR_data.json')
outputfile_b = join(dirname(__file__), 'TABLE.S5B.MUTATION_data.json')
outputfile_c = join(dirname(__file__), 'TABLE.S5C.DRUG_data.json')


config = {
    'program': 'template',
    'input': {
        'input_a': inputfile_a,
        'input_b': inputfile_b,
        'input_c': inputfile_c
        },
    'output': {
        'output_a': outputfile_a,
        'output_b': outputfile_b,
        'output_c': outputfile_c
        }
    }

def getconfig():

    return config

def run(config=None):
    gene = pd.read_csv(config['input']['input_a'])
    data_mutcna = pd.read_csv(config['input']['input_b'])
    data_therapy = pd.read_csv(config['input']['input_c'])

    copy_number_data = open(config['output']['output_a'], 'w')
    mutation_data = open(config['output']['output_b'], 'w')
    mutcna_index = data_mutcna['Description']
    mutcna = data_mutcna[data_mutcna.columns[2:]]
    mutcna.index = mutcna_index
    mutcna_MUT = mutcna[mutcna.index.str.contains('_MUT')]
    mutcna_AMP = mutcna[mutcna.index.str.contains('_AMP')]
    mutcna_DEL = mutcna[mutcna.index.str.contains('_DEL')]
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
            mutcna_MUT_cln_data = mutcna_MUT_cln[mutcna_MUT_cln == 1]
            mutcna_AMP_cln_data = mutcna_AMP_cln[mutcna_AMP_cln == 1]
            mutcna_DEL_cln_data = mutcna_DEL_cln[mutcna_DEL_cln == 1]
            set_trace()
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
                name = gene.loc[j, 'node_name']
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
                    set_trace()
                    if len(mutcna_AMP_cln_data_node) != 0:
                        if len(node_data_cnv) == 0:
                            node_data_cnv_add[name]['function'] = 'AMP'
                            node_data_cnv = node_data_cnv_add
                        else:
                            node_data_cnv_add[name]['function'] = 'AMP'
                            node_data_cnv = dict(node_data_cnv.items() + node_data_cnv_add.items())
                if len(mutcna_DEL_cln_data) != 0:
                    mutcna_DEL_cln_data_node = mutcna_DEL_cln_data[mutcna_DEL_cln_data.index.str.contains(name)]
                    set_trace()
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
    json.dump(cnd, copy_number_data, indent=3, sort_keys=True)
    json.dump(mut, mutation_data, indent=3, sort_keys=True)
    copy_number_data.close()
    mutation_data.close()

    drug_data = open(config['output']['output_c'], 'w')
    i = 0
    drug = {}
    for i in data_therapy['CCLE Cell Line Name'].index:
        progressbar.update(i, len(data_therapy['CCLE Cell Line Name']))
        cln = data_therapy['CCLE Cell Line Name'][i]
        d_name = data_therapy['Compound'][i]
        target = data_therapy['Target'][i]
        # dose = data_therapy['Doses'][i]
        drug_add = {cln: {d_name: {'type': 'inhibitor', 'target': target}}}
        if cln in drug:
            new_drug = {d_name: {'type': 'inhibitor', 'target': target}}
            old_drug = drug[cln]
            drug[cln] = dict(old_drug.items() + new_drug.items())
        else:
            if i == 0:
                drug = drug_add
            else:
                drug = dict(drug.items() + drug_add.items())
        i += 1
    json.dump(drug, drug_data, indent=3, sort_keys=True)
    drug_data.close()
