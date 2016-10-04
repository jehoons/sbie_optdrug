# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from sbie_optdrug import filelist 
from pdb import set_trace
from os.path import join, exists, split
import pytest
import pandas as pd
import tempfile
import json
import pickle
import re
from sbie_optdrug import util
import glob
import os
import shutil


def gex(force=False):
	print '- processing gene expression data ...'

	if exists(filelist.processed_ccle_gex) and force==False:
		return

	df_gex = pd.read_csv(filelist.ccle_gex, sep='\t', skiprows=2)
	idx_filt = [idx.find('AFFX') != 0 for idx in df_gex['Name'].values]
	df_gex = df_gex.loc[idx_filt]
	df_gex.set_index('Name')
	pickle.dump(df_gex, open(filelist.processed_ccle_gex, "wb" ))


def mutcna(force=False):
	print '- processing mutation and CNA data ...'

	if exists(filelist.processed_ccle_mutcna_dense) and force==False:
		return

	df0 = pd.read_csv(filelist.ccle_mutcna, sep='\t', skiprows=2, index_col='Name')
	df0.set_index('Description', inplace=True)
	pickle.dump(df0, open(filelist.processed_ccle_mutcna, "wb" ))
	idx_mut = [re.match('.+_MUT$', idx) != None for idx in df0.index]
	idx_amp = [re.match('.+_AMP$', idx) != None for idx in df0.index]
	idx_del = [re.match('.+_DEL$', idx) != None for idx in df0.index]

	df_mut = df0.loc[idx_mut].copy()
	df_amp = df0.loc[idx_amp].copy()
	df_del = df0.loc[idx_del].copy()

	new_idx_mut = [idx.replace('_MUT', '') for idx in df_mut.index]
	new_idx_amp = [idx.replace('_AMP', '') for idx in df_amp.index]
	new_idx_del = [idx.replace('_DEL', '') for idx in df_del.index]
	df_mut['index'] = new_idx_mut
	df_amp['index'] = new_idx_amp
	df_del['index'] = new_idx_del
	df_mut.set_index('index', inplace=True)
	df_amp.set_index('index', inplace=True)
	df_del.set_index('index', inplace=True)
	pickle.dump(df_mut, open(filelist.processed_ccle_mutcna_mut, "wb" ))
	pickle.dump(df_amp, open(filelist.processed_ccle_mutcna_amp, "wb" ))
	pickle.dump(df_del, open(filelist.processed_ccle_mutcna_del, "wb" ))
	ccle_mutcna_dense = {}
	for i, cell in enumerate(df0.columns):
		util.update_progress(i, df0.shape[1])
		celldata = df0[cell]
		dic = {'MUT': [], 'DEL': [], 'AMP': []}
		ifilt = celldata[celldata==1].index
		for d in ifilt:
			if re.match('.+_MUT$', d) != None :
				dic['MUT'].append(d.replace('_MUT', ''))
			elif re.match('.+_DEL$', d) != None :
				dic['DEL'].append(d.replace('_DEL', ''))
			elif re.match('.+_AMP$', d) != None :
				dic['AMP'].append(d.replace('_AMP', ''))

		ccle_mutcna_dense[cell] = dic

	with open(filelist.processed_ccle_mutcna_dense, 'w') as outfile:
		json.dump(ccle_mutcna_dense, outfile, indent=4, sort_keys=True,
			separators=(',', ':'))


def sampleinfo(force=False):
	print '- processing sample information data ...'

	if exists(filelist.processed_ccle_sampleinfo) and force==False:
		return

	df0 = pd.read_csv(filelist.ccle_sampleinfo, sep='\t', index_col='CCLE name')
	pickle.dump(df0, open(filelist.processed_ccle_sampleinfo, "wb" ))


def therapy(force=False):
	print '- processing therapy data ...'

	if exists(filelist.processed_ccle_therapy) and force==False:
		return

	df0 = pd.read_csv(filelist.ccle_therapy, sep=',')
	pickle.dump(df0, open(filelist.processed_ccle_therapy, "wb" ))


def drug(force=False):
	print '- processing drug data ...'

	if exists(filelist.processed_ccle_druginfo) and force==False:
		return

	files = glob.glob(join(filelist.ccle_drug_dir, '*.csv'))
	sdf_data = {}
	for i, file in enumerate(files):
		util.update_progress(i, len(files))
		df0 = pd.read_csv(file)
		idx = os.path.split(file)[1].split('.')[0]
		sdf_dir = join(filelist.ccle_drug_dir, 'structure', idx)
		sdf_files = glob.glob(sdf_dir+'/*.sdf')

		sdf_files_list = []
		for sdf in sdf_files:
			if simple_check_sdf(sdf):
				sdf_files_list.append(sdf)

		sdf_data[idx] = {
			'structure': sdf_files_list,
			'info': df0.loc[0].to_dict()
			}

		for src in sdf_files_list:
			dst = join(filelist.dir_material, 'processed', 'drug',
				idx+'_'+split(src)[1])
			shutil.copyfile(src, dst)

	with open(filelist.processed_ccle_druginfo, 'wb') as outfile:
		json.dump(sdf_data, outfile, indent=4, sort_keys=True,
			separators=(',', ':'))


def simple_check_sdf(filename):
	lines = file(filename).readlines()
	res = False
	for line in lines:
		if line.find('$$$$') >= 0:
			res = True
			break

	return res
