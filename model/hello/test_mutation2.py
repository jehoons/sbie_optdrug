# -*- coding: utf-8 -*-
#*************************************************************************
# Author: {Je-Hoon Song, <song.je-hoon@kaist.ac.kr>
#
# This file is part of {sbie_optdrug}.
#*************************************************************************

# The collector helper function
#
# Asynchronous updating rules are non deterministic and
# need to be averaged over many runs
#
# The collector class makes this averaging very easy. It takes
# a list of states and nodes to build a data structure that 
# can compute the average the state of each node over all simulation and each timestep.
#
# The output of averaging (in the normalized mode) is a value between
# 0 and 1 representing the fraction of simulation (multiply by 100 to get percent) 
# that had the node in state True. 
#

from pdb import set_trace

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sbie_optdrug import boolean2
from sbie_optdrug.boolean2 import util
from sbie_optdrug.util import progressbar
import random


mutations = {
	'list': {
		'APC': {
			'function': 'LOF', 
	    	'intensity': 0.5
	    }, 
	    'CTNNB1': {
	    	'function': 'GOF',  
	    	'intensity': 1.0
	    }
	}, 
	'default_function': 'LOF'
}

# CNVs can be deinfed with similar manner. 

# drugs = [
#     {
#         'name': 'MEKi', 
#         'type': 'inhibitor',
#         # initial intensity  
#         'intensity': 0.0,
#         # mutations can be assumed as permanent change but drugs can not. 
#         # intensity of drug becomes 50% after its time_constant (unit is given as steps). 
#         'time_constant': 10 
#     }
# ]

drugs = {
	'list': {
		'MEKi': {
			'type': 'inhibitor', 
	    	'dose': 0.5, 
	    	'time_constant': 10
	    }, 
	},
}

# TODO
# build algorithm to simulate drugs and mutations. how? 
def rule_mutation( state, name, value, p ): 
	
	""" rule_mutation defines how mutation is appied into simulation. """
	
	global mutations 

    if name in mutations['list']:

	    given_function = mutations['list'][name]['function'] 

	    intensity = mutations[name]['intensity']

	    if given_function == 'UNKNOWN': 
	    	given_function = mutations['default_function']

        if given_function == 'LOF':
            if value == True: 
                if random.random() < intensity
                    value = False
        
        elif given_function == 'GOF': 
             if value == False: 
                if random.random() < intensity
                    value = True

    setattr( state, name, value )
    
    return value


# hello set_value 
# create a custom value setter
def set_value2( state, name, value, p ):

    "Custom value setter"
    
    value = rule_mutation(state, name, value, p)

    # this sets the attribute
    setattr( state, name, value )
    return value


# hello set_value 
# create a custom value setter
def set_value( state, name, value, p ):
    "Custom value setter"
    
    inhibitor_strength = 0.16
    # detect the node of interest
    if name == 'D':
        # print 'now setting node %s' % name 
        if value == True: 
            if random.random() < inhibitor_strength: 
                value = False

    # this sets the attribute
    setattr( state, name, value )
    return value


def test_main():
    text = """
    A = True
    B = Random
    C = Random
    D = Random

    B* = A or C
    C* = A and not D
    D* = B and C
    """

    repeat = 1000

    coll  = util.Collector()
    for i in range(repeat):
        progressbar.update(i, repeat)
        model = boolean2.Model( text, mode='async')
        model.parser.RULE_SETVALUE = set_value
        model.initialize()
        model.iterate( steps=30 )
        # in this case we take all nodes
        # one could just list a few nodes such as [ 'A', 'B', 'C' ]
        nodes = model.nodes
        # this collects states for each run
        coll.collect(states=model.states, nodes=nodes)

    # this step averages the values for each node
    # returns a dictionary keyed by nodes and a list of values
    # with the average state for in each timestep
    avgs = coll.get_averages( normalize=True )

    # make some shortcut to data to for easier plotting
    valueB = avgs["B"]
    valueC = avgs["C"]
    valueD = avgs["D"]

    p1, = plt.plot( valueB , 'ob-' )
    p2, = plt.plot( valueC , 'sr-' )
    p3, = plt.plot( valueD , '^g-' )
    plt.legend( [p1,p2,p3], ["B","C","D"])
    plt.show()
    plt.savefig('test_mutation_output.png')


