'''
Created on Oct 17, 2014

@author: ezulkosk
'''
from structures.exceptions import NameNotFoundException, TypeException
from structures.graph import BaseGraph, SageGraph
from structures.logic import Assert, Bool


class BoolType():
    def __str__(self):
        return "BoolType"

class GraphType():
    def __str__(self):
        return "GraphType" 

def is_bool(arg):
    return isinstance(arg, BoolType)

def resolve_and_type_check(program):
    for line in program.ast:
        if isinstance(line, Assert):
            expr_type = resolve_expr(program, line.expr)
            assert(is_bool(expr_type))
        elif isinstance(line, Bool):
            program.bools[line.ID.ID] = line
        elif isinstance(line, BaseGraph):
            program.graphs[line.ID.ID] = line
        elif isinstance(line, SageGraph):
            program.graphs[line.ID.ID] = line
        else:
            raise NameNotFoundException(str(line), line.line_number)

def resolve_expr(program, expr):
    try:
        if expr.ID == "and":
            return resolve_and(program, expr.args[0], expr.args[1])
        elif expr.ID == "or":
            return resolve_or(program,expr.args[0], expr.args[1])
        elif expr.ID == "not":
            return resolve_not(program, expr.args[1])
        else:
            #defined operation
            return resolve_operation(program, expr)
    except AttributeError:
        #id lookup
        if expr.ID in program.bools:
            return BoolType()
        elif expr.ID in program.graphs:
            return GraphType()
        else:
            raise NameNotFoundException(str(expr.ID), expr.ID.line_number)
            
def resolve_and(program, l,r):
    ltype = resolve_expr(program, l)
    rtype = resolve_expr(program, r)
    if not(is_bool(ltype) and is_bool(rtype)):
        raise TypeException("&", expected=(BoolType(), BoolType()), given=(ltype, rtype), line_number=l.line_number)
    return BoolType()

def resolve_or(program, l,r):
    ltype = resolve_expr(program, l)
    rtype = resolve_expr(program, r)
    if not(is_bool(ltype) and is_bool(rtype)):
        raise TypeException("|", expected=(BoolType(), BoolType()), given=(ltype, rtype), line_number=l.line_number)
    return BoolType()


def resolve_not(program, e):
    etype = resolve_expr(program, e)
    if not(is_bool(etype)):
        raise TypeException("!", expected=(BoolType()), given=(etype), line_number=e.line_number)
    return BoolType()

def resolve_operation(program, e):
    #print("TODO: ops should be checked")
    #All ops are predicates for now.
    return BoolType()

def skip(l):
    pass