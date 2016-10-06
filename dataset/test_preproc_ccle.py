# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from sbie_optdrug.dataset import preproc_ccle

def test_main(with_small, force):

    preproc_ccle.gex(force=force)

    preproc_ccle.mutcna(force=force)

    preproc_ccle.sampleinfo(force=force)

    preproc_ccle.therapy(force=force)

    # there's json writing bug in preproc_ccle module 
    # preproc_ccle.drug(force=True)
