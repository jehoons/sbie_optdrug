from os.path import exists
from sbie_optdrug.result.tab_s1 import program
from pdb import set_trace
import numpy 


def test():
    
    config = program.getconfig()

    exist_list = [exists(config[output]) for output in \
        ['output_a','output_b','output_c','output_d']]

    if not numpy.product(exist_list):
        program.run(config)

    assert numpy.product(exist_list)


