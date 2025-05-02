import sys
import time
import random
import os

# Parser for DIMACS input

def parse_dimacs(file_content):
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

# Unit Propagation (simplifies unit clauses with only one literal)

def unit_propagate(clauses, assignment):
    while True:
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            break
        for clause in unit_clauses:
            lit = clause[0]
            if -lit in assignment:
                return None
            assignment.add(lit)
            clauses = simplify(clauses, lit)
            if clauses is None:
                return None
    return clauses, assignment

# Clause Simplifciation (once literal assigned to true, removes clauses already assigned)
def simplify(clauses, lit):
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

#Conflict Clause analysis and backtracking (heuristics)
# Pure Literal Elimination from regular DPLL removed due to clause learning implementation

def analyze_conflict(decision_stack):
    if decision_stack:
        return [-decision_stack[-1]]  # Block last decision
    return []

def backtrack(decision_stack, assignment, decision_levels, learned_clause):
    levels = []
    for l in learned_clause:
        level = decision_levels.get(abs(l), 0)
        levels.append(level)

    if len(levels) <= 1:
        return 0

    levels.sort()
    return max(levels[:-1])  # second-highest level

# CDCL-based DPLL solver with conflict-driven clause learning and non-chronological backtracking

def dpll_cdcl(clauses, assignment, decision_stack=[], decision_levels={}, level=0, learned_clauses=set()):
    # Perform unit propagation on the current clause set and assignment
    result = unit_propagate(clauses, assignment.copy())
    
    #If conflict detected during propagation
    if result is None:
        if not decision_stack:
            return None  # No more decisions to backtrack then UNSAT

        learned_clause = analyze_conflict(decision_stack)
        clause_key = tuple(sorted(learned_clause))

        # Avoid looping on the same learned clause
        if clause_key in learned_clauses:
            return None

        learned_clauses.add(clause_key)
        clauses.append(learned_clause)
        bj_level = backtrack(decision_stack, assignment, decision_levels, learned_clause)

        # Backtrack state
        new_assignment = set()
        new_decision_stack = []
        new_decision_levels = {}
        for lit in assignment:
            level_lit = decision_levels.get(abs(lit), 0)
            if level_lit <= bj_level:
                new_assignment.add(lit)
                new_decision_levels[abs(lit)] = level_lit

        for lit in decision_stack:
            if decision_levels.get(abs(lit), 0) <= bj_level:
                new_decision_stack.append(lit)

        # Try assigning learned clause 
        if not learned_clause:
            return None  # return none if there is nothing to learn

        new_lit = learned_clause[0]
        new_assignment.add(new_lit)
        new_decision_stack.append(new_lit)
        new_decision_levels[abs(new_lit)] = bj_level + 1
        
        # Recurse with updated state
        return dpll_cdcl(clauses, new_assignment, new_decision_stack, new_decision_levels, bj_level + 1, learned_clauses)

    clauses, assignment = result

    if not clauses:
        return assignment  # All clauses satisfied

    # Choose an unassigned literal and try both True and False assignments (decision branching)
    for clause in clauses:
        for lit in clause:
            if lit not in assignment and -lit not in assignment:
                for val in [lit, -lit]:
                    new_assignment = set(assignment)
                    new_assignment.add(val)
                    new_clauses = simplify(clauses, val)
                    if new_clauses is None:
                        continue
                    new_stack = decision_stack + [val]
                    new_levels = dict(decision_levels)
                    new_levels[abs(val)] = level + 1
                    result = dpll_cdcl(new_clauses, new_assignment, new_stack, new_levels, level + 1, learned_clauses.copy())
                    if result is not None:
                        return result
                return None
    return assignment

#Solving dimacs formatted input
def solve_dimacs_cnf(dimacs_text):
    clauses, num_vars = parse_dimacs(dimacs_text)
    result = dpll_cdcl(clauses, set())
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
# --- Optional: Random CNF generator ---
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
    return "\n".join(["c Random 3-SAT benchmark", header] + clauses)

# --- Main Entry Point ---
    

if __name__ == "__main__":
    start = time.time()

    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' not found.")
            sys.exit(1)
        with open(filepath, 'r') as f:
            dimacs_text = f.read()
    else:
        print("[Info] Using random generated variables, no CNF file")
        dimacs_text = generate_random_3sat(50, 200)

    solve_dimacs_cnf(dimacs_text)

    end = time.time()
    print(f"Runtime: {end - start:.6f} seconds")
'''
