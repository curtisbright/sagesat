'''
Created on Sep 22, 2014

@author: ezulkosk
'''

import shlex
import subprocess

from sage.all import *
from sage.sat.solvers import Glucose

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
        self.graph_vars = []
        self.clauses = []
        self.process = None
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
            self._t2b[(op.ID, tuple(op.args))] = new_var
            self._b2t[new_var] = (op.ID, op.args)
            return new_var
    
    
    def on(self, graph, entity):
        #replaces g2v
        #returns the dimacs variable associated with the graph entity (edge or vertex),
        #If the graph is a sagegraph, returns True or False
        try:
            b = self._g2v[(graph.ID.ID, entity)] 
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
            val = -val_temp
        except:
            if val_temp:
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
            return [self._v2g[i] for i in dimacs_vars if model[i]]
        else:
            return [self._v2g[i] for i in dimacs_vars if not model[i]]
    
    def prevent_same_model_clause(self, model, _structures):
        #Adds the most basic constraint to the solver, preventing the same EXACT instance from reoccuring.
        clause = []
        for i in range(1, len(model)):
            if model[i]:
                clause.append(-(i))
        return (False, [clause])
    
    def get_result(self):
        
        try:
            model = self.process.stdout.readline()
            s = map(int, model.strip().split(" "))
            s = (None,) + tuple(e>0 for e in s)
            #TODO get rid of this
            self.refine([])
            return list(s)
        except:
            return None
    
    def initial_call(self):
        self.write()
        output_filename = self.options.GLUCOSE_OUTPUT_FILE
        command = self._command.strip()
        if "{output}" in command:
            output_filename = tmp_filename()
        command = command.format(input=self._headname, output=output_filename)
        #print(sharpsat.get_num_solutions(self._headname))
        args = shlex.split(command)
        try:
            self.process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except OSError:
            raise OSError("Could run '%s', perhaps you need to add your SAT solver to $PATH?"%(" ".join(args)))
        return self.get_result()
    
    def refine(self, clauses):
        #print(len(clauses))
        for c in clauses:
            #add clause to output final dimacs file
            self.add_clause(c)
            c_str = " ".join([str(i) for i in c])
            #print(c_str)
            self.process.stdin.write(c_str +"\n")
        #alert glucose that there are no more clauses
        self.process.stdin.write("0\n")
        return self.get_result()
        '''
        #OLD fix sage to handle multiple clauses
        for c in clauses:
            #add clause to output final dimacs file
            self.add_clause(c)
            c_str = " ".join([str(i) for i in c])
            self.process.stdin.write(c_str +"\n")
        return self.get_result()
        '''
        
    def check(self, extra_check=None, structures=None, progress_count=None):
        '''
        extra_check -- function that check some extra property of a sat solution,
        should return the tuple (bool, clauses), 
        where bool is True if the solution satisfies the check (in which case the value of clauses is ignored),
        or False, in which case clauses are added to the solver.
        structures -- list of objects that are utilized by the extra_check
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
            if extra_check:
                (is_satisfied, clauses) = extra_check(self, model, structures)
                if is_satisfied:
                    return (True, model)
                else:
                    model = self.refine(clauses)
            return (True, model)
                
                