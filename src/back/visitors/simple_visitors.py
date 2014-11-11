'''
Created on Nov 3, 2014

@author: ezulkosk
'''
import sys

import z3

from back.operations.blasted_ops import Eager, Lazy
from back.visitors import VisitorTemplate
from back.visitors.Visitor import visit, retvisit
from structures.logic import BoolConst


class MapVars(VisitorTemplate.VisitorTemplate):
    '''
    Map any IDs in args to the correct SAGE entities,
    and create a mapping from ops to booleans.
    '''

    def __init__(self, program, solver, options):
        self.program = program
        self.options = options
        self.solver = solver

    def baseoperationVisit(self, baseop):
        baseop.args = baseop.map_vars(self.program)
        

class T2B(VisitorTemplate.VisitorTemplate):
    '''
    Map any IDs in args to the correct SAGE entities,
    and create a mapping from ops to booleans.
    '''

    def __init__(self, program, solver, options):
        self.program = program
        self.options = options
        self.solver = solver

    def baseoperationVisit(self, baseop):
        if isinstance(baseop.op, Lazy):
            baseop.dimacs_var = self.solver.t2b(baseop)
    
        
class DumpBooleanAbstraction(VisitorTemplate.ReturnVisitorTemplate):

    def __init__(self, program, solver, options):
        self.program = program
        self.options = options
        self.solver = solver
    
    
    def parse_z3_expr(self, c):
        if str(c.decl()) == "Not":
            return -int(self.parse_z3_expr(c.children()[0]))
        elif str(c.decl()) == "Or":
            return [self.parse_z3_expr(i) for i in c.children()]
        else:
            #print(c)
            #print(isinstance(c, int))
            if str(c).startswith("k!"):
                if not self.solver.get_dimacs_for_bool(str(c)):
                    self.solver.add_bool(str(c))
                c = self.solver.get_dimacs_for_bool(str(c))
            if str(c).startswith("bool!"):
                i = str(c).split("bool!")[1]
                return int(i)        
            return int(str(c))
    
    def parse_Z3_tseitin(self, cnf):
        clauses = []
        for c in cnf:
            res = self.parse_z3_expr(c)
            if isinstance(res, int):
                res = [res]
            clauses.append(tuple(res))
        return clauses
            
    
    def programVisit(self, program):
        res = []
        for i in program.ast:
            val = retvisit(self, i)
            if val:
                res.append(val)
        expr = z3.And(res)
        goal = z3.Goal()
        goal.add(expr)
        tactic = z3.Tactic("tseitin-cnf")
        prog = tactic(goal)[0]
        return self.parse_Z3_tseitin(prog)
    
    def boolVisit(self, b):
        return None
    
    def basegraphVisit(self, g):
        return None

    def sagegraphVisit(self, g):
        return None
    
    def assertVisit(self, a):
        return retvisit(self, a.expr)
    
    def opVisit(self, op):
        name = op.ID.ID
        res = []
        for i in op.args:
            res.append(retvisit(self, i))
        if name == "and":
            return z3.And(res)
        elif name == "or":
            return z3.Or(res)
        elif name == "not":
            return z3.Not(res[0])
    
    def baseoperationVisit(self, baseop):
        #TODO should go deeper.
        if isinstance(baseop.op, Lazy):
            return z3.Bool(baseop.dimacs_var)
        else:
            #print(baseop.args)
            res = []
            blasted = baseop.op.apply(self.solver, *baseop.args)
            #print(blasted)
            flag = False
            for arg in blasted:
                subres = []
                for subarg in arg:
                    if isinstance(subarg, BoolConst):
                        if subarg.val:
                            flag = True
                            break
                        else:
                            continue
                    if subarg < 0:
                        subres.append(z3.Not(z3.Bool(str(-subarg))))
                    else:
                        subres.append(z3.Bool(str(subarg)))
                if flag:
                    flag = False
                    continue
                res.append(z3.Or(subres))
            #print(res)
            return z3.And(res)
    
    def idVisit(self, element):
        v = self.solver.get_dimacs_for_bool(self.program.bools[element.ID])
        return z3.Bool("bool!" + str(v))
    
class BlastOps(VisitorTemplate.VisitorTemplate):

    def __init__(self, program, solver, options):
        self.program = program
        self.options = options
        self.solver = solver
    
    def baseoperationVisit(self, baseop):
        #TODO need to be in CNF
        clauses = baseop.op(self.solver, *baseop.args)
        self.solver.add_clauses(clauses)
