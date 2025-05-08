import sys
import time
import random
import os

# Program description: This program implements a SAT solver using the dpll algorithm.
# It takes a cnf formula and prints if it is SAT or UNSAT.
# If it is SAT, the assignments of the varibles are printed. 




def parse_dimacs(file_content):
    """Parser for DIMACS input

    Parameters:
      file_content: The content of the cnf file.

    Returns:
      clauses: A list of lists that represents the cnf formula.
      num_vars: The number of variables in the cnf formula.
    """
    clauses = []
    num_vars = 0
    for line in file_content.strip().split('\n'):
        line = line.strip()
        if line == '' or line.startswith('c'):
            continue
        if line.startswith('p'):
            _, _, num_vars, _ = line.split()
            num_vars = int(num_vars)
        else:
            clause = list(map(int, line.split()))
            clause = [lit for lit in clause if lit != 0]
            clauses.append(clause)
    return clauses, num_vars


def unit_propagate(clauses, assignment):
     """Implements unit propagation. This simplifies the unit clauses by
     assigning unate clauses to true.

    Parameters:
      clauses: A list of lists that represents the current state of the cnf formula.
      assignment: A set showing the variables that have been currently assigned.
      
    Returns:
      clauses: A list of lists that represents the cnf formula. 
      assignment: A set showing the variables that have been currently assigned.
    """
    changed = True
    while changed:
        changed = False
        unit_clauses = [c for c in clauses if len(c) == 1]
        for unit in unit_clauses:
            lit = unit[0]
            if -lit in assignment:
                return None
            if lit not in assignment:
                assignment.add(lit)
                changed = True
                clauses = simplify(clauses, lit)
                if clauses is None:
                    return None
    return clauses, assignment


def simplify(clauses, lit):
    """Implements clause simplification. Once a literal is assigned to true, 
    the clauses already assigned are removed.

    Parameters:
      clauses: A list of lists that represents the current state of the cnf formula.
      lit: The literal being simplified.
      
    Returns:
      new_clauses: A list of lists without the clauses that contain the literal
      and with all instances of the complement of the variable removed.
    """
    new_clauses = []
    for clause in clauses:
        if lit in clause:
            continue
        if -lit in clause:
            new_clause = [l for l in clause if l != -lit]
            if not new_clause:
                return None
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses

# Pure Literal Elimination (safely assigns pure literals to true)
def find_pure_literals(clauses):
    """Implements pure literal elimination. Pure literals are assigned to true.
    Pure literals are those that occur only in complemented or only in 
    uncomplemented form.
    
    Parameters:
      clauses: A list of lists that represents the current state of the cnf formula.
      
    Returns:
      pure: The of pure literals
    """
    counts = {}
    for clause in clauses:
        for lit in clause:
            counts[lit] = counts.get(lit, 0) + 1
    pure = set()
    for lit in counts:
        if -lit not in counts:
            pure.add(lit)
    return pure


def dpll(clauses, assignment):
    """Implements the dpll algorithm.
    
    Parameters:
      clauses: A list of lists that represents the current state of the cnf formula.
      assignment: A set showing the variables that have been currently assigned.
      
    Returns:
      assignment: A set showing the variables that satisfy the cnf formula.
      If none is returned, then the formula is UNSAT.
    """
    result = unit_propagate(clauses, assignment)
    if result is None:
        return None
    clauses, assignment = result

    if not clauses:
        return assignment

    pure_literals = find_pure_literals(clauses)
    for lit in pure_literals:
        assignment.add(lit)
        clauses = simplify(clauses, lit)
        if clauses is None:
            return None

    for clause in clauses:
        for lit in clause:
            if lit not in assignment and -lit not in assignment:
                for value in [lit, -lit]:
                    new_assignment = set(assignment)
                    new_assignment.add(value)
                    new_clauses = simplify(clauses, value)
                    if new_clauses is not None:
                        result = dpll(new_clauses, new_assignment)
                        if result is not None:
                            return result
                return None
    return assignment


def solve_dimacs_cnf(dimacs_text):
    """Solver logic
    
    Parameters:
      dimacs_text: The content of the cnf file.
      
    Returns:
      None
    """
    clauses, num_vars = parse_dimacs(dimacs_text)
    result = dpll(clauses, set())
    if result is None:
        print("RESULT:UNSAT")
    else:
        print("RESULT:SAT")
        assignment_output = []
        for var in range(1, num_vars + 1):
            value = 1 if var in result else 0
            assignment_output.append(f"{var}={value}")
        print("ASSIGNMENT:" + " ".join(assignment_output))


'''
# Random CNF Generator
def generate_random_3sat(num_vars=50, num_clauses=200):
    clauses = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, num_vars)
            lit = var if random.random() < 0.5 else -var
            clause.add(lit)
        clauses.append(" ".join(map(str, clause)) + " 0")
    header = f"p cnf {num_vars} {num_clauses}"
    return "\n".join(["c Random 3-SAT benchmark"] + [header] + clauses)

# Main Entry Point
if __name__ == "__main__":
    start = time.time() #For tracking run time

    if len(sys.argv) == 2: #If CNF File is used
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' not found.")
            sys.exit(1)
        with open(filepath, 'r') as f:
            dimacs_text = f.read()
    else:
        print("[Info] Using random generated variables, no CNF file")
        dimacs_text = generate_random_3sat(50, 200) #If no CNF file do random assignment
        
    solve_dimacs_cnf(dimacs_text)

    end = time.time()
    print(f"Runtime: {end - start:.6f} seconds")
'''
