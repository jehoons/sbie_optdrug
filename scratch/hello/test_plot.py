# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from pdb import set_trace
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from os.path import exists


def test_hist2d_plot():

    """ normal distribution center at x=0 and y=5 """

    x = np.random.randn(1000)
    y = np.random.randn(1000) + 5
    
    plt.hist2d(x, y, bins=40)
    
    plt.show()
    
    outputfile = 'test_plot_fig1.jpg'

    plt.savefig(outputfile)

    assert exists(outputfile)

