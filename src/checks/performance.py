

import ast
import math
import struct
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
    #if u == 1 and v > 9:
    #    sys.exit(str(u) + " " + str(v))
    #mailreturn (u,v)
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

if __name__ == '__main__':
    
    dims = 5
    working_dir = "/home/ezulkosk/git/sagesat/results/performance/"
 
    working_dir = sys.argv[1]
    num_iters = int(sys.argv[2])
    #which cycle to start at
    start_index = num_iters * int(sys.argv[3])
    
    SPLIT=False
    if len(sys.argv) >=5:
        #0-7
        partitions = [(1,3), (1,5), (1,9), (1,17), (2,-1), (3,-1), (4,-1), (5,-1)]
        SPLIT=True
        pu = partitions[int(sys.argv[4])][0]
        pv = partitions[int(sys.argv[4])][1]
    
    #dump_matchings = False
    #if dump_matchings:
    if SPLIT:
        outfile = open(working_dir + "performance.txt_" + sys.argv[3] + "_"+sys.argv[4], 'w')
    else:
        outfile = open(working_dir + "performance.txt_" + sys.argv[3], 'w')
    #else:
    #    infile = open(working_dir + "performance.txt_" + sys.argv[3], 'rb')
    
    retlist = load_lists(working_dir + "forbidden_matchings")
    #for i in retlist:
    #    print(i)
    #sys.exit()
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
    #news = []
    
    
    for c in cycles:
        iters+=1
        if iters %1000 == 0:
            print(iters)
        perm = compute_perm(c)
        matchings_perms = []
        for i in retlist:
            i = sorted([(min(perm[u],perm[v]), max(perm[u],perm[v])) for (u,v) in i])
            #print(i)
            if SPLIT:
                in_partition = check_partner(i[0], pu, pv)
                if not in_partition:
                    continue   
            i = sorted([simp_tuple(u,v) for (u,v) in i])             
            i = str(i).lstrip("[").rstrip("]").replace(" ","")
            matchings_perms.append(i)
            #print(i)
    
        curr_set = set(matchings_perms)
        restricted.update(matchings_perms)#union(curr_set)
        lrest = len(restricted)
        l = lrest - old_count
        #fprint(l)
        #news.append(l)
        outfile.write(str(l)+"\n")
        old_count = lrest
        
        #outfile.write(str(l) + "\n")
        total += l
        
        '''
        curr_set = set(matchings_perms)
        restricted = restricted.union(curr_set)
        lrest = len(restricted)
        l = lrest - old_count
        #fprint(l)
        news.append(l)
        old_count = lrest
        
        #outfile.write(str(l) + "\n")
        total += l
        '''
    #outfile.write(str(news)+"\n")
    print("RESTRICTED LENGTH: " + str(len(restricted)))
    print("TOTAL: " + str(total))
    #for i in news:
        
        
    #print(news)
    print(time.time()- stime)
    