# ECE51216 Project: DPLL SAT Solver with Advanced Heursitics. 

This repository contains an implementation of a Conflict-Driven Clause Learning (CDCL) SAT solver written in Python. The solver supports solving CNF formulas in DIMACS format, using modern DPLL-based techniques such as:
- Unit propagation
- Clause simplification
- MOM (Maximum Occurrence in clauses of Minimum size) heuristic
- Conflict analysis and clause learning
- Non-chronological backtracking

In addition, this repo includes a sat test script that allows you to automatically test your SAT solver against a folder of .cnf files and evaluate its correctness and runtime performance.

**Repository Structure
.
├── sat_solver_h_MOM.py        # CDCL SAT solver using MOM heuristic
├── benchmark_runner.py        # Script to test solver on a batch of CNF files
├── UUF50.218.1000/            # Example folder containing CNF benchmarks (can be replaced)
└── README.md                  # This file

**Features
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

![image](https://github.com/user-attachments/assets/ab5ac0de-052d-438f-b2e0-f272c8a339e7)
