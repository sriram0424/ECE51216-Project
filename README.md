# ECE51216 Project: DPLL SAT Solver with Advanced Heursitics. 

This repository contains an implementation of a Conflict-Driven Clause Learning (CDCL) SAT solver written in Python as part of the Purdue University ECE51216 Final Project. The solver supports solving CNF formulas in DIMACS format, using modern DPLL-based techniques such as:
- Unit propagation
- Clause simplification
- MOM (Maximum Occurrence in clauses of Minimum size) heuristic
- Conflict analysis and clause learning
- Non-chronological backtracking

In addition, this repo includes a sat test script that allows you to automatically test your SAT solver against a folder of .cnf files and evaluate its correctness and runtime performance. 

## Features
### SAT Solver (sat_solver_h_MOM.py)
- DIMACS parser: Reads CNF files in standard SAT format.
- Unit propagation: Simplifies the clause set by propagating unit clauses.
- Heuristic-based decision making: MOM heuristic is used to decide which literal to branch on.
- Conflict analysis: Learns new clauses from conflicts using a simple last-decision blocking technique.
- Non-chronological backtracking: Jumps back to the second-highest decision level upon conflict.
- Random CNF generation: If no CNF file is provided, a 3-SAT instance is randomly generated.

### Benchmarking Script (sat_test_script.py): Used for testing purposes only
- Iterates through a directory of .cnf files
- Runs the SAT solver on each file
- Extracts runtime and validates correctness of output
- Reports:
- 
    -   Average runtime
    -   Max/min runtime
    -   Files with incorrect results
## How to Use
1. Ensure Python is installed
2. The python script can be run from the command window. To run the SAT Solver, specify the specific DIMACS CNF file as shown. Replace "example" with actual CNF file. 
      - **python sat_solver_h_MOM.py example.cnf**
3. If example DIMACS CNF files are not specified, the script will create a random 3-SAT problem, that it will then use to compute the result. If this is done, the output will let the user know this by first outputting: [Info] Using random generated variables, no CNF file. 
     - **python sat_solver_h_MOM.py **
4. After running the command above, the RESULT, ASSIGNMENT of variables, and runtime will be outputed. An example of this is shown below.  <br>
<br>Input: python sat_solver_h_MOM.py uf50-0998.cnf  <br>
RESULT:SAT  <br>
ASSIGNMENT:1=0 2=1 3=1 4=0 5=0 6=1 7=1 8=0 9=1 10=1 11=0 12=0 13=1 14=1 15=0 16=1 17=0 18=1 19=1 20=0 21=1 22=0 23=0 24=0 25=1 26=0 27=0 28=1 29=1 30=1 31=1 32=1 33=0 34=0 35=1 36=0 37=0 38=1 39=0 40=1 41=0 42=0 43=1 44=0 45=0 46=1 47=1 48=1 49=1 50=0  <br>
Runtime: 0.032429 seconds   <br> <br>
6. If wanted to perform further performance analysis, use the benchmark sat test script. This script can be run using the following command. Make sure to set the values at the top of the script as shown as well.
    - **python sat_test_script.py**
    <br>
    
    Note: In order to use the benchmark script, the following parameters need to be updated in the script.
    test_folder = 'UUF50.218.1000'   # Your test CNF folder  <br> 
    correct_result = 'SAT'           # Expected result for all test files  <br> 
    test_solver = 'sat_solver_h_MOM.py'  <br> 

## DIMACS Format Example
A valid CNF file in DIMACS format might look like this:  <br>
<br>
c This is a comment <br>
p cnf 3 2 <br> 
1 -3 0  <br> 
2 3 -1 0  <br> 
 
## Example Benchmark Output
<br>
This is an example output if the benchmark script was run. This script was mainly used for testing, comparing runtimes, and ensuring that the right output is outputed based on the input data set. <br>

There were 100 cases tested <br>
The average_runtime was 0.05341 <br>
The highest runtime was 0.08431 <br>
The lowest runtime was 0.03255 <br> 
All cases produced correct output <br>

## Example of sat_solver_h_MOM.py running on Command Prompt
![image](https://github.com/user-attachments/assets/ab5ac0de-052d-438f-b2e0-f272c8a339e7)
   

