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
    #print(program.toStr(0))
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
    


def display_results(solver, program, is_sat, model):
    if solver.options.RECORD_TIMES:
        f = open("/home/ezulkosk/ham.out", 'w')
        f.write("Refine Times: " + str(sum(solver.refine_times)) + "\n")
        f.write("Solver Times: " + str(sum(solver.solver_times)) + "\n")
        f.write(",".join([str(i) for i in solver.refine_times]) + "\n")
        f.write(",".join([str(i) for i in solver.solver_times]) + "\n")
        f.close()
    
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
  
def run(FILE, options=Options()):
    solver = sagesat.SAGE_SAT(options)
    (success, program) = front(FILE)
    if not success:
        return
    success = middle(solver, program, options)
    if not success:
        return
    back(solver, program, options)
    if solver.options.SHARPSAT:
        return solver.sharpSAT()
    else:
        (is_sat, model) = solver.check(500)
        display_results(solver, program, is_sat, model)
        #print("Refine time:", solver.refine_time)
        return is_sat
    

if __name__ == '__main__':
    import cProfile
    sys.argv.append("../test/hamilton")
    #sys.argv.append("../test/antipodal")
    #sys.argv.append("../test/forbidden_matchings_of_hamilton_cycle")
    #sys.argv.append("../test/matching_counts/d5/maximal_forbidden_matchings")
    #sys.argv.append("../test/enum_d5_matchings/e13")
    #sys.argv.append("../test/count_matchings_cycle")
    options = Options()
    options.RECORD_TIMES = True
    #options.DUMP_INITIAL_DIMACS = True
    spec = sys.argv[1]
    run(spec, options)
        
    #print("Total time:", time.time() - start)
    
    
    