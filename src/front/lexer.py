'''
Created on Oct 15, 2014

@author: ezulkosk
'''
from structures.exceptions import LexerException


tokens = (
    'AND',
    'OR',
    'NOT',
    'ID',
    'NUMBER',
    'BOOL',
    'GRAPH',
    'ASSERT',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET', 
    'COMMA',
    'EQUALS',
    'DOT',
    'SAGEGRAPH'
    )
# Tokens
reserved = {
   'graph' : 'GRAPH',
   'sagegraph' : 'SAGEGRAPH',
   'bool' : 'BOOL',
   'assert' : 'ASSERT'
}

t_DOT = r'\.'
t_AND    = r'&'
t_OR   = r'\|'
t_NOT   = r'!'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS  = r'='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    raise LexerException("illegal character '" + str(t.value[0]) + ".", t.lineno)
    
def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded
    