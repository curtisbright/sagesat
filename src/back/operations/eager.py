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
    edge_vertex_clause_sets = [[(-solver.g2v[(graph.ID.ID, (v1,v2))], solver.g2v[graph.ID.ID,v1]),
                            (-solver.g2v[(graph.ID.ID,(v1,v2))], solver.g2v[graph.ID.ID,v2])] for (v1, v2) in graph.internal_graph.edges(labels=False)]
    return [c for cs in edge_vertex_clause_sets for c in cs]
    
##############
# Operations #
##############

def subgraph(solver, x, G):
    print(x.internal_graph.vertices())
    print(G.internal_graph.vertices())
    sys.exit()
    return []

def matching(solver, x, G):
    #TODO Need to ensure subgraph!!!
    #XXX: Currently the matching contains edges and vertices -- probably it should only be the set of edges?
    #edge restriction -- no two incident edges can both be on
    incidence_list = [G.internal_graph.edges_incident(v, labels=False) for v in G.internal_graph.vertices()]
    clauses = subgraph(solver, x, G)
    for inc_edges in incidence_list:
        for i in range(len(inc_edges)):
            for j in range(i+1, len(inc_edges)):
                clauses.append((-solver.g2v[(x.ID.ID, inc_edges[i])], -solver.g2v[(x.ID.ID, inc_edges[j])]))
    #v => some incident edge <==> !v or some incident edge 
    clauses += [tuple([-solver.g2v[(x.ID.ID, v)]] + [solver.g2v[(x.ID.ID, e)] for e in G.internal_graph.edges_incident(v, labels=None)]) for v in G.vertices()]
    return clauses

def isolated_vertex(solver, graph, vertex):
    return [(-solver.g2v[e],) for e in graph.edges_incident(vertex, labels=False)]

def maximal_matching(solver, graph):
    return [(solver.g2v[v1], solver.inv_vars[v2]) for (v1,v2) in graph.edges(labels=False)]