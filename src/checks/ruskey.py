'''
Created on Jan 5, 2015

@author: ezulkosk
'''

import ast
import math
import sys

from sqlalchemy.engine import create_engine
import sqlalchemy.sql

import sqlalchemy.databases.mysql as m


def get(conn, cols, table, test=False):
    #returns columns from the db
    s = sqlalchemy.sql.text("select " + ",".join(cols) + \
                            " from " + table + ";")
    res = conn.execute(s).fetchall()
    elems = []
    count = 0
    for i in res:
        #print(i)
        elems.append([ast.literal_eval(str(j)) for j in i])
        count += 1
        if count % 10000 == 0:
            print(count)
        if test and count % 10 == 0:
            return elems
    return elems

def hamming_distance(s1, s2):
    """ http://en.wikipedia.org/wiki/Hamming_distance """
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

if __name__ == '__main__':
    
    dims = 5
    engine = create_engine('mysql://ezulkosk@localhost/ruskey')
    conn = engine.connect()
    
    matchings_table = "matchings" + str(dims)
    cycles_table = "cycles" + str(dims)

    trans = conn.begin()
    try:
        '''
        We store the cycles and matchings in a mysql db.
        '''
        #number of edges that must be in cycle
        edges_in_cycle_count = int(math.pow(2,dims))
        #remove the id's
        cycles = [i for (_, i) in get(conn, ["id", "cycle"], cycles_table, test=False)]
        matchings = [i for (_, i) in get(conn, ["id", "matching"], matchings_table, test=False)]
        count = 0
        
        #actual check
        for (c,m) in zip(cycles, matchings):
            #ensure that the matching is a subset of the cycle
            if not set(m).issubset(c):
                sys.exit("Bug")
            #ensure that there are 2^n edges in the cycle
            if not len(c) == edges_in_cycle_count:
                sys.exit("Bug")
            #ensure that each edge in c is a valid hypercube edge (converting ints to binary)
            for (v1,v2) in c:
                b1 = ('{0:0' + str(dims) + 'b}').format(v1)
                b2 = ('{0:0' + str(dims) + 'b}').format(v2)
                #an edge is in the hypercube if its vertices differ by 1 in binary
                if hamming_distance(b1,b2) != 1:
                    sys.exit("Bug")
                #ensure that each vertex is a valid id for the hypercube
                if v1 < 0 or v2 < 0 or v1 > edges_in_cycle_count or v2 > edges_in_cycle_count:
                    sys.exit("Bug")
            #simple check to ensure that c is indeed a Hamiltonian cycle    
            visited = []
            (first_vertex, next) = c[0]
            c.pop(0)
            visited.append(first_vertex)
            while True:
                next_edges = [(v1,v2) for (v1,v2) in c if v1 == next or v2 == next]
                if len(next_edges) != 1:
                    if next == first_vertex and set(visited) == set(range(edges_in_cycle_count)):
                        break
                    else:
                        sys.exit("Bug in cycle detection")
                visited.append(next)
                (v1,v2) = next_edges[0]
                c.remove((v1,v2))
                if v1 == next:
                    next = v2
                else:
                    next = v1
            #progress counter
            count = count + 1
            if count % 500 == 0:
                print(count)
        print("Passed")
    except Exception as e:
        print(e)
        