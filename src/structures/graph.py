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
        solver.add_instantiate_graph_constraint(edge_to_vertex_axiom(self, solver))
        curr_vars = solver.nvars()
        solver.graph_vars.append((self, prev_vars+1, curr_vars))
   
    def create_graph_from_model(self, solver, model):
        '''
        Given a model from the SAT solver, construct the graph.
        '''
        g = Graph()
        on_vertices = solver.get_objects_in_model(model, self, self.internal_graph.vertices())
        on_edges = solver.get_objects_in_model(model, self, self.internal_graph.edges(labels=False))
        g.add_vertices(on_vertices)
        g.add_edges(on_edges)
        return g
        
        
   
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
            self.args = []
        else:
            self.args = args
        
        self.line_number = line_number
        self.internal_graph = None
            
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
        self.internal_graph.relabel()
        
    def __str__(self):
        return self.graph_type + " " + self.ID.ID + "(" + ", ".join([str(i) for i in self.args]) + ")"
    
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

