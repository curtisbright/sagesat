'''
Created on Oct 14, 2014

@author: ezulkosk

Defines the operations that are eagerly encoded to SAT/BVs
'''
import itertools
import sys

import back
from back.visitors import Visitor

from structures.logic import Op, ID


##########
# Axioms #
##########
def edge_to_vertex_axiom(graph, solver):
    clauses = []
    for (v1, v2) in graph.internal_graph.edges(labels=False):
        clauses.append(Op(ID('or'), [solver.off(graph, (v1,v2)), solver.on(graph,v1)]))
        clauses.append(Op(ID('or'), [solver.off(graph,(v1,v2)), solver.on(graph,v2)]))
    return Op(ID('and'), clauses)
    
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
            clauses.append(Op(ID('or'), [solver.off(x, i), solver.on(G, i)]))
        for i in x.internal_graph.edges(labels=False):
            clauses.append(Op(ID('or'), [solver.off(x, i), solver.on(G, i)]))
        return Op(ID('and'), clauses)
    
    
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
        clauses = [subgraph.apply(solver, x, G)]
        incidence_list = [G.internal_graph.edges_incident(v, labels=False) for v in G.internal_graph.vertices()]
        for inc_edges in incidence_list:
            for i in range(len(inc_edges)):
                for j in range(i+1, len(inc_edges)):
                    clauses.append(Op(ID('or'), [solver.off(G, inc_edges[i]), solver.off(G, inc_edges[j]), solver.off(x, inc_edges[i]), solver.off(x, inc_edges[j])]))
        #since we are returning a graph instead of a set, only include vertices that are actually matched
        #v => some incident edge <==> !v or some incident edge 
        clauses += [Op(ID('or'),[solver.off(x, v)] + [solver.on(x, e) for e in G.internal_graph.edges_incident(v, labels=None)]) for v in G.internal_graph.vertices()]
        return Op(ID('and'), clauses)

class imperfect_matching(Eager):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(solver, x, v, G):
        #ensures that the vertex v cannot be in the matching
        return Op(ID('and'), [solver.off(x, e) for e in G.internal_graph.edges_incident(v, labels=False)])

class maximal_matching(Eager):
    
    def __init__(self):
        pass
    
    @staticmethod
    def apply(solver, x, G):
        return Op(ID('and'), [Op(ID('or'),[solver.off(G, (v1,v2)), solver.on(x, v1), solver.on(x, v2)]) for (v1,v2) in G.internal_graph.edges(labels=False)])


class card(Eager):
    #TODO make efficient
    @staticmethod
    def apply(solver, x, l, low=-1, high=-1):
        from back.visitors.simple_visitors import DumpBooleanAbstraction
        subexprs = []
        combs = itertools.combinations(l, low)
        if low == high:
            for i in combs:
                subexprs.append(Op(ID('and'), [solver.on(x, j) for j in i] + [solver.off(x, j) for j in list(set(l) - set(i))]))
            return Op(ID('or'), subexprs)
        else:
            sys.exit("TODO card cases")

class k_regular(Eager):
    
    @staticmethod
    def apply(solver, x, k):
        res = []
        x_g = x.internal_graph
        for v in x_g.vertices():
            edges_inc_v = x_g.edges_incident(v, labels=False)
            res.append(Op(ID('or'), [solver.off(x, v), card.apply(solver, x, edges_inc_v, low=k, high=k)]))
            #sys.exit()
        return Op(ID('and'), res)