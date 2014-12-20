'''
Created on Oct 15, 2014

@author: ezulkosk
'''
import sys
from time import sleep
import time

from ply import lex, yacc


from back.solver_interfaces import sagesat
from back.visitors import Visitor, simple_visitors
from common.common import Options, stderr_print
from front import lexer
from front import parser
from middle import checks
from middle.instantiation import instantiate_vars
from structures.exceptions import ParserException, LexerException, \
    NameNotFoundException, GraphOrderException, OperationNotSupportedException
from structures.program import Program
from sage.graphs.graph import Graph


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

def middle(solver, program, options):
    try:
        checks.resolve_and_type_check(program)
    except NameNotFoundException as e:
        stderr_print(e)
        return False
    try:
        instantiate_vars(solver, program, options)
    except NameNotFoundException as e:
        stderr_print(e)
        return False
    return True
  
def back(solver, program, options):
    #maps any graph args of an op to the correct instance 
    Visitor.visit(simple_visitors.MapVars(program, solver, options), program)
    #assigns a unique boolean to each lazy operation
    Visitor.visit(simple_visitors.T2B(program, solver, options), program)
    cnf = Visitor.retvisit(simple_visitors.DumpBooleanAbstraction(program, solver, options), program)
    solver.add_clauses(cnf)
    #sys.exit()
    #Visitor.visit(simple_visitors.BlastOps(program, solver, options), program)
    (is_sat, model) = solver.check(500)
    return (is_sat, model)


def display_results(solver, program, is_sat, model):
    if not is_sat:
        print("UNSAT " + str(model))
        return
    print("SAT")
    for (graph, low, high) in solver.graph_vars:
        print("")
        g = graph.create_graph_from_model(solver, model)
        print(graph)
        print(g)
        print(g.vertices())
        print(g.edges(labels=False))
        if False:
            p = g.plot()
            p.show()
            sleep(5)
    if program.bools.values():
        print("\nBools: ")
        for i in program.bools.values():
            try:
                if model[solver.get_dimacs_for_bool(i)]:
                    print(i.ID.ID)
                else:
                    print("!" + i.ID.ID)
            except:
                print("UNCONSTRAINED BOOL: RESULTS MAY NOT MATCH!")
  
def run(FILE):
    options = Options()
    solver = sagesat.SAGE_SAT(options)
    (success, program) = front(FILE)
    if not success:
        return
    success = middle(solver, program, options)
    if not success:
        return
    (is_sat, model) = back(solver, program, options)
    display_results(solver, program, is_sat, model)

if __name__ == '__main__':
    print("TODO:")
    print("recursive t2b")
    print("simplify based on subgraph")
    sys.argv.append("/home/ezulkosk/git/sagesat/test/inputtest")
    spec = sys.argv[1]
    run(spec)
    
    