from pdb import set_trace
from sbie_optdrug.dataset import ccle 
import re 
import os
# from sets import Set
import pickle

output = 'mut_list.p'

if not os.path.exists(output):
    mutcna = ccle.mutcna()
    mutcna_names = mutcna.index.values.tolist()
    mut_list = []
    for name in mutcna_names:
        if re.search('.+_MUT$', name):
            mut_list.append( name.replace('_MUT', '') ) 

    mut_set = set(mut_list)
    mut_list = [m for m in mut_set]
    pickle.dump(mut_list, open(output,'w'))

else: 
    mut_list = pickle.load(open(output, 'r'))

for mut in mut_list[0:5]:
    os.system('phantomjs binfo.js %s' % mut)

# gene_name, html_name, class
# APC, APC.html, TSG or Oncogene

