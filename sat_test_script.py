import subprocess
from pathlib import Path
import time

# Configurations
# Change test_folder to the folder with the files in cnf format used for testing
# Change correct_result to SAT or UNSAT. All files in the folder should have the same satisfiability
# Change test_solver to the file name of the sat solver being tested
test_folder = 'UUF50.218.1000'
correct_result = 'SAT'
test_solver = 'sat_solver_h_MOM.py'

# Initialization
folder = Path(test_folder)
track = 0
runtimes = []
min_time = float('inf')
max_time = 0
incorrect_cases = []

# Loop through each test file and run the solver
for file_path in folder.iterdir():
    track += 1
    if file_path.is_file():
        cmd_input = ['python3', test_solver, file_path]
        result = subprocess.run(cmd_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        sat_output = result.stdout

        # Parse runtime from output 
        if correct_result == 'SAT':
            if len(result.stdout.split('\n')) != 4:
                file_time = float(result.stdout.split('\n')[1].split(' ')[-2])
                incorrect_cases.append(file_time)
            else:
                file_time = float(result.stdout.split('\n')[2].split(' ')[-2])
        if correct_result == 'UNSAT':
            if len(result.stdout.split('\n')) != 3:
                file_time = float(result.stdout.split('\n')[2].split(' ')[-2])
                incorrect_cases.append(file_time)
            else:
                file_time = float(result.stdout.split('\n')[1].split(' ')[-2])

        runtimes.append(file_time)

        # Check correctness of solver result
        actual_result = result.stdout.split('\n')[0].split(' ')[-1]
        if actual_result != 'RESULT:' + correct_result:
            incorrect_cases.append(file_path)

        # Update runtime statistics
        max_time = max(max_time, file_time)
        min_time = min(min_time, file_time)

# Compute average runtime
average_runtime = sum(runtimes) / len(runtimes)

# Print summary
print(f'There were {track} cases tested')
print(f'The average_runtime was {average_runtime}')
print(f'The highest runtime was {max_time}')
print(f'The lowest runtime was {min_time}')

if not incorrect_cases:
    print('All cases produced correct output')
else:
    print('Incorrect cases at the following file paths:')
    for test_idx in incorrect_cases:
        print(f' {test_idx},')
