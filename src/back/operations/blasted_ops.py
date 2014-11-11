'''
Created on Oct 14, 2014

@author: ezulkosk

Defines the operations that are eagerly encoded to SAT/BVs
'''
import sys


##########
# Axioms #
##########
def edge_to_vertex_axiom(graph, solver):
    edge_vertex_clause_sets = [[(solver.off(graph, (v1,v2)), solver.on(graph,v1)),
                            (solver.off(graph,(v1,v2)), solver.on(graph,v2))] for (v1, v2) in graph.internal_graph.edges(labels=False)]
    return [c for cs in edge_vertex_clause_sets for c in cs]
    
##############
# Operations #
##############

class Constraint():
    pass

class Eager(Constraint):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(args=None):
        sys.exit("Constraint not implemented.")
        
class Lazy(Constraint):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(args=None):
        sys.exit("Constraint not implemented.")


class subgraph(Eager):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(solver, x, G):
        #the set of vertices and edges in x is a subset of that in G.
        #currently assume that all graphs have the same possible order.
        assert(x.internal_graph.order() == G.internal_graph.order())
        clauses = []
        #x.vertex => G.vertex & x.edge => G.edge
        # <=> (CNF)
        #!x.vertex v G.vertex & ...
        for i in x.internal_graph.vertices():
            clauses.append((solver.off(x, i), solver.on(G, i)))
        return clauses
    
    
class matching(Eager):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(solver, x, G): 
        #XXX: Currently the matching contains edges and vertices -- probably it should only be the set of edges?
        #edge restriction -- no two incident edges can both be on
        #G.e1 & G.e2 => !x.e1 v !x.e2 (where e1 and e2 are incident)
        # <=>
        #!G.e1 v !G.e2 v !x.e1 v !x.e2  
        clauses = subgraph.apply(solver, x, G)
        incidence_list = [G.internal_graph.edges_incident(v, labels=False) for v in G.internal_graph.vertices()]
        for inc_edges in incidence_list:
            for i in range(len(inc_edges)):
                for j in range(i+1, len(inc_edges)):
                    clauses.append((solver.off(G, inc_edges[i]), solver.off(G, inc_edges[j]), solver.off(x, inc_edges[i]), solver.off(x, inc_edges[j])))
        #since we are returning a graph instead of a set, only include vertices that are actually matched
        #v => some incident edge <==> !v or some incident edge 
        clauses += [tuple([solver.off(x, v)] + [solver.on(x, e) for e in G.internal_graph.edges_incident(v, labels=None)]) for v in G.internal_graph.vertices()]
        return clauses

class imperfect_matching(Eager):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(solver, x, v, G):
        #ensures that the vertex v cannot be in the matching
        return [(solver.off(x, e),) for e in G.internal_graph.edges_incident(v, labels=False)]

class maximal_matching(Eager):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(solver, x, G):
        return [(solver.off(G, (v1,v2)), solver.on(x, v1), solver.on(x, v2)) for (v1,v2) in G.internal_graph.edges(labels=False)]
