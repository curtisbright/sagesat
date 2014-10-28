'''
Created on Oct 14, 2014

@author: ezulkosk
'''
import sys


def create_hamiltonian_cycle_clause(solver, model, g, cycle_edges):
    #if a cycle is found, prevent any future matching that are subsets of the cycle.
    dimacs_edges_in_cycle = solver.get_dimacs_for_objects(cycle_edges)
    dimacs_edges = solver.get_dimacs_for_objects(g.edges(labels=None))
    clause = [i for i in dimacs_edges if not (i in dimacs_edges_in_cycle)]
    return [clause]
    
    
def check_hamiltonicity(solver, model, structures):
    g = structures[0]
    #get edges in matching
    matching = solver.get_objects_in_model(model, g.edges(labels=False))

    #Convert to TSP problem:
    for (v1,v2) in g.edges(labels=False):
        if (v1,v2) in matching:
            g.set_edge_label(v1,v2,1) 
        else:
            g.set_edge_label(v1,v2,2)
    cycle_through_matching = g.traveling_salesman_problem(use_edge_labels=True)
    
    #Get total weight of cycle
    #We can find a Hamiltonian cycle through the matching by converting to a TSP Problem, 
    #where edges in the matching have weight 1, and edges not in the matching have weight 2.
    #If TSP returns a cycle of weight (2*|V| - |M|), then a cycle through the matching exists.
    cycle_weight = sum([w for (_v1,_v2,w) in cycle_through_matching.edges()])
    if cycle_weight == 2*g.order()-len(matching):
        #Not a counterexample to conjecture, create new clause
        return (False, create_hamiltonian_cycle_clause(solver, model, g, cycle_through_matching.edges(labels=None)))
    else:
        print("Counterexample!")
        return (True, model)
    
    