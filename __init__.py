# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

__all__ = ['analysis', 'dataset', 'model', 'scratch', 'result']

from os.path import dirname,join 

root_dir = dirname(__file__)

module_dir = join(root_dir, 'module')

booleansim_dir = join(root_dir, 'module', 'BooleanSim')

import sys 

sys.path.append(module_dir)

sys.path.append(booleansim_dir) 

