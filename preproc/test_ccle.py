# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

from sbie_optdrug.preproc import ccle

def test_main(with_small, force):
    
    ccle.gex(force=force)
    
    ccle.mutcna(force=force)
    
    ccle.sampleinfo(force=force)
    
    ccle.therapy(force=force)
    
    ccle.drug(force=True)

  