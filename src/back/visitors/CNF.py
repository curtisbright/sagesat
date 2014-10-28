'''
Created on Oct 24, 2014

@author: ezulkosk
'''
from back.visitors import VisitorTemplate
import back.visitors


class CNF(VisitorTemplate.VisitorTemplate):

    def __init__(self, program, solver, options):
        self.program = program
        self.options = options
        self.solver = solver

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
        args = baseop.map_vars(self.program)
        print(baseop.op(self.solver, *args))
    
    def idVisit(self, element):
        return element
    
    