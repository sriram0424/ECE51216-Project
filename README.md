# ECE51216 Project: DPLL SAT Solver with Advanced Heursitics. 

This repository contains an implementation of a Conflict-Driven Clause Learning (CDCL) SAT solver written in Python. The solver supports solving CNF formulas in DIMACS format, using modern DPLL-based techniques such as:
- Unit propagation
- Clause simplification
- MOM (Maximum Occurrence in clauses of Minimum size) heuristic
- Conflict analysis and clause learning
- Non-chronological backtracking

In addition, this repo includes a sat test script that allows you to automatically test your SAT solver against a folder of .cnf files and evaluate its correctness and runtime performance. 

## Features
**SAT Solver (sat_solver_h_MOM.py)
- DIMACS parser: Reads CNF files in standard SAT format.
- Unit propagation: Simplifies the clause set by propagating unit clauses.
- Heuristic-based decision making: MOM heuristic is used to decide which literal to branch on.
- Conflict analysis: Learns new clauses from conflicts using a simple last-decision blocking technique.
- Non-chronological backtracking: Jumps back to the second-highest decision level upon conflict.
- Random CNF generation: If no CNF file is provided, a 3-SAT instance is randomly generated.

**Benchmarking Script (sat_test_script.py)
- Iterates through a directory of .cnf files
- Runs the SAT solver on each file
- Extracts runtime and validates correctness of output
- Reports:
- 
    -   Average runtime
    -   Max/min runtime
    -   Files with incorrect results
# How to Use
1. Ensure Python is installed
2. Run SAT Solver. Specify the specific DIMACS CNF file as shown. Replace "example" with actual CNF file. 
  ** python sat_solver_h_MOM.py exanmple.cnf**
4. If wanting to solve a random 3-SAT problem without a cnf, you do not need to include the cnf.
   ** python sat_solver_h_MOM.py **
6. If wanted to perform further performance analysis, use the benchmark sat test script. This script can be run using the following command. Make sure to set the values at the top of the script as shown as well.
   command: **python sat_test_script.py**
   
   test_folder = 'UUF50.218.1000'   # Your test CNF folder
   correct_result = 'SAT'           # Expected result for all test files
   test_solver = 'sat_solver_h_MOM.py'

**DIMACS Format Example
A valid CNF file in DIMACS format might look like this:
c This is a comment
p cnf 3 2
1 -3 0
2 3 -1 0

**Example Benchmark Output
There were 100 cases tested
The average_runtime was 0.05341
The highest runtime was 0.08431
The lowest runtime was 0.03255
All cases produced correct output

**Example of sat_solver_h_MOM.py running on PC
![image](https://github.com/user-attachments/assets/ab5ac0de-052d-438f-b2e0-f272c8a339e7)
   

