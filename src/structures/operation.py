'''
Created on Oct 17, 2014

@author: ezulkosk
'''

import sys

import back.operations.blasted_ops
import back.operations.sage_ops
from structures.exceptions import OperationNotSupportedException
from structures.logic import ID


class BaseOperation():
    
    def __init__(self, name, args, line_number):
        self.ID = name.ID
        self.line_number = line_number
        #reflection using the op name
        try:
            attr = getattr(back.operations.sage_ops, self.ID)
        except:
            try:
                attr = getattr(back.operations.blasted_ops, self.ID)
            except:
                raise OperationNotSupportedException(self.ID, self.line_number)
        self.op = attr
        self.args = args
        
    def map_vars(self, program):
        temp_args = []
        for i in self.args:
            if isinstance(i, ID):
                if i.ID in program.graphs.keys():
                    temp_args.append(program.graphs[i.ID])
                elif i.ID in program.bools.keys():
                    temp_args.append(program.bools[i.ID])
            else: 
                temp_args.append(i)
        return temp_args    
    
    def __str__(self):
        return "(" + self.ID + " " + " ".join([str(i) for i in self.args]) + ")"

    def __repr__(self):
        return self.__str__()