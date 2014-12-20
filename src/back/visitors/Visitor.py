'''
Created on Mar 26, 2013

@author: ezulkosk
'''
import z3

import structures
from structures.logic import ID, BoolConst


def visit(visitor, element):
    if isinstance(element, structures.program.Program):
        visitor.programVisit(element)
    elif isinstance(element, structures.logic.Bool):
        visitor.boolVisit(element)
    elif isinstance(element, structures.graphs.graph.BaseGraph):
        visitor.basegraphVisit(element)
    elif isinstance(element, structures.graphs.graph.CASGraph):
        visitor.sagegraphVisit(element)
    elif isinstance(element, structures.logic.Assert):
        visitor.assertVisit(element)
    elif isinstance(element, structures.logic.Op):
        visitor.opVisit(element)
    elif isinstance(element, structures.operation.BaseOperation):
        visitor.baseoperationVisit(element)
    elif isinstance(element, ID):
        visitor.idVisit(element)
    else:
        print("Error in visitor: " + str(element))
    
def retvisit(visitor, element):
    '''
    Method used to determine which visit method to call, based on the type of element.
    
    :param element: A Clafer AST node.
    :type element: ast.* 
    
    *see* :doc:`ast`
    '''
    if isinstance(element, structures.program.Program):
        return visitor.programVisit(element)
    elif isinstance(element, structures.logic.Bool):
        return visitor.boolVisit(element)
    elif isinstance(element, structures.graphs.graph.BaseGraph):
        return visitor.basegraphVisit(element)
    elif isinstance(element, structures.graphs.graph.CASGraph):
        return visitor.sagegraphVisit(element)
    elif isinstance(element, structures.logic.Assert):
        return visitor.assertVisit(element)
    elif isinstance(element, structures.logic.Op):
        return visitor.opVisit(element)
    elif isinstance(element, structures.operation.BaseOperation):
        return visitor.baseoperationVisit(element)
    elif isinstance(element, ID):
        return visitor.idVisit(element)
    elif isinstance(element, z3.BoolRef):
        #preconverted by blasted op
        return visitor.boolref_visit(element)
    elif isinstance(element, BoolConst):
        return visitor.boolconst_visit(element)
    elif isinstance(element, int):
        #preconverted by blasted op
        return visitor.blasted_int_visit(element)
    else:
        print("Error in visitor: " + str(element))
        print(element.__class__)