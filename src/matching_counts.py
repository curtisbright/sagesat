'''
Created on Sep 20, 2014

@author: ezulkosk
'''

from common.common import Options
from main import run


if __name__ == '__main__':
    TEST_DIR = "../test/matching_counts/"
    options = Options()
    options.SHARPSAT=True
    print("Obtaining counts for hypercube matchings.")
    for d in range(2,6):
        d_dir = TEST_DIR + "d" + str(d) + "/"
        print("Dimension "+ str(d))
        
        spec = d_dir + "matchings"
        print("\tmatchings: " + str(run(spec, options)))
        
        spec = d_dir + "forbidden_matchings"
        print("\tforbidden matchings: " + str(run(spec, options)))
        
        spec = d_dir + "maximal_forbidden_matchings"
        print("\tmaximal forbidden matchings: " + str(run(spec, options)))
        
    