'''
Created on Sep 26, 2014

@author: ezulkosk
'''

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

ENCODINGS = enum('SAT', 'BV')

class Options():
    
    
    def __init__(self):
        self.ENCODING = ENCODINGS.SAT
        

