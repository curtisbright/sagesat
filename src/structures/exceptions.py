'''
Created on Oct 17, 2014

@author: ezulkosk
'''


class LexerException(Exception):
    def __init__(self, value=None, line_number=-1):
        self.line_number = line_number
        self.value = value
    def __str__(self):
        return repr("LexerException at line " + str(self.line_number) + ": " + self.value)

class ParserException(Exception):
    def __init__(self, value=None, line_number=-1):
        self.line_number = line_number
        self.value = value
    def __str__(self):
        return repr("ParserException at line " + str(self.line_number) + ": " + self.value)
    
class NameNotFoundException(Exception):
    def __init__(self, value=None, line_number=-1):
        self.line_number = line_number
        self.value = value
    def __str__(self):
        return repr("NameNotFoundException at line " + str(self.line_number) + ": " + self.value)

class TypeException(Exception):
    def __init__(self, operand, expected, given, line_number=-1):
        self.line_number = line_number
        self.value = "incorrect operands for " + operand + ". Given: " + given + ". Expected: " + expected + "."
    def __str__(self):
        return repr("TypeException at line " + str(self.line_number) + ": " + self.value)
    
class GraphOrderException(Exception):
    def __init__(self, ID, lower, upper, line_number=-1):
        self.line_number = line_number
        self.value = "graph " + ID + " with lower bound (" + str(lower) + ") > upper bound (" + str(upper) + ")"
    def __str__(self):
        return repr("GraphOrderException at line " + str(self.line_number) + ": " + self.value)
 
class OperationNotSupportedException(Exception):
    def __init__(self, value=None, line_number=-1):
        self.line_number = line_number
        self.value = value
    def __str__(self):
        return repr("OperationNotSupportedException at line " + str(self.line_number) + ": " + self.value)   