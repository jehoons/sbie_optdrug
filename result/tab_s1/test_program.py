from os.path import exists
from sbie_optdrug.result.tab_s1 import program
from pdb import set_trace
import numpy


def test(with_small, force):

    config = program.getconfig()

    exist_list = [exists(config[output]) for output in \
        ['output_a','output_b','output_c','output_d','output_e']]

    if not numpy.product(exist_list) or force:
        program.run(config)
