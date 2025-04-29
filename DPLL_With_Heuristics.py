import sys
import time
import random
import os

# Parser for DIMACS input (clause, number of variables)
def parse_dimacs(file_content):
    clauses = [] #list to store clauses
    num_vars = 0 #initialize number of variables
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

# Unit Propagation (simplifies unit clauses with only one literal)
def unit_propagate(clauses, assignment):
    changed = True #initialze changed flag
    while changed:
        changed = False
        unit_clauses = [c for c in clauses if len(c) == 1] #finds the unit clauses based on length
        for unit in unit_clauses:
            lit = unit[0]
            if -lit in assignment: #if negation assigned, there is a conflict
                return None
            if lit not in assignment: #if unassigned, assign to true
                assignment.add(lit)
                changed = True
                clauses = simplify(clauses, lit)
                if clauses is None: #if conflict return none
                    return None
    return clauses, assignment 

# Clause Simplifciation (once literal assigned to true, removes clauses already assigned)
def simplify(clauses, lit):
    new_clauses = []
    for clause in clauses:
        if lit in clause: #skips satisfied clauses
            continue
        if -lit in clause: #removes -lit from clause
            new_clause = [l for l in clause if l != -lit]
            if not new_clause:
                return None
            new_clauses.append(new_clause) #add simplified clause
        else:
            new_clauses.append(clause) #clause unchanged, add it
    return new_clauses

# Pure Literal Elimination (safely assigns pure literals to true)
def find_pure_literals(clauses):
    counts = {}
    for clause in clauses:
        for lit in clause:
            counts[lit] = counts.get(lit, 0) + 1
    pure = set()
    for lit in counts:
        if -lit not in counts:
            pure.add(lit)
    return pure

# Conflict Analysis: learn a conflict clause
def analyze_conflict(assignment, decision_stack):
    learned_clause = [] #new learned clause
    for lit in decision_stack: #for every decision made, negate decision and add to learned clause
        learned_clause.append(-lit)
    return learned_clause

# Non-chronological Backjumping: deciding where to jump back
def backjump(learned_clause, decision_levels):
    levels = [] #list of decision levels for literals in learned clause
    for lit in learned_clause:
        levels.append(decision_levels.get(abs(lit), 0))
    if levels:
        return max(0, max(levels) - 1) #jump to one level before highest conflicting level
    return 0

# DPLL with CDCL and Non-Chronological Backtracking (Fixed)
def dpll(clauses, assignment, decision_stack=[], decision_levels={}):
    result = unit_propagate(clauses, assignment)
    if result is None:
        if not decision_stack:
            return None  # No decisions left, UNSAT
        learned_clause = analyze_conflict(assignment, decision_stack)
        clauses.append(learned_clause)
        backtrack_level = backjump(learned_clause, decision_levels)

        # Rebuild assignment and decision stack up to backtrack_level
        new_assignment = set()
        new_decision_stack = []
        new_decision_levels = {}

        for lit in assignment:
            var = abs(lit)
            if decision_levels.get(var, 0) <= backtrack_level:
                new_assignment.add(lit)
                if var in decision_levels:  # Only copy if exists
                    new_decision_levels[var] = decision_levels[var]

        for lit in decision_stack:
            var = abs(lit)
            if decision_levels.get(var, 0) <= backtrack_level:
                new_decision_stack.append(lit)

        return dpll(clauses, new_assignment, new_decision_stack, new_decision_levels)

    clauses, assignment = result

    if not clauses:
        return assignment  # SAT: all clauses satisfied

    # Apply pure literal elimination
    pure_literals = find_pure_literals(clauses)
    for lit in pure_literals:
        assignment.add(lit)
        clauses = simplify(clauses, lit)
        if clauses is None:
            return None  # Conflict from pure literal assignment

    # Pick next literal to branch on (unassigned)
    for clause in clauses:
        for lit in clause:
            if lit not in assignment and -lit not in assignment:
                for value in [lit, -lit]:  # Try literal True, then False
                    new_assignment = set()
                    for l in assignment:
                        new_assignment.add(l)
                    new_assignment.add(value)
                    new_clauses = simplify(clauses, value)
                    if new_clauses is not None:
                        new_decision_stack = []
                        for l in decision_stack:
                            new_decision_stack.append(l)
                        new_decision_stack.append(value)
                        new_decision_levels = {}
                        for var in decision_levels:
                            new_decision_levels[var] = decision_levels[var]
                        new_decision_levels[abs(value)] = len(new_decision_stack)
                        result = dpll(new_clauses, new_assignment, new_decision_stack, new_decision_levels)
                        if result is not None:
                            return result
                return None  # Both assignments failed
    return assignment

# Solver Logic
def solve_dimacs_cnf(dimacs_text):
    clauses, num_vars = parse_dimacs(dimacs_text)
    result = dpll(clauses, set())
    if result is None:
        print("RESULT:UNSAT")
    else:
        print("RESULT:SAT")
        assignment_output = []
        for var in range(1, num_vars + 1):
            if var in [abs(l) for l in result]:
                value = 1 if var in result else 0
            else:
                value = 1  # Unassigned → treat as True
            assignment_output.append(f"{var}={value}")
        print("ASSIGNMENT:" + " ".join(assignment_output))

# Random CNF Generator (not needed in final code)
def generate_random_3sat(num_vars, num_clauses):
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

# Main program entry
if __name__ == "__main__":
    start = time.time()  # Start timing

    # Generate a random 3-SAT problem based on function above
    print("Using a randomly generated CNF formula")
    dimacs_text = generate_random_3sat(5, 15)  # Generate CNF with x variables, y clauses

    solve_dimacs_cnf(dimacs_text)  # Solve the generated CNF

    end = time.time()  # End timing
    print(f"Runtime: {end - start:.6f} seconds")  # Output solving time
