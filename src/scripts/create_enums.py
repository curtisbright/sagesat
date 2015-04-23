'''
Created on Apr 20, 2015

@author: ezulkosk
'''
import itertools
import sys

from common.common import Options
from main import run

from sage.graphs.generators.families import CubeGraph

if __name__ == '__main__':
    
    s = "graph x(32)\nsagegraph.CubeGraph G(5)\nassert matching(x,G)\nassert imperfect_matching(x,0,G)\nassert maximal_matching(x,G)\n"
    
    cycle = [(0,1),(0,8),(1,9),(2,6),(2,10),(3,7),(3,19),(4,5),(4,20),(5,21),(6,22),(7,23),(8,12),(9,25),(10,11),(11,27),(12,14),
             (13,15),(13,29),(14,30),(15,31),(16,18),(16,24),(17,19),(17,25),(18,26),(20,28),(21,29),(22,23),(24,28),(26,30),(27,31)]

    print(s)
    G = CubeGraph(5)
    G.relabel() 
    #print(G)
    c_edges = set(G.edges(labels=False))
    off = c_edges.difference(cycle)
    
    for (u,v) in off:
        print("assert disallowed_edge(x," + str(u) + "," + str(v) + ")")

    
    sys.exit()
    
    base_dir="../../test/enum_d5_matchings/"
    v1 = [(1,3), (1,5), (1,9), (1,17)]
    v2 = [(2,3), (2,6), (2,10), (2,18)]
    v7 = [(3,7), (5,7), (6,7), (7,15), (7, 23)]
    
    for i in itertools.product(v1,v2,v7):
        name = "e_" + "_".join([str(u) +str(v) for (u,v) in i])
        print(name)
        f = open(base_dir + name, 'w')
        f.write(s)
        for (u,v) in i:
            f.write("assert required_edge(x," + str(u) + "," + str(v) + ")\n")
        f.close()
        
        options = Options()
        options.DUMP_INITIAL_DIMACS = True
        options.DIMACS_FILE=base_dir + name + ".dimacs"
        spec = base_dir + name
        run(spec, options)
            
            