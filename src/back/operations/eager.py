'''
Created on Oct 14, 2014

@author: ezulkosk

Defines the operations that are eagerly encoded to SAT/BVs
'''


##########
# Axioms #
##########

def edge_to_vertex_axiom(graph, solver):
    edge_vertex_clause_sets = [[(-solver.inv_vars[(v1,v2)], solver.inv_vars[v1]),
                            (-solver.inv_vars[(v1,v2)], solver.inv_vars[v2])] for (v1, v2) in graph.edges(labels=False)]
    return [c for cs in edge_vertex_clause_sets for c in cs]
    
##############
# Operations #
##############

def matching(solver, x, G):
    #XXX: Currently the matching contains edges and vertices -- probably it should only be the set of edges?
    #edge restriction -- no two incident edges can both be on
    print(G)
    incidence_list = [G.edges_incident(v, labels=False) for v in G.vertices()]
    clauses = []
    for inc_edges in incidence_list:
        for i in range(len(inc_edges)):
            for j in range(i+1, len(inc_edges)):
                clauses.append((-solver.inv_vars[inc_edges[i]], -solver.inv_vars[inc_edges[j]]))
    #v => some incident edge <==> !v or some incident edge 
    clauses += [tuple([-solver.inv_vars[v]] + [solver.inv_vars[e] for e in G.edges_incident(v, labels=None)]) for v in G.vertices()]
    return clauses

def isolated_vertex(solver, graph, vertex):
    return [(-solver.inv_vars[e],) for e in graph.edges_incident(vertex, labels=False)]

def maximal_matching(solver, graph):
    return [(solver.inv_vars[v1], solver.inv_vars[v2]) for (v1,v2) in graph.edges(labels=False)]