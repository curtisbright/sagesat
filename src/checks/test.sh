#!/bin/bash

for i in 0 1 2 3 4 5 6 7
do
    python3 performance.py /home/ezulkosk/git/sagesat/results/performance/ 100 0 $i
done
