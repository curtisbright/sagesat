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

def itersubclasses(cls, _seen=None):
    """
    itersubclasses(cls)

    Generator over all subclasses of a given class, in depth first order.

    >>> list(itersubclasses(int)) == [bool]
    True
    >>> class A(object): pass
    >>> class B(A): pass
    >>> class C(A): pass
    >>> class D(B,C): pass
    >>> class E(D): pass
    >>> 
    >>> for cls in itersubclasses(A):
    ...     print(cls.__name__)
    B
    D
    E
    C
    >>> # get ALL (new-style) classes currently defined
    >>> [cls.__name__ for cls in itersubclasses(object)] #doctest: +ELLIPSIS
    ['type', ...'tuple', ...]
    """
    
    if not isinstance(cls, type):
        raise TypeError('itersubclasses must be called with '
                        'new-style classes, not %.100r' % cls)
    if _seen is None: _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError: # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in itersubclasses(sub, _seen):
                yield sub

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

