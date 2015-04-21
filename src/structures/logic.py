'''
Created on Oct 17, 2014

@author: ezulkosk
'''
from common import common




class Op():
    
    def simp(self):
        self.args = [i.simp() for i in self.args]
        if self.ID.ID == 'or':
            self.args = [i for i in self.args if i != BoolConst("False")]
            if len(self.args) == 0:
                pass #TODO :
        elif self.ID.ID == 'and':
            pass #TODO:
        
    ''' and, or, not '''
    def __init__(self, name, args, line_number=-1):
        self.ID = name
        self.args = args
        #self.simp()
        self.line_number = line_number
    
    def __str__(self):
        return "(" + self.ID.ID + " " + " ".join([str(i) for i in self.args]) + ")"

    def __repr__(self):
        return self.__str__()

class Bool():
    def __init__(self, ID, line_number=-1):
        self.ID = ID
        self.line_number = line_number
    
    def instantiate(self, solver, options):
        solver.add_bool(self)
    
    def __str__(self):
        return "bool " + self.ID.ID
        
    def toStr(self, indent):
        return common.INDENT * indent + self.__str__()
    
class BoolConst():
    def __init__(self, val):
        self.val = val
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.val == other.val)
    
    def simp(self):
        return self
    
    def __str__(self):
        return "B" + str(self.val)
    
    def __repr__(self):
        return self.__str__()
        
    def toStr(self, indent):
        return common.INDENT * indent + self.__str__()

class Assert():
    def __init__(self, expr, line_number=-1):
        self.expr = expr
        self.line_number = line_number
    
    def __str__(self):
        return str(self.expr.__str__())
    
    def toStr(self, indent):
        return common.INDENT * indent + self.__str__()
        
class ID():
    def __init__(self, ID, line_number=-1):
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