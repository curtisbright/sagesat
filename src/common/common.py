'''
Created on Sep 26, 2014

@author: ezulkosk
'''
from __future__ import print_function
import sys


INDENT = "  "

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

ENCODINGS = enum('SAT', 'BV')

def stderr_print(s):
    print(s,file=sys.stderr)
    sys.stderr.flush()

class Options():
    
    def __init__(self):
        self.ENCODING = ENCODINGS.SAT
        #Options
        self.GLUCOSE_LOCATION = "../bin/glucose"
        self.SHARPSAT_LOCATION = "../bin/sharpSAT"
        
        self.OUTPUT_DIRECTORY="../results/"
        self.DIMACS_FILE = self.OUTPUT_DIRECTORY + "dimacs"
        self.DUMP_INITIAL_DIMACS=False
        self.GLUCOSE_OUTPUT_FILE = self.OUTPUT_DIRECTORY + "output"
        self.PROOF_CERTIFICATE_FILE = self.OUTPUT_DIRECTORY + "proofcertificate"
        self.SHARPSAT = False

