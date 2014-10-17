'''
Created on Oct 17, 2014

@author: ezulkosk
'''
from structures.exceptions import GraphOrderException


class BaseGraph():
    
    def __init__(self, ID, lower_order, upper_order, adj_matrix, line_number):
        self.ID = ID
        self.lower_order = lower_order
        self.upper_order = lower_order if not upper_order else upper_order
        if self.lower_order > self.upper_order:
            raise GraphOrderException(self.ID, self.lower_order, self.upper_order)
        self.adj_matrix =  adj_matrix
        self.line_number = line_number
        
    def instantiate(self, options):
        print(self)
    
    def __str__(self):
        return "graph " + self.ID + "(" +str(self.lower_order) + ":" + str(self.upper_order) + ":" + str(self.adj_matrix) + ")"
    
    def __repr__(self):
        return self.__str__()
        