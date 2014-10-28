'''
Created on Oct 17, 2014

@author: ezulkosk
'''

import itertools

from sage.all import *
from sage.graphs.generic_graph import GenericGraph

from common import common
import sage.graphs.generators.families as F
from structures.exceptions import GraphOrderException


class BaseGraph(GenericGraph):
    
    def __init__(self, ID, order, adj_matrix, line_number):
        self.ID = ID
        self.order = order
        self.adj_matrix =  adj_matrix
        self.line_number = line_number
        
    def instantiate(self, options):
        self._vertices = [Vertex(self.ID.ID + "$v" + str(i)) for i in range(self.order)]
        vertex_pairs = list(itertools.combinations(self._vertices, 2))
        self._edges = [Edge(self.ID.ID, v1, v2) for (v1,v2) in vertex_pairs]
   
    def vertices(self):
        return self._vertices
    
    def edges(self):
        return self._edges
    
    def __str__(self):
        return "graph " + self.ID.ID + "(" + str(self.order) + ":" + str(self.adj_matrix) + ")"
    
    def __repr__(self):
        return self.__str__()

    def toStr(self, indent):
        return common.INDENT * indent + self.__str__()
    
    
class SageGraph():
    
    def __init__(self, graph_type, ID, args, line_number):
        self.graph_type = graph_type
        self.ID = ID
        self.args = args
        self.line_number = line_number
        self.internal_graph = None
        
    def instantiate(self, options):
        self.internal_graph = F.CubeGraph(self.args)
        #reflection using the graph_type
        attr = getattr(F, self.graph_type)
        self.internal_graph = attr(self.args)
        
    def __str__(self):
        return self.graph_type + " " + self.ID + "(" + str(self.args) + ")"
    
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

