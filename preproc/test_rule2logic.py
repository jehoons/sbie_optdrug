# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

import re 
from sbie_optdrug.preproc import rule2logic
from sbie_optdrug.model.published import fumia_network


def test_this():

    txtdata = re.sub('%.*\n', '\n', fumia_network.get_txtdata())
    txtdata = re.sub('[ ;]', '', txtdata)
    txtdata = txtdata.replace('(t)', '')
    txtdata = txtdata.replace('(t+1)', '')

    res = rule2logic.run(txtdata)

    print(res)

    assert True
