import sys
import time
import random
import os


#clauses -> each grouping
#assignment -> assignment to each variable

# Unit Propagation (simplifies unit clauses with only one literal)
# need to update trail
def unit_propagate(clauses, assignment):
    changed = True
    conflict = ''
    while changed:
        changed = False
        unit_clauses = [c for c in clauses if len(c) == 1 and c != [0]]
        for unit in unit_clauses:
            lit = unit[0]
            if -lit in assignment:
                conflict = lit
                return None, assignment, conflict
            if lit not in assignment:
                assignment.append(lit)
                changed = True
                clauses, conflict = simplify(clauses, lit)
                if clauses is None:
                    return None, assignment, conflict

    return clauses, assignment, conflict


# Clause Simplifciation (once literal assigned to true)
# if literal assigned set to 0. All literals that are 0 have satsifed the clause
# need to update trail
def simplify(clauses, value, trail, initial_clauses):
    conflict = ''
    new_clauses = []
    for clause in clauses:
        if lit in clause or clause == [0]:
            new_clauses.append([0])
            continue
        if -lit in clause:
            new_clause = [l for l in clause if l != -lit]
            if not new_clause:
                conflict = lit
                return None, conflict
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return new_clauses, conflict





"""purpose: compute the conflict clause and obtain the backtrack level

inputs: conflict: the literal responsible for the conflict, clause1: one of the clauses responsible
for the conflict (in initial form), clause2: other clause responsible for conflict, decision:
stack of free decisions, assignment: stack of all assignments made (free and forced)

outputs: conflict clause and backtrack level"""


def conflict_analysis(conflict, clause1, clause2, decision, assignment):
    conflict_clause1 = [x for x in clause1 if abs(x) != abs(conflict)]
    conflict_clause2 = [x for x in clause2 if abs(x) != abs(conflict)]
    conflict_clause = list(set(conflict_clause1 + conflict_clause2))

    conflict_temp = conflict_clause
    conflict_clause = list(set([-x for x in conflict_clause if x != conflict]))
    backtrack_level = 0

    for i in range(len(assignment) - 2, -1, -1):
        if len(conflict_temp) == 0:
            break

        if i == 0:
            if assignment[i] in conflict_temp or -assignment[i] in conflict_temp:
                backtrack_level += 1
        else:
            if assignment[i] in conflict_temp:
                conflict_temp.remove(assignment[i])

            elif -assignment[i] in conflict_temp:
                conflict_temp.remove(-assignment[i])

            if len(conflict_temp) == 0:
                break

            if assignment[i + 1] in decision:
                backtrack_level += 1

    return backtrack_level, conflict_clause


"""purpose: update clauses, assignment, prev_clauses, and decision using the backtrack level

inputs: backtrack_level: the number of times backtracking should occur, clauses: the current state
of each clause in the CNF formula, assignment: stack of all assignments made (free and forced),
prev_clauses: stack of the state of clauses after each free decision, decision: stack of free decisions

outputs: clauses, assignment, prev_clauses, decision"""

def backtrack(backtrack_level, clauses, assignment, prev_clauses, decision):
    for i in range(backtrack_level):
        for j in assignment:
            if j == decision[-1]:
                assignment.pop()
                break
            else:
                assignment.pop()


        decision.pop()
        prev_clauses.pop()

    clauses = prev_clauses[-1]


    return clauses, assignment, prev_clauses, decision



"""functions that will be added: chose literal: currently just pick the first one
conflict: when conflict occurs add all the steps in the conflict analysis and backtracking. The
code is already done for one branch but will improve readability since will occur for multiple brances"""


# DPLL Clauses
"""inputs: clauses: initial list of clauses, assignment: empty list of assignments, num_vars: total number of 
different absolute value of variables in clauses
returns None if Unsat and assignments in the form of a set if SAT"""


def cdcl(clauses, assignment, num_vars):

    initial_clauses = clauses


    #unit propogate
    clauses, assignment, conflict = unit_propagate(current_clauses, assignment)

    if conflict:
        return None

    #gives decision level
    dl = 0

    # stack of the free decisions. Each time a free decsion is made add the literal to the stack
    decision = []


    # shows which clause forced each decision -> trail[node] = intial_clauses[clause], if free decison -> trail[node] = 0
    trail = {}

    #stack with the state of the clauses list at each free decision. Each time a free decision is made add clauses to stack
    prevclauses = []

    while len(assignments) < num_vars:
        backtrack = False
        for clause in clauses:
            for lit in clause:
                if lit != 0 and lit not in assignment and -lit not in assignment:
                    dl = dl + 1
                    decision.append(lit)
                    prevclauses.append([clauses])
                    new_assignment = assignment
                    new_assignment.append(lit)
                    clauses, conflict, trail = simplify(clauses, value, trail, initial_clauses)
                    if conflict is None:
                        clauses, assignment, conflict = unit_propagate(clauses, assignment)
                        if conflict is None:
                            pass
                            #integrate pure here
                            if conflict is None:
                                continue
                            else:
                                pass
                                #repeat conflict analysis and backtracking
                        else:
                            pass
                            #repeat conflict analysis and backtracking


                    else:
                        #will create function of this branch to put in for unit propagate and pure branches above
                        backtrack_level, conflict_clause = conflict_analysis(conflict, clause1, clause2, decision, assignment)
                        if backtrack_level < 0:
                            return None
                        else:
                            clauses, assignment, prev_clauses, decision = backtrack(backtrack_level, clauses, assignment, prev_clauses, decision)

                            clauses.append(conflict_clause)
                            backtrack = True
                            dl -= backtrack_level
                            if dl < 0:
                                return None
                            break
            if backtrack == True:
                break

    assignment = set(assignment)

