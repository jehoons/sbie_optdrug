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
inputfile_d = join(dirname(__file__), '..','tab_s1','TABLE.S1E.LOF_GOF_INDV.CSV')
inputfile_e = join(dirname(__file__), '..','tab_s4','TABLE_S4A_MUTGENES.CSV')
inputfile_f = join(dirname(__file__), '..','tab_s4','TABLE_S4C_TUMORSUPPRESSORS_AND_ONCOGENES.CSV')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE.S5A.COPYNUMVAR_data_s1.json')
outputfile_b = join(dirname(__file__), 'TABLE.S5A.COPYNUMVAR_data_s4.json')
outputfile_c = join(dirname(__file__), 'TABLE.S5B.MUTATION_data_s1.json')
outputfile_d = join(dirname(__file__), 'TABLE.S5B.MUTATION_data_s4.json')
outputfile_e = join(dirname(__file__), 'TABLE.S5C.DRUG_data.json')

config = {
    'program': 'template',
    'input': {
        'input_a': inputfile_a,
        'input_b': inputfile_b,
        'input_c': inputfile_c,
        'input_d': inputfile_d,
        'input_e': inputfile_e,
        'input_f': inputfile_f
        },
    'output': {
        'output_a': outputfile_a,
        'output_b': outputfile_b,
        'output_c': outputfile_c,
        'output_d': outputfile_d,
        'output_e': outputfile_e
        }
    }

def getconfig():

    return config

