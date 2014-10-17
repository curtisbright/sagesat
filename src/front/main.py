'''
Created on Oct 15, 2014

@author: ezulkosk
'''
import sys

from ply import lex, yacc

from common.common import Options
from front import lexer
from front import parser
from middle import checks
from middle.instantiation import instantiate_vars
from structures.exceptions import ParserException, LexerException, \
    NameNotFoundException, GraphOrderException
from structures.program import Program


TESTINPUT= ["../../test/parser/p_example1",
            "../../test/parser/n_undefinedvar1",
            "../../test/parser/n_graphbounds"
            ]

def front(FILE):
    l = lex.lex(module=lexer)
    with open(FILE, "rb") as read_file:
        contents = read_file.read()
    l.input(contents)
    try:
        yy = yacc.yacc(module=parser)
        ast = yy.parse(lexer=l)
    except (ParserException, LexerException, GraphOrderException) as e:
        print(e)
        return (False, None)
    program = Program(ast)
    return (True, program)

def middle(program, options):
    try:
        checks.resolve_and_type_check(program)
    except NameNotFoundException as e:
        print(e)
        return False
    try:
        instantiate_vars(program, options)
    except Exception as e:
        print(e)
        return False
    return True
    
def run(FILE):
    options = Options()
    (success, program) = front(FILE)
    if not success:
        return
    success = middle(program, options)
    if not success:
        return

if __name__ == '__main__':
    for i in TESTINPUT:
        print("==================================")
        print(i)
        print("==================================")
        run(i)
    
    