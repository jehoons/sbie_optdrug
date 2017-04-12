# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

""" This module should be executed from python 3.5 
This module changes 'z = sign(x+y-1)' to logical equation. """

import re
import sys
import itertools
from pyeda.inter import *
from ipdb import set_trace
from sympy import And, Or, Not, symbols


def get_variables(rule): 
    found = re.findall('[A-Za-z_][_A-Za-z0-9]+', rule)
    variables = [] 
    for v in found:
        if v not in ['sgn_th']: 
            variables.append(v)

    return variables


def compute_truth_table(rule, tt, variables):
    def sgn_th(x):
        if x > 0:
            return 1
        else: 
            return 0

    output_list = [] 
    for var_assignment in tt: 
        expression = repr(tuple(variables)).replace('\'', '') + '=' + \
            repr(var_assignment)
        exec(expression)
        y = eval(rule)
        output_list.append(str(y))

    return output_list


def engine_rule2logic(rule):
    variables = get_variables(rule)
    tt = [i for i in itertools.product([0,1], repeat=len(variables))]

    if variables == []:
        if rule == '1':
            boolvalue = 'True'
        elif rule == '0': 
            boolvalue = 'False'
        else: 
            assert False 

        return boolvalue, boolvalue, variables, None, None, boolvalue

    output_list = compute_truth_table(rule, tt, variables)

    tt_f = truthtable(ttvars('x', len(variables)), "".join(output_list))

    sop = [] 
    for i,output in enumerate(output_list):
        if output == '1': 
            args = tt[i]
            lbls = []
            for i,arg in enumerate(args):
                if arg == 1:
                    lbls.append(variables[i])
                else: 
                    lbls.append('not ' + variables[i])

            sop.append(" and ".join(lbls))

    # print ( 'sop: ' + repr(sop))
    sop_eqns = " or ".join(sop)

    # set_trace();

    f_minimized = espresso_tts(tt_f)
    str_f_min = repr(f_minimized[0])
    for i in range(len(variables)): 
        str_f_min = str_f_min.replace('x[%d]'%(len(variables)-1-i), \
            variables[i])

    for var in variables:
        cmd = '%s = symbols(\'%s\')' % (var, var)
        exec(cmd)
        
    from sympy import And, Or, Not, Xor, printing 

    # if len(variables) > 4: 
    #     set_trace()

    cstr = repr( eval('printing.ccode(%s)' % str_f_min) )
    cstr = cstr.replace('&&', 'and')
    cstr = cstr.replace('||', 'or')
    cstr = cstr.replace('!', 'not ')
    cstr = cstr.replace('\'', '')
    
    return rule, cstr, variables, tt, output_list, sop_eqns


def run(txtdata, short=False):
    eq_lines = txtdata.split('\n')
    output_str = '' 
    for k, eq in enumerate(eq_lines): 
        eq = eq.strip()
        if eq == '':
            continue

        words = eq.split('=')
        res0, res1, varlist, tt, y, sop_eqns = engine_rule2logic(words[1])
        
        if short == False: 
            output_str += 'source: ' + words[0] + ' *= ' + res0 + '\n'
            output_str += 'input: ' + ",".join(varlist) + '\n'
            output_str += 'output: ' + words[0] + '\n'
            output_str += 'table: ' + '\n'

            if tt != None: 
                for j, row in enumerate(tt):
                    lhs_ = ",".join( ['%d' % r for r in row] )
                    output_str += lhs_ + ' | ' + str(y[j]) + '\n'

            else:  
                output_str += 'N/A' + '\n'

            output_str += 'target: ' + words[0] + ' *= ' + res1 + '\n'
            output_str += 'before: ' + words[0] + ' *= ' + sop_eqns + '\n\n'

        else: 
            output_str += words[0] + ' *= ' + res1 + '\n'

    return output_str

    
if __name__ == '__main__': 

    argv = sys.argv[1:]

    infile_txt = argv[0]

    with open(infile_txt, 'r') as fin: 
        txtdata = "\n".join(fin.readlines())

    res = run(txtdata, short=False)

    print (res)

    assert True

