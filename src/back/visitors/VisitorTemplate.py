'''
Created on Mar 26, 2013

@author: ezulkosk
'''
import sys

import back.visitors.Visitor


class VisitorTemplate(object):
    '''
    *see:* :class:`visitors.Visitor`
    
    Visitor that simply traverses the Clafer AST, 
    used as a superclass for other visitors
    '''
    def __init__(self):
        pass
    
    def programVisit(self, program):
        for i in program.ast:
            back.visitors.Visitor.visit(self, i)
    
    def boolVisit(self, b):
        pass
    
    def basegraphVisit(self, g):
        pass

    def sagegraphVisit(self, g):
        pass
    
    def assertVisit(self, a):
        back.visitors.Visitor.visit(self, a.expr)
    
    def opVisit(self, op):
        for i in op.args:
            back.visitors.Visitor.visit(self, i)
    
    def baseoperationVisit(self, baseop):
        pass
    
    def idVisit(self, element):
        pass
    