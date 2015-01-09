'''
Created on Oct 14, 2014

@author: ezulkosk
'''
import math
import sys

from sage.categories.sets_cat import EmptySetError
from sage.graphs.graph import Graph

from back.operations.blasted_ops import Constraint


class Lazy(Constraint):
    
    @staticmethod
    def apply(args=None):
        sys.exit("Constraint not implemented.")
    
    @staticmethod
    def learn(solver, model, *structures):
        #Adds the most basic constraint to the solver, preventing the same EXACT instance from reoccuring.
        clause = []
        for i in range(1, len(model)):
            if model[i]:
                clause.append(-(i))
            else:
                clause.append((i))
        return [clause]


class girth(Lazy):

    @staticmethod
    def apply(solver, model, structures):
        x = structures[0]
        x_g = x.create_graph_from_model(solver, model)
        girth = structures[1]
        if x_g.girth() != girth:
            return (False, [])
        else:
            return (True, [])






class extends_to_hamiltonian(Lazy):
    
    @staticmethod
    def apply(solver, model, structures):
        #TODO change to be more robust -- use create_graph_for_model on BOTH
        x = structures[0]
        G = structures[1]
        #get edges in matching
        matching = solver.get_objects_in_model(model, x, x.internal_graph.edges(labels=False))
        #Convert to TSP problem:
        for (v1,v2) in G.internal_graph.edges(labels=False):
            if (v1,v2) in matching:
                G.internal_graph.set_edge_label(v1,v2,1) 
            else:
                G.internal_graph.set_edge_label(v1,v2,2)
        try:
            cycle_through_matching = G.internal_graph.traveling_salesman_problem(use_edge_labels=True)
        except EmptySetError:
            #The graph is non-hamiltonian - return the empty clause
            #TODO HOW to handle this case?
            return (False, [[]])
        
        #Get total weight of cycle
        #We can find a Hamiltonian cycle through the matching by converting to a TSP Problem, 
        #where edges in the matching have weight 1, and edges not in the matching have weight 2.
        #If TSP returns a cycle of weight (2*|V| - |M|), then a cycle through the matching exists.
        cycle_weight = sum([w for (_v1,_v2,w) in cycle_through_matching.edges()])
        
        if cycle_weight == 2*x.internal_graph.order()-len(matching):
            #Hamiltonian cycle found - create a clause corresponding to edges not in the cycle. 
            return (True, [x, cycle_through_matching.edges(labels=None)]) #extends_to_hamiltonian.create_hamiltonian_cycle_clause(solver, model, x, cycle_through_matching.edges(labels=None)))
        else:
            #Hamiltonian cycle not found - ensure no future x has edges that are a subset of the current x.
            return (False, [x, matching])#extends_to_hamiltonian.create_hamiltonian_cycle_clause(solver, model, x, matching.edges(labels=None)))
        
    @staticmethod    
    def learn(solver, model, x, cycle_edges):
        '''
        TODO doc
        '''
        #if a cycle is found, prevent any future matching that are subsets of the cycle.
        dimacs_edges_in_cycle = solver.get_dimacs_for_objects(x, cycle_edges)
        dimacs_edges = solver.get_dimacs_for_objects(x, x.internal_graph.edges(labels=None))
        clause = [i for i in dimacs_edges if not (i in dimacs_edges_in_cycle)]
        #print("hamclause")
        #print(clause)
        return [clause]

class exists_connected_antipodal_vertices(Lazy):

    @staticmethod
    def apply(solver, model, structures):
    
        g = structures[0]
        vertices = solver.get_objects_in_model(model, g, g.internal_graph.vertices())
        dims = int(math.log(g.order, 2))
        #print(vertices)
        #print(dims)
        edges = solver.get_objects_in_model(model, g, g.internal_graph.edges(labels=False))
        #print(edges)
        #create temp graph
        t = Graph()
        t.add_vertices(vertices)
        t.add_edges(edges)
        for i in range(g.order/2):
            antipod = g.order - 1 - i
            #print(i, antipod)
            if i in vertices and antipod in vertices:
                path = t.shortest_path(i, antipod)
                if path:
                    #print(path)
                    return (True, [g, path])
        print("COUNTER")
        return (False, [])
        
    @staticmethod    
    def learn(solver, model, g, path):
        #print(path)
        edges = []
        prev = path[0]
        for i in path[1:]:
            edges.append((min(prev, i), max(prev,i)))
            prev = i
        dimacs_edges = solver.get_dimacs_for_objects(g, edges)
        clause = [-i for i in dimacs_edges]
        
        
        return [clause]

    
    