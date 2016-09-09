# -*- coding: utf-8 -*-
#!/usr/bin/python
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

""" This module should be executed from python 3.5 
This module changes 'z = sign(x+y-1)' to logical equation. """

import re
import itertools
from pyeda.inter import *
from pdb import set_trace
from sympy import And, Or, Not, symbols
from sbie_optdrug.model.published import fumia_network


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
        # now we are ready to run the rule with sympy
        y = eval(rule)
        output_list.append(str(y))
        # set_trace()

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

        return boolvalue, boolvalue, variables, None, None 

    output_list = compute_truth_table(rule, tt, variables)

    tt_f = truthtable(ttvars('x', len(variables)), "".join(output_list))
    f_minimized = espresso_tts(tt_f)

    str_f_min = repr(f_minimized[0])
    for i in range(len(variables)): 
        str_f_min = str_f_min.replace('x[%d]'%(len(variables)-1-i), \
            variables[i])

    for var in variables:
        cmd = '%s = symbols(\'%s\')' % (var, var)
        exec(cmd)
        
    from sympy import And, Or, Not, Xor, printing 
    cstr = repr( eval('printing.ccode(%s)' % str_f_min) )
    cstr = cstr.replace('&&', 'and')
    cstr = cstr.replace('||', 'or')
    cstr = cstr.replace('!', 'not ')
    cstr = cstr.replace('\'', '')
    
    return rule, cstr, variables, tt, output_list


def run(txtdata, short=False):
    eq_lines = txtdata.split('\n')
    for k, eq in enumerate(eq_lines): 
        eq = eq.strip()
        if eq == '':
            continue

        words = eq.split('=')
        res0, res1, varlist, tt, y = engine_rule2logic(words[1])
        
        if short == False: 
            print ('source: ', words[0], '*=', res0)
            print ('input:', varlist)
            print ('output:', words[0])
            print ('table:')
            if tt != None: 
                for j, row in enumerate(tt):
                    print(row, y[j])
            else:  
                print ('N/A')

            print ('target:', words[0], '*=', res1)
            print ('')

        else: 
            print (words[0], '*=', res1)

            