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
        self.GLUCOSE_LOCATION = "/home/ezulkosk/Downloads/glucose-3.0/core/glucose"
        self.SHARPSAT_LOCATION = "/home/ezulkosk/git/hamilton/bin/sharpSAT"
        
        self.OUTPUT_DIRECTORY="/home/ezulkosk/git/sagesat/results/"
        self.DIMACS_FILE = self.OUTPUT_DIRECTORY + "dimacs"
        self.GLUCOSE_OUTPUT_FILE = self.OUTPUT_DIRECTORY + "output"
        self.PROOF_CERTIFICATE_FILE = self.OUTPUT_DIRECTORY + "proofcertificate"
        self.SHARPSAT = False

