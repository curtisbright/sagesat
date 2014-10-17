'''
Created on Oct 17, 2014

@author: ezulkosk
'''
from structures.exceptions import NameNotFoundException, TypeException
from structures.graph import BaseGraph
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
        #print(line)
        if isinstance(line, Assert):
            expr_type = resolve_expr(program, line.expr)
            assert(is_bool(expr_type))
        elif isinstance(line, Bool):
            program.bools[line.ID] = line
        elif isinstance(line, BaseGraph):
            program.graphs[line.ID] = line

def resolve_expr(program, expr):
    try:
        if expr.name == "and":
            return resolve_and(program, expr.args[0], expr.args[1])
        elif expr.name == "or":
            return resolve_or(program,expr.args[0], expr.args[1])
        elif expr.name == "not":
            return resolve_not(program, expr.args[1])
        else:
            #defined operation
            return resolve_operation(program, expr)
    except AttributeError:
        #id lookup
        if expr in program.bools:
            return BoolType()
        elif expr in program.graphs:
            return GraphType()
        else:
            raise NameNotFoundException(str(expr))
            
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
    print("TODO: ops should be checked")
    return BoolType()

def skip(l):
    pass