def run(config=None):
    gene = pd.read_csv(config['input']['input_a'])
    data_mutcna = pd.read_csv(config['input']['input_b'])
    data_therapy = pd.read_csv(config['input']['input_c'])
    LOF_GOF_s1 = pd.read_csv(config['input']['input_d']) # index : number
    Mutagen_s4 = pd.read_csv(config['input']['input_e']) # index : number
    LOF_GOF_s4 = pd.read_csv(config['input']['input_f']) # index : number

    copy_number_data_s1 = open(config['output']['output_a'], 'w')
    copy_number_data_s4 = open(config['output']['output_b'], 'w')
    mutation_data_s1 = open(config['output']['output_c'], 'w')
    mutation_data_s4 = open(config['output']['output_d'], 'w')
    mutcna_index = data_mutcna['Description']
    mutcna = data_mutcna[data_mutcna.columns[2:]]
    mutcna.index = mutcna_index
    mutcna_MUT = mutcna[mutcna.index.str.contains('_MUT')]
    mutcna_AMP = mutcna[mutcna.index.str.contains('_AMP')]
    mutcna_DEL = mutcna[mutcna.index.str.contains('_DEL')]
    i = 0
    cnd_s1 = {}
    mut_s1 = {}
    cnd_s4 = {}
    mut_s4 = {}
    for i in range(len(mutcna.columns)):
        progressbar.update(i, len(mutcna.columns))
        cln = mutcna.columns[i]
        if (len(cln) != 0) & (cln != 'Description'):
            cnd_add_s1 = {cln: {}}
            mut_add_s1 = {cln: {}}
            cnd_add_s4= {cln: {}}
            mut_add_s4 = {cln: {}}
            mutcna_MUT_cln = mutcna_MUT[cln]
            mutcna_AMP_cln = mutcna_AMP[cln]
            mutcna_DEL_cln = mutcna_DEL[cln]
            mutcna_MUT_cln_data = mutcna_MUT_cln[mutcna_MUT_cln == 1]
            mutcna_AMP_cln_data = mutcna_AMP_cln[mutcna_AMP_cln == 1]
            mutcna_DEL_cln_data = mutcna_DEL_cln[mutcna_DEL_cln == 1]
            if len(cnd_s1) == 0:
                cnd_s1 = cnd_add_s1
            elif len(cnd_s1) != 0:
                cnd_s1 = dict(cnd_s1.items() + cnd_add_s1.items())

            if len(mut_s1) == 0:
                mut_s1 = mut_add_s1
            elif len(mut_s1) != 0:
                mut_s1 = dict(mut_s1.items() + mut_add_s1.items())

            if len(cnd_s4) == 0:
                cnd_s4 = cnd_add_s4
            elif len(cnd_s4) != 0:
                cnd_s4 = dict(cnd_s4.items() + cnd_add_s4.items())

            if len(mut_s4) == 0:
                mut_s4 = mut_add_s4
            elif len(mut_s4) != 0:
                mut_s4 = dict(mut_s4.items() + mut_add_s4.items())

            j = 0
            node_data_cnv_s1 = {}
            node_data_mut_s1 = {}
            node_data_cnv_s4 = {}
            node_data_mut_s4 = {}
            for j in gene.index:
                name = gene.loc[j, 'node_name']
                node_data_cnv_add_s1 = {name: {'function': '', 'intensity': 0.5}}
                node_data_mut_add_s1 = {name: {'function': '', 'intensity': 0.5}}
                node_data_cnv_add_s4 = {name: {'function': '', 'intensity': 0.5}}
                node_data_mut_add_s4 = {name: {'function': '', 'intensity': 0.5}}
                if len(mutcna_MUT_cln_data) > 0:
                    mutcna_MUT_cln_data_node = mutcna_MUT_cln_data[mutcna_MUT_cln_data.index.str.contains(name)]
                    if len(mutcna_MUT_cln_data_node) > 0:
                        k = 0
                        for k in range(len(mutcna_MUT_cln_data_node.index)):
                            chk_list = mutcna_MUT_cln_data_node.index[k]
                            L_G_list = LOF_GOF_s1[LOF_GOF_s1['Description'] == chk_list]['Loss or Gain']
                            if L_G_list.item() == 'Gain':
                                L_G = 'GOF'
                            elif L_G_list.item() == 'Loss':
                                L_G = 'LOF'
                            if len(node_data_mut_s1) == 0:
                                node_data_mut_add_s1[name]['function'] = L_G
                                node_data_mut_s1 = node_data_mut_add_s1
                            elif len(node_data_mut_s1) > 0:
                                if node_data_mut_add_s1[name]['function'] == '':
                                    node_data_mut_add_s1[name]['function'] = L_G
                                    node_data_mut_s1 = dict(node_data_mut_s1.items() + node_data_mut_add_s1.items())
                                else:
                                    if L_G == node_data_mut_add_s1[name]['function']:
                                        node_data_mut_add_s1[name]['function'] = L_G
                                        node_data_mut_s1 = dict(node_data_mut_s1.items() + node_data_mut_add_s1.items())
                                    elif L_G != node_data_mut_add_s1[name]['function']:
                                        node_data_mut_add_s1[name]['function'] = 'GOFLOF'
                                        node_data_mut_s1 = dict(node_data_mut_s1.items() + node_data_mut_add_s1.items())

                            chk_list_name = chk_list[0:chk_list.find('_')]
                            if chk_list_name.find('.') > -1:
                                chk_list_name = chk_list_name[0:chk_list_name.find('.')]
                            if chk_list_name.find('-') > -1:
                                if chk_list_name.find('-') < chk_list_name.find(name):
                                    chk_list_name = chk_list_name[chk_list_name.find(name):]
                                else:
                                    chk_list_name = chk_list_name[chk_list_name.find(name):chk_list_name.find('-')]
                            mut_list = LOF_GOF_s4[LOF_GOF_s4['ID']==chk_list_name]
                            if len(mut_list) > 0:
                                temp = dict(mut_list['CATEGORY']).values()
                                if 'UNKNOWN' in temp:
                                    if 'Oncogene' in temp:
                                        if 'Tumor suppressor gene' in temp:
                                            L_G = 'GOFLOF'
                                        else:
                                            #if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            #else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                    else:
                                        if 'Tumor suppressor gene' in temp:
                                            #if chk_list.find('-AS') > -1:
                                            #    L_G = 'Supp_LOF'
                                            #else:
                                            #    L_G = 'Supp_GOF'
                                            L_G = 'LOF'
                                        else: # unknown = Onco
                                            #if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            #else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                else:
                                    if 'Oncogene' in temp:
                                        if 'Tumor suppressor gene' in temp:
                                            L_G = 'GOFLOF'
                                        else:
                                            #if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            #else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                    else:
                                        if 'Tumor suppressor gene' in temp:
                                            #if chk_list.find('-AS') > -1:
                                            #    L_G = 'Supp_LOF'
                                            #else:
                                            #    L_G = 'Supp_GOF'
                                            L_G = 'LOF'
                            else:
                                #if chk_list.find('-AS') > -1:
                                #    L_G = 'LOF'
                                #else:
                                #    L_G = 'GOF'
                                L_G = 'GOF'
                            if len(node_data_mut_s4) == 0:
                                node_data_mut_add_s4[name]['function'] = L_G
                                node_data_mut_s4 = node_data_mut_add_s4
                            elif len(node_data_mut_s4) > 0:
                                if node_data_mut_add_s4[name]['function'] == '':
                                    node_data_mut_add_s4[name]['function'] = L_G
                                    node_data_mut_s4 = dict(node_data_mut_s4.items() + node_data_mut_add_s4.items())
                                else:
                                    if L_G == node_data_mut_add_s4[name]['function']:
                                        node_data_mut_add_s4[name]['function'] = L_G
                                        node_data_mut_s4 = dict(node_data_mut_s4.items() + node_data_mut_add_s4.items())
                                    elif L_G != node_data_mut_add_s4[name]['function']:
                                        node_data_mut_add_s4[name]['function'] = 'GOFLOF'
                                        node_data_mut_s4 = dict(node_data_mut_s4.items() + node_data_mut_add_s4.items())
                            k += 1
                if len(mutcna_AMP_cln_data) > 0:
                    mutcna_AMP_cln_data_node = mutcna_AMP_cln_data[mutcna_AMP_cln_data.index.str.contains(name)]
                    if len(mutcna_AMP_cln_data_node) > 0:
                        k = 0
                        for k in range(len(mutcna_AMP_cln_data_node.index)):
                            chk_list = mutcna_AMP_cln_data_node.index[k]
                            L_G_list = LOF_GOF_s1[LOF_GOF_s1['Description'] == chk_list]['Loss or Gain']
                            if L_G_list.item() == 'Gain':
                                L_G = 'GOF'
                            elif L_G_list.item() == 'Loss':
                                L_G = 'LOF'
                            if len(node_data_cnv_s1) == 0:
                                node_data_cnv_add_s1[name]['function'] = L_G
                                node_data_cnv_s1 = node_data_cnv_add_s1
                            elif len(node_data_cnv_s1) > 0:
                                if node_data_cnv_add_s1[name]['function'] == '':
                                    node_data_cnv_add_s1[name]['function'] = L_G
                                    node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())
                                else:
                                    if L_G == node_data_cnv_add_s1[name]['function']:
                                        node_data_cnv_add_s1[name]['function'] = L_G
                                        node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())
                                    elif L_G != node_data_cnv_add_s1[name]['function']:
                                        node_data_cnv_add_s1[name]['function'] = 'GOFLOF'
                                        node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())

                            chk_list_name = chk_list[0:chk_list.find('_')]
                            if chk_list_name.find('.') > -1:
                                chk_list_name = chk_list_name[0:chk_list_name.find('.')]
                            if chk_list_name.find('-') > -1:
                                if chk_list_name.find('-') < chk_list_name.find(name):
                                    chk_list_name = chk_list_name[chk_list_name.find(name):]
                                else:
                                    chk_list_name = chk_list_name[chk_list_name.find(name):chk_list_name.find('-')]
                            mut_list = LOF_GOF_s4[LOF_GOF_s4['ID'] == chk_list_name]
                            if len(mut_list) > 0:
                                temp = dict(mut_list['CATEGORY']).values()
                                if 'UNKNOWN' in temp:
                                    if 'Oncogene' in temp:
                                        if 'Tumor suppressor gene' in temp:
                                            L_G = 'GOFLOF'
                                        else:
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            # else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                    else:
                                        if 'Tumor suppressor gene' in temp:
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Supp_LOF'
                                            # else:
                                            #    L_G = 'Supp_GOF'
                                            L_G = 'LOF'
                                        else:  # unknown = Onco
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            # else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                else:
                                    if 'Oncogene' in temp:
                                        if 'Tumor suppressor gene' in temp:
                                            L_G = 'GOFLOF'
                                        else:
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            # else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                    else:
                                        if 'Tumor suppressor gene' in temp:
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Supp_LOF'
                                            # else:
                                            #    L_G = 'Supp_GOF'
                                            L_G = 'LOF'
                            else:
                                # if chk_list.find('-AS') > -1:
                                #    L_G = 'LOF'
                                # else:
                                #    L_G = 'GOF'
                                L_G = 'GOF'
                            if len(node_data_cnv_s4) == 0:
                                node_data_cnv_add_s4[name]['function'] = L_G
                                node_data_cnv_s4 = node_data_cnv_add_s4
                            elif len(node_data_cnv_s4) > 0:
                                if node_data_cnv_add_s4[name]['function'] == '':
                                    node_data_cnv_add_s4[name]['function'] = L_G
                                    node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                                else:
                                    if L_G == node_data_cnv_add_s4[name]['function']:
                                        node_data_cnv_add_s4[name]['function'] = L_G
                                        node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                                    elif L_G != node_data_cnv_add_s4[name]['function']:
                                        node_data_cnv_add_s4[name]['function'] = 'GOFLOF'
                                        node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                            k += 1
                if len(mutcna_DEL_cln_data) > 0:
                    mutcna_DEL_cln_data_node = mutcna_DEL_cln_data[mutcna_DEL_cln_data.index.str.contains(name)]
                    if len(mutcna_DEL_cln_data_node) > 0:
                        k = 0
                        for k in range(len(mutcna_DEL_cln_data_node.index)):
                            chk_list = mutcna_DEL_cln_data_node.index[k]
                            L_G_list = LOF_GOF_s1[LOF_GOF_s1['Description'] == chk_list]['Loss or Gain']
                            if L_G_list.item() == 'Loss':
                                L_G = 'GOF'
                            elif L_G_list.item() == 'Gain':
                                L_G = 'LOF'
                            if len(node_data_cnv_s1) == 0:
                                if node_data_cnv_add_s1[name]['function'] == '':
                                    node_data_cnv_add_s1[name]['function'] = L_G
                                    node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())
                                else:
                                    if L_G == node_data_cnv_add_s1[name]['function']:
                                        node_data_cnv_add_s1[name]['function'] = L_G
                                        node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())
                                    elif L_G != node_data_cnv_add_s1[name]['function']:
                                        node_data_cnv_add_s1[name]['function'] = 'GOFLOF'
                                        node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())
                            elif len(node_data_cnv_s1) > 0:
                                if node_data_cnv_add_s1[name]['function'] == '':
                                    node_data_cnv_add_s1[name]['function'] = L_G
                                    node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())
                                else:
                                    if L_G == node_data_cnv_add_s1[name]['function']:
                                        node_data_cnv_add_s1[name]['function'] = L_G
                                        node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())
                                    elif L_G != node_data_cnv_add_s1[name]['function']:
                                        node_data_cnv_add_s1[name]['function'] = 'GOFLOF'
                                        node_data_cnv_s1 = dict(node_data_cnv_s1.items() + node_data_cnv_add_s1.items())

                            chk_list_name = chk_list[0:chk_list.find('_')]
                            if chk_list_name.find('.') > -1:
                                chk_list_name = chk_list_name[0:chk_list_name.find('.')]
                            if chk_list_name.find('-') > -1:
                                if chk_list_name.find('-') < chk_list_name.find(name):
                                    chk_list_name = chk_list_name[chk_list_name.find(name):]
                                else:
                                    chk_list_name = chk_list_name[chk_list_name.find(name):chk_list_name.find('-')]
                            mut_list = LOF_GOF_s4[LOF_GOF_s4['ID'] == chk_list_name]
                            if len(mut_list) > 0:
                                temp = dict(mut_list['CATEGORY']).values()
                                if 'UNKNOWN' in temp:
                                    if 'Oncogene' in temp:
                                        if 'Tumor suppressor gene' in temp:
                                            L_G = 'GOFLOF'
                                        else:
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            # else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                    else:
                                        if 'Tumor suppressor gene' in temp:
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Supp_LOF'
                                            # else:
                                            #    L_G = 'Supp_GOF'
                                            L_G = 'LOF'
                                        else:  # unknown = Onco
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            # else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                else:
                                    if 'Oncogene' in temp:
                                        if 'Tumor suppressor gene' in temp:
                                            L_G = 'GOFLOF'
                                        else:
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Onco_LOF'
                                            # else:
                                            #    L_G = 'Onco_GOF'
                                            L_G = 'GOF'
                                    else:
                                        if 'Tumor suppressor gene' in temp:
                                            # if chk_list.find('-AS') > -1:
                                            #    L_G = 'Supp_LOF'
                                            # else:
                                            #    L_G = 'Supp_GOF'
                                            L_G = 'LOF'
                            else:
                                # if chk_list.find('-AS') > -1:
                                #    L_G = 'LOF'
                                # else:
                                #    L_G = 'GOF'
                                L_G = 'GOF'
                            if len(node_data_cnv_s4) == 0:
                                if node_data_cnv_add_s4[name]['function'] == '':
                                    node_data_cnv_add_s4[name]['function'] = L_G
                                    node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                                else:
                                    if L_G == node_data_cnv_add_s4[name]['function']:
                                        node_data_cnv_add_s4[name]['function'] = L_G
                                        node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                                    elif L_G != node_data_cnv_add_s4[name]['function']:
                                        node_data_cnv_add_s4[name]['function'] = 'GOFLOF'
                                        node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                            elif len(node_data_cnv_s4) > 0:
                                if node_data_cnv_add_s4[name]['function'] == '':
                                    node_data_cnv_add_s4[name]['function'] = L_G
                                    node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                                else:
                                    if L_G == node_data_cnv_add_s4[name]['function']:
                                        node_data_cnv_add_s4[name]['function'] = L_G
                                        node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                                    elif L_G != node_data_cnv_add_s4[name]['function']:
                                        node_data_cnv_add_s4[name]['function'] = 'GOFLOF'
                                        node_data_cnv_s4 = dict(node_data_cnv_s4.items() + node_data_cnv_add_s4.items())
                            k += 1
                j += 1
            cnd_s1[cln] = node_data_cnv_s1
            mut_s1[cln] = node_data_mut_s1
            cnd_s4[cln] = node_data_cnv_s4
            mut_s4[cln] = node_data_mut_s4
        i += 1
    json.dump(cnd_s1, copy_number_data_s1, indent=3, sort_keys=True)
    json.dump(mut_s1, mutation_data_s1, indent=3, sort_keys=True)
    json.dump(cnd_s4, copy_number_data_s4, indent=3, sort_keys=True)
    json.dump(mut_s4, mutation_data_s4, indent=3, sort_keys=True)
    copy_number_data_s1.close()
    mutation_data_s1.close()
    copy_number_data_s4.close()
    mutation_data_s4.close()

    drug_data = open(config['output']['output_e'], 'w')
    i = 0
    drug = {}
    for i in data_therapy['CCLE Cell Line Name'].index:
        progressbar.update(i, len(data_therapy['CCLE Cell Line Name']))
        cln = data_therapy['CCLE Cell Line Name'][i]
        d_name = data_therapy['Compound'][i]
        target = data_therapy['Target'][i]
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
