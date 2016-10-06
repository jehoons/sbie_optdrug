# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import pickle
from sbie_optdrug.dataset import filelist
from pdb import set_trace
import json
import pandas as pd


def gex():

	return pickle.load(open(filelist.processed_ccle_gex, 'rb'))


def mutcna():

	return pickle.load(open(filelist.processed_ccle_mutcna, 'rb'))


def mutcna_dense():

	return json.load(open(filelist.processed_ccle_mutcna_dense, 'rb'))


def mutcna_seperately():

    # mutcna_mut - get only mutation
    # mutcna_amp - get only CNV with amplification
    # mutcna_del - get only CNV with deletion
	return pickle.load(open(filelist.processed_ccle_mutcna_mut, 'rb')), \
		pickle.load(open(filelist.processed_ccle_mutcna_amp, 'rb')), \
		pickle.load(open(filelist.processed_ccle_mutcna_del, 'rb'))


def sampleinfo():

	return pickle.load(open(filelist.processed_ccle_sampleinfo, "rb" ))


def therapy():

	return pickle.load(open(filelist.processed_ccle_therapy, "rb" ))


def check_intestine_cells():

    sample_data = sampleinfo()
    therapy_data = therapy()

    idx = (sample_data['Site Primary']=='large_intestine') | \
        (sample_data['Site Primary']=='small_intestine')

    intestine = sample_data[idx].index.tolist()

    index_list = []
    count = 0
    for i in therapy_data.index:
        cell = therapy_data['CCLE Cell Line Name'].loc[i]
        if cell in intestine:
            count += 1
            index_list.append(i)

    drug_list = set(therapy_data['Compound'].loc[index_list])

    print ('# experiments:', count)
    print ('# cells:', len(intestine))
    print ('# drugs:', len(drug_list))
