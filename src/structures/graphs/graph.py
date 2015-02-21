'''
Created on Oct 17, 2014

@author: ezulkosk
'''





import itertools

from sage.all import *
from sage.graphs.generators.basic import CompleteGraph, CycleGraph
from sage.graphs.generic_graph import GenericGraph
from sage.graphs.graph_generators import graphs

from back.operations.blasted_ops import edge_to_vertex_axiom
from common import common
import networkx as N
import sage.graphs.generators.families as F
import sage.graphs.generators.smallgraphs as C
import sage.graphs.generators.basic as B
from structures.exceptions import GraphOrderException


class CASGraph():
    
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
                try:
                    attr = getattr(B, self.graph_type)
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
  
  

