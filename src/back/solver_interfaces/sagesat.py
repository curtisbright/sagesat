'''
Created on Sep 22, 2014

@author: ezulkosk
'''

import shlex
import subprocess
import time

from sage.all import *
from sage.sat.solvers import Glucose
import z3

from back.solver_interfaces import sharpsat
from common import common
from structures.logic import BoolConst


class SAGE_SAT(Glucose):
    def __init__(self, options):
        self.command=options.GLUCOSE_LOCATION + " -verb=0 -certified -certified-output=" + \
            options.PROOF_CERTIFICATE_FILE + \
            " -model " + options.DIMACS_FILE + " " + options.GLUCOSE_OUTPUT_FILE
        self.options = options
        self._v2g = {}
        self._g2v = {}
        self._t2b = {}
        self._b2t = {}
        self.antipodal_file = file("/home/ezulkosk/pycharm/sagesat/results/antipodal_edges", 'w')
        self.instantiate_graph_constraints = []
        self.graph_vars = []
        self.clauses = []
        self.process = None
        if options.RECORD_TIMES:
            self.refine_times = []
            self.solver_times = []
        sage.sat.solvers.Glucose.__init__(self, filename=options.DIMACS_FILE, command=self.command)
        
    def add_clauses(self, clauses):
        for c in clauses:
            self.add_clause(c)
    
    def add_vars(self, graph, sage_entities):
        ID = graph.ID.ID
        for i in sage_entities:
            new_var = self.var()
            self._v2g[new_var] = (ID, i)
            self._g2v[(ID, i)] = new_var
    
    def add_instantiate_graph_constraint(self, expr):
        self.instantiate_graph_constraints.append(expr)
    
    def add_bool(self, b):
        new_var = self.var()
        self._v2g[new_var] = b
        self._g2v[b] = new_var
    
    def add_clause(self, c):
        l = []
        for i in c:
            if isinstance(i, BoolConst):
                if i.val:
                    return
            else:
                l.append(i)
        tup = tuple(l)
        return super(SAGE_SAT, self).add_clause(tup)
    
    def t2b(self, op):
        '''
        Maps the tuple of an op + args to a boolean variable.
        Creates a new variable if necessary.
        Returns the dimacs variable
        '''
        sig = (op.ID, tuple(op.args))
        d = self._t2b.get(sig)
        if d:
            return d
        else:
            new_var = self.var()
            self._t2b[(op, tuple(op.args))] = new_var
            self._b2t[new_var] = (op, op.args)
            return new_var
    
    def b2t(self, v):
        return self._b2t[v]
    
    def on(self, graph, entity):
        #replaces g2v
        #returns the dimacs variable associated with the graph entity (edge or vertex),
        #If the graph is a sagegraph, returns True or False
        try:
            b = self._g2v[(graph.ID.ID, entity)]
            return z3.Bool(str(b))
            #b = self._g2v[(graph.ID.ID, entity)]  old
        except:
            #sage graph case
            if entity in graph.internal_graph.vertices() or entity in graph.internal_graph.edges(labels=False):
                return BoolConst(True)
            else:
                return BoolConst(False)
        return b  
    
    def off(self, graph, entity):
        #negation of on
        val_temp = self.on(graph, entity)
        try:
            #val = -val_temp old
            return z3.Not(val_temp)
        except:
            if val_temp.val:
                val = BoolConst(False)
            else:
                val = BoolConst(True)
        return val
        
    def get_dimacs_for_objects(self, graph, objects):
        return [self._g2v[(graph.ID.ID,i)] for i in objects]
    
    def get_dimacs_for_bool(self, b):
        try:
            return self._g2v[b]
        except:
            return None
    
    def get_objects_in_model(self, model, graph, objects, inverse=False):
        '''
        returns the objects that are set to true by the SAT solver
        '''
        dimacs_vars = self.get_dimacs_for_objects(graph, objects)
        if not inverse:
            l = [self._v2g[i] for i in dimacs_vars if model[i]]
        else:
            l = [self._v2g[i] for i in dimacs_vars if not model[i]]
        return [i for (_, i) in l]
            
    
    def get_result(self):
        if self.options.RECORD_TIMES:
            start = time.time()
        try:
            model = self.process.stdout.readline()
            if self.options.RECORD_TIMES:
                self.solver_times.append(time.time() - start)
            s = map(int, model.strip().split(" "))
            s = (None,) + tuple(e>0 for e in s)
            return list(s)
        except:
            return None
    
    def dump_to_dimacs(self):
        
        
        self.write()
        output_filename = self.options.GLUCOSE_OUTPUT_FILE
        command = self._command.strip()
        if "{output}" in command:
            output_filename = tmp_filename()
        command = command.format(input=self._headname, output=output_filename)
        if self.options.DUMP_INITIAL_DIMACS:
            print("Dimacs in " + self.options.DIMACS_FILE + ", exiting.")
        return command
        
    def sharpSAT(self):
        self.dump_to_dimacs()
        return sharpsat.get_num_solutions(self._headname, self.options)
         
    def initial_call(self):
        if self.options.SHARPSAT:
            return self.sharpSAT()
        
        command = self.dump_to_dimacs()
        if self.options.DUMP_INITIAL_DIMACS:
            return None
        args = shlex.split(command)
        try:
            self.process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except OSError:
            raise OSError("Could run '%s', perhaps you need to add your SAT solver to $PATH?"%(" ".join(args)))
        return self.get_result()
    
    def refine(self, clauses):
        for c in clauses:
            #add clause to output final dimacs file
            self.add_clause(c)
            c_str = " ".join([str(i) for i in c])
            self.process.stdin.write(c_str +"\n")
        #alert glucose that there are no more clauses
        self.process.stdin.write("0\n")
        res = self.get_result()
        
        return res
        
    def check(self, progress_count=None):
        '''
        progress_count -- outputs the number of sat solutions returned for each multiple of progress_count
        '''
        count = 0 #number of sat solutions checked
        
        #get satisfying solution
        model = self.initial_call()
        while True:
            if not model:
                #print("Done: " + str(count))
                #dump DIMACS
                self.write(self.options.DIMACS_FILE)
                return (False, count)
            count += 1
            if progress_count and count % progress_count == 0:
                print(count)
            sat = True
            clauses = []
            if self.options.RECORD_TIMES:
                start = time.time()
            for i in self._b2t.keys():
                #TODO t2b needs to be fixed for recursive
                #TODO should convert result to cnf, currently overkill
                (baseop, args) = self.b2t(i)
                (is_satisfied, learn_args) = baseop.op.apply(self, model, args)
                if is_satisfied == model[i]:
                    continue
                else:
                    learned_clauses = baseop.op.learn(self, model, *learn_args)
                    sat = False
                    for j in learned_clauses:
                        if is_satisfied:
                            j.append(i)
                        else:
                            j.append(-i)
                    clauses += learned_clauses
            if self.options.RECORD_TIMES:
                self.refine_times.append(time.time() - start)
            if not sat:
                model = self.refine(clauses)
            if sat:
                #SAT -- kill glucose
                print("CHECK ITERATIONS: " + str(count))
                self.write(self.options.DIMACS_FILE)
                self.refine([])    
                return (True, model)
                