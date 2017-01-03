# <<<<<<< HEAD
from ipdb import set_trace
from sbie_optdrug.result import tab_s7
from sbie_optdrug.result import tab_s11
from os.path import exists
import json
import pandas as pd
from termutil import progressbar

def test_table_ab(force):

    output_a = tab_s11.get_config()['output']['a']
    output_b = tab_s11.get_config()['output']['b']

    if exists(output_b) and force == False:
        return

    with open(tab_s7.get_config()['output']['c'], 'r') as fin:
        data1 = json.load(fin)

    with open(tab_s7.get_config()['output']['d'], 'r') as fin:
        data2 = json.load(fin)

    data1['configs'] = data1['configs'][0:100]
    data2['scanning_results'] = data2['scanning_results'][0:100]

    with open(output_a, 'w') as fout:
        json.dump(data1, fout, indent=1)

    with open(output_b, 'w') as fout:
        json.dump(data2, fout, indent=1)


def test_table_c(with_small, force):

    output_c = tab_s11.get_config()['output']['c']

    if exists(output_c) and force == False:
        return

    if with_small:
        with open(tab_s11.get_config()['output']['a'], 'r') as fin:
            data1 = json.load(fin)
        with open(tab_s11.get_config()['output']['b'], 'r') as fin:
            data2 = json.load(fin)
    else:
        with open(tab_s7.get_config()['output']['c'], 'r') as fin:
            data1 = json.load(fin)
        with open(tab_s7.get_config()['output']['d'], 'r') as fin:
            data2 = json.load(fin)

    all_dict = {}

    df0 = pd.DataFrame(index=range(0,len(all_dict)),
        columns=['S%d'%i for i in range(96)])

    for i,res in enumerate(data2['scanning_results']):
        progressbar.update(i, len(data2['scanning_results']))
        this_dict = res['state_key']
        all_dict.update(this_dict)

    for i,k in enumerate(all_dict):
        progressbar.update(i, len(all_dict))
        v = all_dict[k]
        df0.loc[i] = [w for w in v]

    df0.to_csv(output_c, index=False)

# =======
import pandas as pd
from ipdb import set_trace

def test_1():

	HALLMARK_APOPTOSIS = 'dataset/MSigDB/HALLMARK_APOPTOSIS.txt'
	HALLMARK_E2F_TARGETS = 'dataset/MSigDB/HALLMARK_E2F_TARGETS.txt'
	HALLMARK_G2M_CHECKPOINT = 'dataset/MSigDB/HALLMARK_G2M_CHECKPOINT.txt'
	HALLMARK_MITOTIC_SPINDLE = 'dataset/MSigDB/HALLMARK_MITOTIC_SPINDLE.txt'
	HALLMARK_MYC_TARGETS_V1 = 'dataset/MSigDB/HALLMARK_MYC_TARGETS_V1.txt'
	HALLMARK_MYC_TARGETS_V2 = 'dataset/MSigDB/HALLMARK_MYC_TARGETS_V2.txt'
	HALLMARK_P53_PATHWAY = 'dataset/MSigDB/HALLMARK_P53_PATHWAY.txt'

	fumia_node_list = 'dataset/fumia-node-list.txt'

	df_apo = pd.read_csv(HALLMARK_APOPTOSIS, skiprows=[1])
	df_ef2 = pd.read_csv(HALLMARK_E2F_TARGETS, skiprows=[1])
	df_g2m = pd.read_csv(HALLMARK_G2M_CHECKPOINT, skiprows=[1])
	df_mit = pd.read_csv(HALLMARK_MITOTIC_SPINDLE, skiprows=[1])
	df_myc1 = pd.read_csv(HALLMARK_MYC_TARGETS_V1, skiprows=[1])
	df_myc2 = pd.read_csv(HALLMARK_MYC_TARGETS_V2, skiprows=[1])
	df_p53 = pd.read_csv(HALLMARK_P53_PATHWAY, skiprows=[1])

	hallmarks = set()

	hallmarks= hallmarks.union( set(df_apo['HALLMARK_APOPTOSIS'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_ef2['HALLMARK_E2F_TARGETS'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_g2m['HALLMARK_G2M_CHECKPOINT'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_mit['HALLMARK_MITOTIC_SPINDLE'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_myc1['HALLMARK_MYC_TARGETS_V1'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_myc2['HALLMARK_MYC_TARGETS_V2'].values.tolist()) )
	hallmarks= hallmarks.union( set(df_p53['HALLMARK_P53_PATHWAY'].values.tolist()) )

	df_fumia = pd.read_csv(fumia_node_list, names=['fumia_node'])
	fumia_nodes = set(df_fumia['fumia_node'].values.tolist())

	print('hallmarks: ', len(hallmarks))
	print('fumia_nodes: ', len(fumia_nodes))
	print('intersection: ', len(fumia_nodes.intersection(hallmarks)))

	set_trace()

# >>>>>>> 9414ef959c8fdfc1068d7672110e3178d9e7a385
