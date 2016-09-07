from os.path import join, split, abspath
from pdb import set_trace

# directory for source and processed datasets. 

# dir_material = '/home/pbs/proj/het/material'
dir_material = join(split(__file__)[0], '..', 'material')

dir_material = abspath(dir_material)

# ccle source data: 
ccle_gex = join(dir_material, 'CCLE', 'gene_expression', 'CCLE_Expression_Entrez_2012-09-29.gct')

ccle_mutcna = join(dir_material, 'CCLE', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct') 

ccle_sampleinfo = join(dir_material, 'CCLE', 'CCLE_sample_info_file_2012-10-18.txt') 

ccle_therapy = join(dir_material, 'CCLE', 'CCLE_NP24.2009_Drug_data_2015.02.24.csv')

ccle_drug_dir = join(dir_material, 'CCLE', 'additional', 'drug_info')

# ccle processed data: 
processed_ccle_gex = join(dir_material, 'processed', 'CCLE_Expression_Entrez_2012-09-29.processed.p')

processed_ccle_mutcna = join(dir_material, 'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.processed.p') 

processed_ccle_mutcna_dense = join(dir_material, 'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.processed.dense.json') 

processed_ccle_mutcna_mut = join(dir_material, 'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.mut.processed.p') 

processed_ccle_mutcna_amp = join(dir_material, 'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.amp.processed.p') 

processed_ccle_mutcna_del = join(dir_material, 'processed', 'CCLE_MUT_CNA_AMP_DEL_binary_Revealer.del.processed.p') 

processed_ccle_sampleinfo = join(dir_material, 'processed', 'CCLE_sample_info_file_2012-10-18.processed.p') 

processed_ccle_therapy = join(dir_material, 'processed', 'CCLE_NP24.2009_Drug_data_2015.02.24.processed.p')

processed_ccle_druginfo = join(dir_material, 'processed', 'ccle_drug_info.processed.json')

