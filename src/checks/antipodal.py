'''
Created on Jan 19, 2015

@author: ezulkosk
'''

import ast
import math


if __name__ == '__main__': 
    dims = 6
    m = int(math.pow(2, dims) - 1)
    print(m)
    f = "/home/ezulkosk/git/sagesat/results/antipodal/edges_6"
    d = {}
    for line in file(f,'r'):
        l = ast.literal_eval(line)
        if abs(l[0] + l[-1]) != m :
            print(l)
        d[len(l)] = d.get(len(l), 0) + 1
        if len(l) == 23:
            print(l)
    print(d)
    print("Done")
        