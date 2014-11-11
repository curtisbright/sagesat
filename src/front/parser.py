'''
Created on Oct 15, 2014

@author: ezulkosk
'''

from front.lexer import tokens
from structures import logic
from structures.exceptions import ParserException
from structures.graph import BaseGraph, SageGraph
from structures.logic import Bool, Assert, Keyword
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
    'boolvardecl : BOOL idprod'
    t[0] = [Bool(t[2], t.lexer.lineno)]
    #bools[t[2]] = "bool"
    
def p_graphvardecl(t):
    '''
    graphvardecl : GRAPH idprod LPAREN NUMBER RPAREN graphdef
                 | SAGEGRAPH DOT idprod idprod LPAREN exprlist RPAREN 
    '''
    if t[1] == "graph":
        t[0] = [BaseGraph(t[2], t[4], t[6], t.lexer.lineno)]
    else:
        t[0] = [SageGraph(t[3], t[4], t[6], t.lexer.lineno)]
    #graphs[t[2]] = (t[4], t[5], t[7])
    
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
    t[0] = [Assert(t[2], t.lexer.lineno)]

def p_operation(t):
    'operation : idprod LPAREN exprlist RPAREN'
    t[0] = BaseOperation(t[1], t[3], t.lexer.lineno)

def p_expression(t):
    '''
    expr : expr AND expr
         | expr OR expr
         | NOT expr
         | operation
         | idprod
         | NUMBER
    '''
    if len(t) == 4:
        if t[2] == '|'  : t[0] = logic.Op(Keyword("or", t.lexer.lineno), [t[1], t[3]], t.lexer.lineno)
        elif t[2] == '&': t[0] = logic.Op(Keyword("and", t.lexer.lineno), [t[1], t[3]], t.lexer.lineno)
    elif len(t) == 3:
        t[0] = logic.Op(Keyword("not", t.lexer.lineno), [t[2]], t.lexer.lineno)
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
 
def p_ID(p):
    'idprod : ID'
    p[0] = logic.ID(p[1], p.lexer.lineno) 
 
def p_empty(p):
    'empty :'
    pass

def p_error(t):
    raise ParserException("syntax error at '" + str(t.value) + ".", t.lexer.lineno)
