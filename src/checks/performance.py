

import ast
import math
import sys
import time


def load_lists(s,test=False, start_index=0, num_iters=-1):
    f = open(s,'r')
    retlist = []
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
        retlist.append(ast.literal_eval(line))
        
        if test and iters % 100 == 0:
            return retlist
    return retlist


def compute_perm(c):
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
    
    perm_dict = {}
    for i in range(len(perm)):
        perm_dict[i] = perm[i]
    return perm_dict

def simp_tuple(u,v):
    CONST=32
    return 32*u + v

if __name__ == '__main__':
    
    dims = 5
    working_dir = "/home/ezulkosk/git/sagesat/results/performance/"
 
    working_dir = sys.argv[1]
    num_iters = int(sys.argv[2])
    #which cycle to start at
    start_index = num_iters * int(sys.argv[3])
    outfile = open(working_dir + "performance.txt_" + sys.argv[3], 'w')
    
    retlist = load_lists(working_dir + "forbidden_matchings")
    #number of edges that must be in cycle
    edges_in_cycle_count = int(math.pow(2,dims))
    #remove the id's
    cycles = load_lists(working_dir + "cycles", test=False, start_index=start_index, num_iters=num_iters)
    
    count = 0
    stime = time.time()
    restricted = set()
    total = 0
    iters = 0
    old_count = 0
    news = []
    for c in cycles:
        iters+=1
        if iters %100 == 0:
            print(iters)
        perm = compute_perm(c)
        matchings_perms = []
        for i in retlist:
            i = sorted([simp_tuple(min(perm[u],perm[v]), max(perm[u],perm[v])) for (u,v) in i])
            #print(i)
            i = str(i).lstrip("[").rstrip("]").replace(" ","")
            matchings_perms.append(i)
            #print(i)
        curr_set = set(matchings_perms)
        restricted = restricted.union(curr_set)
        lrest = len(restricted)
        l = lrest - old_count
        #fprint(l)
        news.append(l)
        old_count = lrest
        
        #outfile.write(str(l) + "\n")
        total += l
    print("RESTRICTED LENGTH: " + str(len(restricted)))
    print("TOTAL: " + str(total))
    print(news)
    print(time.time()- stime)
     