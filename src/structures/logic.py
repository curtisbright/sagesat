'''
Created on Oct 17, 2014

@author: ezulkosk
'''

class Op():
    def __init__(self, name, args, line_number):
        self.name = name
        self.args = args
        self.line_number = line_number
    
    def __str__(self):
        return "(" + self.name + " " + " ".join([str(i) for i in self.args]) + ")"

    def __repr__(self):
        return self.__str__()

class Bool():
    def __init__(self, ID, line_number=-1):
        self.ID = ID
        self.line_number = line_number
        
class Assert():
    def __init__(self, expr, line_number):
        self.expr = expr
        self.line_number = line_number
        
