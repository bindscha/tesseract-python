#!/usr/bin/env bash

PYTHON_INTERPRETER="pypy3"

ALGORITHMS="clique cycle example motif"
NS="100 200 500 1000 2000 5000 10000"
MODES="static dynamic"
GRAPH="er"
MAX=5

for alg in $ALGORITHMS; do
    for n in $NS; do
        for mode in $MODES; do
            cmd="$PYTHON_INTERPRETER main.py -a $alg -g $GRAPH -m $mode --max $MAX -n $n --reset"
            echo "Running $cmd..."
            $cmd
        done
    done
done

