# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from os.path import join, split, abspath, dirname, exists
import sbie_optdrug

# directory for source and processed datasets.

dir_material = abspath(dirname(sbie_optdrug.__file__)+'/dataset/material')

# if not exists(dir_material):
#     print('missing directory:', dir_material)
#     print('material should be provided to program.')
#     assert False

# ccle source data:
ccle_gex = join(dir_material,
    'CCLE', 'gene_expression', 'CCLE_Expression_Entrez_2012-09-29.gct')

ccle_mutcna = join(dir_material,
    'CCLE', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct')

ccle_sampleinfo = join(dir_material,
    'CCLE', 'CCLE_sample_info_file_2012-10-18.txt')

ccle_therapy = join(dir_material,
    'CCLE', 'CCLE_NP24.2009_Drug_data_2015.02.24.csv')

ccle_drug_dir = join(dir_material,
    'CCLE', 'additional', 'drug_info')

# ccle processed data:
processed_ccle_gex = join(dir_material,
    'processed', 'CCLE_Expression_Entrez_2012-09-29.processed.p')

processed_ccle_mutcna = join(dir_material,
    'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.processed.p')

processed_ccle_mutcna_dense = join(dir_material,
    'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.processed.dense.json')

processed_ccle_mutcna_mut = join(dir_material,
    'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.mut.processed.p')

processed_ccle_mutcna_amp = join(dir_material,
    'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.amp.processed.p')

processed_ccle_mutcna_del = join(dir_material,
    'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.del.processed.p')

processed_ccle_sampleinfo = join(dir_material,
    'processed', 'CCLE_sample_info_file_2012-10-18.processed.p')

processed_ccle_therapy = join(dir_material,
    'processed', 'CCLE_NP24.2009_Drug_data_2015.02.24.processed.p')

processed_ccle_druginfo = join(dir_material,
    'processed', 'ccle_drug_info.processed.json')

gdsc_v50 = { }

gdsc_v50['raw'] = { }

gdsc_v50['raw']['expU133A'] = join(dir_material, 'GDSC','release-5.0',
    'expU133A.txt.zip')
gdsc_v50['raw']['gdsc_cell_lines_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_cell_lines_w5.csv')
gdsc_v50['raw']['gdsc_compounds_conc_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_compounds_conc_w5.csv')
gdsc_v50['raw']['gdsc_drug_sensitivity_fitted_data_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_drug_sensitivity_fitted_data_w5.csv')
gdsc_v50['raw']['gdsc_drug_sensitivity_raw_data_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_drug_sensitivity_raw_data_w5.csv')
gdsc_v50['raw']['gdsc_en_input_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_en_input_w5.csv')
gdsc_v50['raw']['gdsc_en_output_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_en_output_w5.csv')
gdsc_v50['raw']['gdsc_manova_input_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_manova_input_w5.csv')
gdsc_v50['raw']['gdsc_manova_output_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_manova_output_w5.csv')
gdsc_v50['raw']['gdsc_mutation_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_mutation_w5.csv')
gdsc_v50['raw']['gdsc_tissue_output_w5'] = join(dir_material, 'GDSC','release-5.0',
    'gdsc_tissue_output_w5.csv')
