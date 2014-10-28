'''
Created on Oct 17, 2014

@author: ezulkosk
'''
from common import common


class Op():
    def __init__(self, name, args, line_number):
        self.ID = name
        self.args = args
        self.line_number = line_number
    
    def __str__(self):
        return "(" + self.ID.ID + " " + " ".join([str(i) for i in self.args]) + ")"

    def __repr__(self):
        return self.__str__()

class Bool():
    def __init__(self, ID, line_number=-1):
        self.ID = ID
        self.line_number = line_number
    
    def __str__(self):
        return "bool " + self.ID.ID
        
    def toStr(self, indent):
        return common.INDENT * indent + self.__str__()
        
class Assert():
    def __init__(self, expr, line_number):
        self.expr = expr
        self.line_number = line_number
    
    def __str__(self):
        return "assert " + str(self.expr.__str__())
    
    def toStr(self, indent):
        return common.INDENT * indent + self.__str__()
        
class ID():
    def __init__(self, ID, line_number):
        self.ID = ID
        self.line_number = line_number
        
    def __str__(self):
        return str(self.ID)   
     
    def toStr(self, indent):
        return self.ID
        
class Keyword():
    def __init__(self, ID, line_number):
        self.ID = ID
        self.line_number = line_number