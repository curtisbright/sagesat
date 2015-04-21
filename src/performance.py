


import ast
import itertools
import math
import sys
import time


#from common.common import Options
#from main import run
#from sage.graphs.generators.families import CubeGraph
def load_lists(s,test=False, start_index=0, num_iters=-1):
    f = open(s,'r')
    forbidden_matchings = []
    if num_iters < 0:
        limit = -1
    else:
        limit = start_index + num_iters
    iters = -1
    for line in f:
        iters += 1
        if iters < start_index:
            continue
        elif limit > 0 and iters >= limit:
            break
        forbidden_matchings.append(ast.literal_eval(line))
        
        if test and iters % 100 == 0:
            return forbidden_matchings
    return forbidden_matchings


def compute_perm(c):
    #base_cycle = [(0,1),(0,8),(1,9),(2,6),(2,10),(3,7),(3,19),(4,5),(4,20),(5,21),(6,22),(7,23),(8,12),(9,25),(10,11),(11,27),(12,14),
    #         (13,15),(13,29),(14,30),(15,31),(16,18),(16,24),(17,19),(17,25),(18,26),(20,28),(21,29),(22,23),(24,28),(26,30),(27,31)]
    #base_perm = [0, 1, 9, 25, 17, 19, 3, 7, 23, 22, 6, 2, 10, 11, 27, 31, 15, 13, 29, 21, 5, 4, 20, 28, 24, 16, 18, 26, 30, 14, 12, 8]

    c2 = [i for i in c]
    perm = []
    #print(c[1:])
    
    (u,v) = c2[0]
    assert u == 0
    perm.append(u)
    c2.remove((u,v))
    while c2:
        perm.append(v)
        (u2,v2) = [(u2,v2) for (u2,v2) in c2 if (u2 == v or v2 == v)][0]
        if v == v2:
            v = u2
        else:
            v = v2
        c2.remove((u2,v2))

    #print(len(perm))
    #print(perm)
    
    perm_dict = {}
    for i in range(len(perm)):
        #fix me and figure out how to only consider correct matchings for the cycle
        perm_dict[i] = perm[i]
    #print(perm_dict)
    #sys.exit()
    return perm_dict

def simp_tuple(u,v):
    #if u == 1 and v > 9:
    #    sys.exit(str(u) + " " + str(v))
    #return (u,v)
    return 32*u + v

def check_partner(tup, pu, pv):
    (u,v) = tup
    if pu == 1 and u == 1:
        if v == pv:
            return True
        else:
            return None  
    elif u == pu:
        return True
    else:
        return False
    
def check_maximal(cycle, matching, q5_edges, my_partition = None):
    #print(cycle)
    #print(matching)
    vertices = list(sum(matching, ()))
    #print(my_partition)
    if not check_partition(matching, vertices, my_partition):
        return False
    #print(vertices)
    #print(G.edges)
    for (u,v) in q5_edges:
        if u != 0 and not(u in vertices or v in vertices):
            #print("BAD")
            #print(u,v)
            #sys.exit()
            return False
    return True

def check_partition(matching, vertices, my_partition = None):
    if not my_partition:
        return True
    for (u,v) in my_partition:
        if v == -1 and u in vertices:
            return False
        elif not (u,v) in matching:
                return False
    return True

if __name__ == '__main__':
    
    dims = 5
    working_dir = "/home/ezulkosk/git/sagesat/results/performance/"
 
    
 
 
    working_dir = sys.argv[1]
    num_iters = int(sys.argv[2])
    #which cycle to start at
    start_index = num_iters * int(sys.argv[3])

    q5_edges = [(0, 1), (0, 2), (0, 4), (0, 8), (0, 16), (1, 3), (1, 5), (1, 9), (1, 17), (2, 3), (2, 6), 
                (2, 10), (2, 18), (3, 7), (3, 11), (3, 19), (4, 5), (4, 6), (4, 12), (4, 20), (5, 7), (5, 13), 
                (5, 21), (6, 7), (6, 14), (6, 22), (7, 15), (7, 23), (8, 9), (8, 10), (8, 12), (8, 24), 
                (9, 11), (9, 13), (9, 25), (10, 11), (10, 14), (10, 26), (11, 15), (11, 27), (12, 13), (12, 14), 
                (12, 28), (13, 15), (13, 29), (14, 15), (14, 30), (15, 31), (16, 17), (16, 18), (16, 20), (16, 24), 
                (17, 19), (17, 21), (17, 25), (18, 19), (18, 22), (18, 26), (19, 23), (19, 27), (20, 21), (20, 22), 
                (20, 28), (21, 23), (21, 29), (22, 23), (22, 30), (23, 31), (24, 25), (24, 26), (24, 28), (25, 27), 
                (25, 29), (26, 27), (26, 30), (27, 31), (28, 29), (28, 30), (29, 31), (30, 31)]


    SPLIT=False
    if len(sys.argv) >=5:
        #0-179
        #v1 = [(1,3), (1,5), (1,9), (1,17, (1,-1))]
        v2 = [(2,3), (2,6), (2,10), (2,18), (2,-1)]
        v7 = [(3,7), (5,7), (6,7), (7,15), (7, 23), (7,-1)]
        v14 = [(12,14),(10,14), (6,14), (14,15), (14,30), (14,-1)] 
        partitions = list(itertools.product(v2,v7,v14))
        print(len(partitions))
        print(partitions)
        my_partition = list(partitions[int(sys.argv[4])])
        print(my_partition)
        SPLIT=True
    else:
        my_partition = None
        
    if SPLIT:
        outfile = open(working_dir + "performance.txt_" + sys.argv[3] + "_"+sys.argv[4], 'w')
    else:
        outfile = open(working_dir + "performance.txt_" + sys.argv[3], 'w')
    #else:
    #    infile = open(working_dir + "performance.txt_" + sys.argv[3], 'rb')
    
    forbidden_matchings = load_lists(working_dir + "forbidden_matchings")
    edges_in_cycle_count = int(math.pow(2,dims))
    cycles = open(working_dir + "cycles")
    
    count = 0
    stime = time.time()
    restricted = set()
    total = 0
    iters = 0
    old_count = 0
    lrest = 0
    prev_lrest = 0
    
    print("Iterating through cycles")

    for l in cycles:
        c = ast.literal_eval(l)
        iters+=1
        if iters - 1 == num_iters:
            break
        if iters %500 == 0:
            print(iters, lrest, lrest - prev_lrest)
            prev_lrest = lrest
        perm = compute_perm(c)
        matchings_perms = []
        
        for i in forbidden_matchings:
            i = sorted([(min(perm[u],perm[v]), max(perm[u],perm[v])) for (u,v) in i])
            if not check_maximal(c, i, q5_edges, my_partition):
                continue           
            i = sorted([simp_tuple(u,v) for (u,v) in i])             
            i = str(i).lstrip("[").rstrip("]").replace(" ","")
            matchings_perms.append(i)
        restricted.update(matchings_perms)
        lrest = len(restricted)
        l = lrest - old_count

        outfile.write(str(l)+"\n")
        old_count = lrest

        total += l

    outfile.close()
    print("RESTRICTED LENGTH: " + str(len(restricted)))
    print("TOTAL: " + str(total))
    print(time.time()- stime)
    