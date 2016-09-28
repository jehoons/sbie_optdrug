# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Name, <email>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import json
import pickle
import os 
from os import system,mkdir
from os.path import dirname,join,exists,basename
import pandas as pd
from ipdb import set_trace
import sbie_optdrug
from sbie_optdrug import filelist
from sbie_optdrug.dataset import ccle
from util import progressbar
import re 
import sbie_optdrug 
from sbie_optdrug.dataset import ccle 
from util import progressbar
from bs4 import BeautifulSoup

""" requirements """
# inputfile_a = join(dirname(__file__), '..','tab_s2','TABLE.S2.NODE-NAME.CSV')
# inputfile_b = join(dirname(__file__), '..','tab_s1','TABLE.S1A.MUTCNA_CRC_NET.CSV')
# inputfile_c = join(dirname(__file__), '..','tab_s1','TABLE.S1B.THERAPY_CRC_NET.CSV')

""" results """
outputfile_a = join(dirname(__file__), 'TABLE_S4A_MUTGENES.CSV')
outputfile_b = join(dirname(__file__), 'TABLE_S4B_HTMLFILE_LIST.CSV')
outputfile_c = join(dirname(__file__), 'TABLE_S4C_TUMORSUPPRESSORS_AND_ONCOGENES.CSV')

config = {
    'program': 'Oncogene/TumorSuppressors Downloader',
    'scratch_dir': dirname(__file__)+'/untracked', 
    'input': {
        # 'a': inputfile_a,
        # 'b': inputfile_b,
        # 'c': inputfile_c
        },
    'output': {
        'a': outputfile_a,
        'b': outputfile_b,
        'c': outputfile_c,
        }
    }

    
def getconfig():

    return config


def addtag(pathname, addstr, prefix=True):

    pathdir = dirname(pathname)
    name, ext = basename(pathname).split('.')
    
    if prefix:
        return join(pathdir, '%s%s.%s' % (addstr,name,ext))

    else: 
        return join(pathdir, '%s%s.%s' % (name,addstr,ext))


def run_step1(config=None):

    """ 
    Here, phantomjs can be downloaded as following commands:
    wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
    # gene_name, html_name, class
    # APC, APC.html, TSG or Oncogene
    """
    output = config['output']['a']
    
    if not exists(output) or True :
        mutcna = ccle.mutcna()
        mutcna_names = mutcna.index.values.tolist()
        mut_list = []
        for name in mutcna_names:
            if re.search('.+_MUT$', name):
                mut_list.append( name.replace('_MUT', '') ) 

        mut_set = set(mut_list)        
        mut_list = [m for m in mut_set]
        df_mut = pd.DataFrame(mut_list, columns=['ID'])
        df_mut.to_csv(output, index=False)


def run_step2(config=None):

    inputfile = config['output']['a']
    output_dir = config['scratch_dir']
    output = config['output']['b']

    binfo_exec = dirname(__file__)+'/binfo.js'

    if not exists(output_dir):
        os.mkdir(output_dir)

    data = pd.read_csv(inputfile)
    gene_list = data['ID']

    df_output = pd.DataFrame([], columns=['HTML_FILE'])

    for i,gene in enumerate(gene_list):
        progressbar.update(i, len(gene_list))
        outputfile = join(output_dir, gene+'.html')
        if not exists(outputfile):
            system('phantomjs %s %s %s' % (binfo_exec, gene, outputfile))
        df_output.loc[i, 'HTML_FILE'] = outputfile 

    df_output.to_csv(output, index=False)


def run_step3(config=None):

    inputfile = config['output']['b']
    outputfile = config['output']['c']

    data = pd.read_csv(inputfile)

    for i in data.index: 
        progressbar.update(i, data.shape[0])
        genefile = data.loc[i, 'HTML_FILE']
        genename = basename(genefile).split('.')[0]

        gene_found = False 
        content_found = False
        content = 'UNKNOWN'

        if exists(genefile):
            gene_found = True 

            with open(genefile, 'rb') as f:
                lines = f.readlines()

            soup = BeautifulSoup("".join(lines), 'html.parser')
            tdlist = soup.find_all('td')

            if len(tdlist) >= 6 :
                content_found = True 
                content = tdlist[5].get_text()

        content = content.replace('-- & ', '')
        content = content.replace(' & --', '')

        data.loc[i, 'ID'] = genename
        data.loc[i, 'CATEGORY'] = content
        data.loc[i, 'GENE_FOUND'] = gene_found
        data.loc[i, 'CONTENT_FOUND'] = content_found

    outdata_df = data[['ID','CATEGORY','GENE_FOUND','CONTENT_FOUND']]
    
    outdata_df.to_csv(outputfile, index=False) 
    
    outdata_df.head().to_csv(addtag(outputfile, 'SMALL_', prefix=True), \
        index=False)


