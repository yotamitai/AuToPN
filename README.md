# AuToPN

AuToPN is automatic process for generating Temporal Planning Networks (TPNs) from input temporal planning problems.

# Requirmrnts

## Packages
1) antlr4
pip install antlr4-python3-runtime

2) scipy
pip install scipy

3) numpy 1.15.4 (current issue with new version https://github.com/numpy/numpy/issues/14384 )
 pip install numpy==1.15.4

3) pymzn
pip install pymzn

4) networkx
pip install networkx

## software
1) Temporal Planner (optic) - must be placed in ../diverse_temporal/[name-of-planner]
2) Constrain Programing solver (Minizinc)


# Running
python main.py

## Custome domain and problem
requires a directory with the name of the domain to be placed in ../benchmarks/Temporal
domain file must be named 'domain.pddl'
problem file must be in same directory

