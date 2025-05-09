# Program description: This program implements a SAT solver using dpll and heuristics.
# Heuristics used are conflict driven learning, non-chrolological backtracking,
# and MOM branching. It takes a formula in cnf format and prints if it is SAT or UNSAT.
# If it is SAT, the assignments of the varibles are printed. 


import sys
import time
import random
import os


def parse_dimacs(file_content):
    
    # Note: ChatGPT was used to assist with parsing of DIMACS CNF file
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
        if line == '' or line.startswith('c') or line.startswith('%'):
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


def decide_literal(clauses, assignment):
    """Implements the MOM (Maximum Occurrence of clauses of Minimum size) heuristic
    to decide the literal to branch on.
    
    Parameters:
      clauses: A list of lists that represents the current state of the cnf formula.
      assignment: A set showing the variables that have been currently assigned.
      
    Returns:
      lit_choice: The chosen literal to branch on.
    """
    literal_assignments = [abs(l) for l in assignment]
    min_size = min((len(c) for c in clauses if c), default=0)
    counts = {}

    for clause in clauses:
        if len(clause) == min_size:
            for lit in clause:
                if abs(lit) not in literal_assignments:
                    if lit not in counts and -lit not in counts:
                        counts[lit] = 0
                        counts[-lit] = 0
                    elif lit not in counts:
                        counts[lit] = 0
                    counts[lit] += 1

    if not counts:
        return None

    vars = [abs(lit) for lit in counts]
    score_vals = []

    for lit in vars:
        num_uncomp = counts[lit]
        num_comp = counts[-lit]
        score_vals.append(((num_uncomp + num_comp)) * (2 ** min_size) + (num_uncomp * num_comp))

    lit_choice = vars[score_vals.index(max(score_vals))]
    return lit_choice


# Conflict Clause analysis and backtracking (heuristics)
# Pure Literal Elimination from regular DPLL removed due to clause learning implementation

def analyze_conflict(decision_stack):
    """Conflict analysis to compute the learned clause.
    
    Parameters:
      decision_stack: The stack of free decisions.
      
    Returns:
      The learned clause from the conflict.
    """
    if decision_stack:
        return [-decision_stack[-1]]  # Block last decision
    return []


def backtrack(decision_stack, assignment, decision_levels, learned_clause):
    """Decides how far to backtrack based on the decision levels of the literals 
    present in the learned clause. The function jumps back to the second-highest 
    level from where an issue has occurred.
    
    Parameters:
      decision_stack: The stack of free decisions.
      assignment: A set showing the variables that have been currently assigned.
      decision_levels: A dictionary that shows the decsion level where each free
      decision was made.
      learned_clause: The clause learned from conflict analysis.
      
    Returns:
      The second-highest level from where an issue has occurred.
    """
    levels = []
    for l in learned_clause:
        level = decision_levels.get(abs(l), 0)
        levels.append(level)

    if len(levels) <= 1:
        return 0

    levels.sort()
    return max(levels[:-1])  # second-highest level


# CDCL-based DPLL solver with conflict-driven clause learning and non-chronological backtracking

def dpll_cdcl(clauses, assignment, decision_stack=[], decision_levels={}, level=0,
              learned_clauses=set()):
    """Implements the dpll algorithm using a cdcl approach with conflict-driven clause learning,
    and non-chronological backtracking.
    
    Parameters:
      clauses: A list of lists that represents the current state of the cnf formula.
      assignment: A set showing the variables that have been currently assigned.
      decision_stack: A stack of the free decisions made, implemented using a list.
      decision_levels: A dictionary that shows the decsion level where each free
      decision was made.
      level: An integer that shows the current decision level.
      learned_clauses: A set of the clauses that have been learned through 
      conflict-driven learning.
      
    Returns:
      assignment: A set showing the variables that satisfy the cnf formula.
      If none is returned, then the formula is UNSAT.
    """
    # Perform unit propagation on the current clause set and assignment
    result = unit_propagate(clauses, assignment.copy())

    # If conflict detected during propagation
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
        return dpll_cdcl(clauses, new_assignment, new_decision_stack, new_decision_levels,
                         bj_level + 1, learned_clauses)

    clauses, assignment = result

    if not clauses:
        return assignment  # All clauses satisfied

    # Choose an unassigned literal and try both True and False assignments (decision branching)
    lit = decide_literal(clauses, assignment)


    if lit == None:
        return assignment
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
            result = dpll_cdcl(new_clauses, new_assignment, new_stack, new_levels,
                               level + 1, learned_clauses.copy())
            if result is not None:
                return result
        return None
    return assignment


def solve_dimacs_cnf(dimacs_text):
    """Solving dimacs formatted input
    
    Parameters:
      dimacs_text: The content of the cnf file.
      
    Returns:
      None
    """
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


# --- Main Entry Point ---
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
        dimacs_text = generate_random_3sat(200, 800)

    solve_dimacs_cnf(dimacs_text)

    end = time.time()

#Uncomment line below to output runtime
    #print(f"Runtime: {end - start:.6f} seconds")

