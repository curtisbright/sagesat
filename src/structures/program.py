'''
Created on Oct 17, 2014

@author: ezulkosk
'''

class Program(object):
    '''
    classdocs
    '''


    def __init__(self, ast):
        '''
        Constructors
        '''
        self.ast = ast
        self.bools = { }
        self.graphs = { }
        
    def toStr(self, indent):
        res = "Program\n"
        for i in self.ast:
            res += i.toStr(1) + "\n"
        return res