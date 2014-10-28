'''
Created on Mar 26, 2013

@author: ezulkosk
'''
import structures
from structures.logic import ID


def visit(visitor, element):
    '''
    Method used to determine which visit method to call, based on the type of element.
    
    :param element: A Clafer AST node.
    :type element: ast.* 
    
    *see* :doc:`ast`
    '''
    if isinstance(element, structures.program.Program):
        visitor.programVisit(element)
    elif isinstance(element, structures.logic.Bool):
        visitor.boolVisit(element)
    elif isinstance(element, structures.graph.BaseGraph):
        visitor.basegraphVisit(element)
    elif isinstance(element, structures.graph.SageGraph):
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
    