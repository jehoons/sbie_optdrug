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
