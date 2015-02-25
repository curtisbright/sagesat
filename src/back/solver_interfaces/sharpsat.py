'''
Created on Oct 7, 2014

@author: ezulkosk
'''
from subprocess import Popen, PIPE

from common import common


def get_num_solutions(dimacs, options):
    #copy_file_with_extra_clauses(extra_clauses, opts)
    sharpsat_output = Popen([options.SHARPSAT_LOCATION + " " + dimacs], stderr=open("/dev/null", "w"),stdout=PIPE,shell=True)
    flag = False
    for line in sharpsat_output.stdout:
        line = str(line.decode("utf-8"))
        if flag:
            return int(line)
        if "solutions" in line:
            flag = True
    return 0