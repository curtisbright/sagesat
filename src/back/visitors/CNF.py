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
        #TODO need to be in CNF
        args = baseop.map_vars(self.program)
        clauses = baseop.op(self.solver, *args)
        #print(clauses)
        self.solver.add_clauses(clauses)
        #print(self.solver.clauses)
    
    def idVisit(self, element):
        return element
    
    