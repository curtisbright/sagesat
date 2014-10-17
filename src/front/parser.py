'''
Created on Oct 15, 2014

@author: ezulkosk
'''

from front.lexer import tokens
from structures import logic
from structures.exceptions import ParserException
from structures.graph import BaseGraph
from structures.logic import Bool, Assert
from structures.operation import BaseOperation


precedence = (
    ('right', 'AND', 'OR'),

)

def p_program(t):
    '''
    program : program vardecl 
            | program assertdecl 
            | vardecl
            | assertdecl
    '''
    if len(t) == 3:
        t[0] = t[1] + t[2]
    else:
        t[0] = t[1]

def p_vardecl(t):
    '''
    vardecl : boolvardecl
            | graphvardecl
    '''
    t[0] = t[1]

def p_boolvardecl(t):
    'boolvardecl : BOOL ID'
    t[0] = [Bool(t[2], t.lineno)]
    #bools[t[2]] = "bool"
    
def p_graphvardecl(t):
    'graphvardecl : GRAPH ID LPAREN NUMBER optgraphrange RPAREN graphdef'
    t[0] = [BaseGraph(t[2], t[4], t[5], t[7], t.lineno)]
    #graphs[t[2]] = (t[4], t[5], t[7])
    
def p_optgraphrange(t):
    '''
    optgraphrange : COLON NUMBER
                  | empty
    '''
    if len(t) == 3:
        t[0] = t[2]
    else:
        t[0] = None

def p_graphdef(t):
    '''
    graphdef : EQUALS LBRACKET exprlist RBRACKET
             | empty 
    '''
    if len(t) == 5:
        t[0] = t[3]
    else:
        t[0] = None
    
def p_exprlist(t):
    '''
    exprlist : expr nonemptylist
            | empty 
    '''
    if len(t) == 3:
        t[2].insert(0, t[1])
        t[0] = t[2]
    elif len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = []

def p_nonemptylist(t):
    '''
    nonemptylist : COMMA expr nonemptylist 
                 | empty 
    '''
    if len(t) == 4:
        t[3].insert(0, t[2])
        t[0] = t[3]
    else:
        t[0] = []

    
def p_assertdecl(t):
    'assertdecl : ASSERT expr'
    t[0] = [Assert(t[2], t.lineno)]

def p_operation(t):
    'operation : ID LPAREN exprlist RPAREN'
    t[0] = BaseOperation(t[1], t[3], t.lineno)

def p_expression(t):
    '''
    expr : expr AND expr
         | expr OR expr
         | NOT expr
         | operation
         | ID
         | NUMBER
    '''
    if len(t) == 4:
        if t[2] == '|'  : t[0] = logic.Op('or', [t[1], t[3]], t.lineno)
        elif t[2] == '&': t[0] = logic.Op('and', [t[1], t[3]], t.lineno)
    elif len(t) == 3:
        t[0] = logic.Op('not', t[2], t.lineno)
    else:
        t[0] = t[1]
    
    
def p_expression_group(t):
    'expr : LPAREN expr RPAREN'
    t[0] = t[2]


'''
def p_expression_name(t):
    'expr : ID'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0
'''
 
def p_empty(p):
    'empty :'
    pass

def p_error(t):
    raise ParserException("syntax error at '" + str(t.value) + ".", t.lineno)
