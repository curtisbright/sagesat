'''
Created on Oct 15, 2014

@author: ezulkosk
'''
import time

from ply import lex, yacc

from back.solver_interfaces import sagesat
from back.visitors import Visitor, CNF
from common.common import Options, stderr_print
from front import lexer
from front import parser
from middle import checks
from middle.instantiation import instantiate_vars
from structures.exceptions import ParserException, LexerException, \
    NameNotFoundException, GraphOrderException, OperationNotSupportedException
from structures.program import Program


TEST_DIR = "../test/"
TEST_PARSER_DIR = TEST_DIR + "parser/"
TESTINPUT= [TEST_PARSER_DIR + "p_example1",
            TEST_PARSER_DIR + "n_undefinedvar1",

            TEST_DIR + "hamilton"
            ]

def front(FILE):
    l = lex.lex(module=lexer)
    with open(FILE, "rb") as read_file:
        contents = read_file.read()
    l.input(contents)
    try:
        yy = yacc.yacc(module=parser)
        ast = yy.parse(lexer=l)
    except (ParserException, LexerException, GraphOrderException, OperationNotSupportedException) as e:
        stderr_print(e)
        return (False, None)
    program = Program(ast)
    print(program.toStr(0))
    return (True, program)

def middle(program, options):
    try:
        checks.resolve_and_type_check(program)
    except NameNotFoundException as e:
        stderr_print(e)
        return False
    try:
        instantiate_vars(program, options)
    except Exception as e:
        stderr_print(e)
        return False
    return True
  
def back(program, options):
    solver = sagesat.SAGE_SAT(options)
    Visitor.visit(CNF.CNF(program, solver, options), program)
  
def run(FILE):
    options = Options()
    (success, program) = front(FILE)
    if not success:
        return
    success = middle(program, options)
    if not success:
        return
    success = back(program, options)

if __name__ == '__main__':
    for i in TESTINPUT:
        print("==================================")
        print(i)
        print("==================================")
        run(i)
        time.sleep(0.1)
    
    