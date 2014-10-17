'''
Created on Oct 17, 2014

@author: ezulkosk
'''

def instantiate_vars(program, options):
    #bools do not need further instantiation
    for g in program.graphs.values():
        g.instantiate(options)