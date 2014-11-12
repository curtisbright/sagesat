'''
Created on Oct 14, 2014

@author: ezulkosk
'''
import sys

from back.operations.blasted_ops import Lazy

class extends_to_hamiltonian(Lazy):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(solver, model, structures):
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
        cycle_through_matching = G.internal_graph.traveling_salesman_problem(use_edge_labels=True)
        
        #Get total weight of cycle
        #We can find a Hamiltonian cycle through the matching by converting to a TSP Problem, 
        #where edges in the matching have weight 1, and edges not in the matching have weight 2.
        #If TSP returns a cycle of weight (2*|V| - |M|), then a cycle through the matching exists.
        cycle_weight = sum([w for (_v1,_v2,w) in cycle_through_matching.edges()])
        
        #TODO don't make unnecessary clause creation calls
        if cycle_weight == 2*x.internal_graph.order()-len(matching):
            #extends
            return (True, create_hamiltonian_cycle_clause(solver, model, x, cycle_through_matching.edges(labels=None)))
            #return (True, solver.prevent_same_model_clause(model, []))
        else:
            #doesnt extend ... print("Counterexample!")
            return (False, model)
        
        
def create_hamiltonian_cycle_clause(solver, model, x, cycle_edges):
    #if a cycle is found, prevent any future matching that are subsets of the cycle.
    dimacs_edges_in_cycle = solver.get_dimacs_for_objects(x, cycle_edges)
    dimacs_edges = solver.get_dimacs_for_objects(x, x.internal_graph.edges(labels=None))
    clause = [i for i in dimacs_edges if not (i in dimacs_edges_in_cycle)]
    #print("hamclause")
    #print(clause)
    return [clause]
    
    
    