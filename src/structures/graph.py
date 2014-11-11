'''
Created on Oct 17, 2014

@author: ezulkosk
'''

import itertools

from sage.all import *
from sage.graphs.generators.basic import CompleteGraph
from sage.graphs.generic_graph import GenericGraph

from back.operations.blasted_ops import edge_to_vertex_axiom
from common import common
import sage.graphs.generators.families as F
import sage.graphs.generators.smallgraphs as C
from structures.exceptions import GraphOrderException


class BaseGraph():
    
    def __init__(self, ID, order, adj_matrix, line_number):
        self.ID = ID
        self.order = order
        self.internal_graph = CompleteGraph(self.order)
        self.adj_matrix =  adj_matrix
        self.line_number = line_number
        
    def instantiate(self, solver, options):
        prev_vars = solver.nvars()
        solver.add_vars(self, self.internal_graph.vertices())
        solver.add_vars(self, self.internal_graph.edges(labels=False))
        solver.add_clauses(edge_to_vertex_axiom(self, solver))
        curr_vars = solver.nvars()
        solver.graph_vars.append((self, prev_vars+1, curr_vars))
   
    def vertices(self):
        return self.internal_graph.vertices()
    
    def edges(self):
        return self.internal_graph.edges()
    
    def __str__(self):
        return "graph " + self.ID.ID + "(" + str(self.order) + (":" + str(self.adj_matrix) if self.adj_matrix else "") + ")"
    
    def __repr__(self):
        return self.__str__()

    def toStr(self, indent):
        return common.INDENT * indent + self.__str__()
    
    
class SageGraph():
    
    def __init__(self, graph_type, ID, args, line_number):
        self.graph_type = graph_type.ID
        self.ID = ID
        if args == [None]:
            self.args = None
        else:
            self.args = args
        
        self.line_number = line_number
        self.internal_graph = None
    
    
    def rename_components(self, g):
        '''
        Certain constructors for graph families (e.g. CubeGraph) give different names to vertices.
        This remaps them from 0 - |V|.
        '''
        #TODO remove, obsolete by relabel
        assert isinstance(g, Graph)
        num_vertices = g.num_verts()
        new_g = Graph()
        new_g.add_vertices(range(num_vertices))
        vmap = {}
        count = 0
        for i in g.vertices():
            vmap[i] = count
            count += 1
        for i in g.edges(labels=False):
            new_g.add_edge(vmap[i[0]], vmap[i[1]])
        return new_g
            
    def instantiate(self, solver, options):
        #TODO cache.
        #reflection using the graph_type
        try:
            attr = getattr(F, self.graph_type)
        except:
            try:
                attr = getattr(C, self.graph_type)
            except:
                raise Exception()
        if self.args:
            self.internal_graph = attr(*self.args)
        else:
            self.internal_graph = attr()
        self.internal_graph.relabel()#range(temp_graph.num_verts()))
        
        
    def __str__(self):
        return self.graph_type + " " + self.ID.ID + "(" + str(self.args) + ")"
    
    def __repr__(self):
        return self.__str__()
    
    def toStr(self, indent):
        return common.INDENT * indent + self.__str__()
  
class Vertex():   
    def __init__(self, ID):
        self.ID = ID
        self.var = None
        
    def __str__(self):
        return self.ID
    
    def __repr__(self):
        return self.__str__()
  
class Edge():   
    def __init__(self, graph_ID, v1, v2):
        self.ID = graph_ID + "_e_" + str(v1) + "_" + str(v2)
        self.v1 = v1
        self.v2 = v2
        self.var = None
        
    def __str__(self):
        return self.ID
        
    def __repr__(self):
        return self.__str__()   

