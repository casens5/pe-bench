import os
import json
from argparse import ArgumentParser
from io import StringIO
from contextlib import redirect_stdout
import traceback
import builtins
import multiprocessing

def get_extension(language):
    if language == 'c': return 'c'
    elif language == 'r': return 'r'
    elif language == 'go': return 'go'
    elif language == 'c++': return 'cpp'
    elif language == 'lua': return 'lua'
    elif language == 'java': return 'java'
    elif language == 'lisp': return 'lisp'
    elif language == 'rust': return 'rs'
    elif language == 'ruby': return 'rb'
    elif language == 'perl': return 'pl'
    elif language == 'python': return 'py'
    elif language == 'prolog': return 'pl'
    elif language == 'matlab': return 'matlab'
    elif language == 'kotlin': return 'kt'
    elif language == 'fortran': return 'f'
    elif language == 'javascript': return 'js'
    else:
        raise Exception(f"Unsupported language: {language}")

def execute_python_code_worker(code, output_queue):
    # Define allowed built-ins
    safe_builtins = [
        'print', 'range', 'len', 'int', 'float', 'str', 'sum', 'chr',
        'enumerate', 'sorted', 'reversed', 'zip', 'map', 'filter',
        'any', 'all', 'min', 'max', 'abs', 'pow', 'round', 'ord', 
        'list', 'dict', 'set', 'tuple', 'type', 'isinstance', 'bin',
    ]
    allowed_builtins = {name: getattr(builtins, name) for name in safe_builtins}

    # Define allowed modules
    allowed_module_names = ['math', 'itertools', 'random']  # Add more as needed
    allowed_modules = {name: __import__(name) for name in allowed_module_names}

    # Custom __import__ function to restrict imports
    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in allowed_modules:
            return allowed_modules[name]
        else:
            raise ImportError(f"Importing module '{name}' is not allowed.")

    # Define the restricted global environment
    restricted_globals = {
        '__builtins__': allowed_builtins,
        '__import__': safe_import,
    }

    # Capture the output
    f = StringIO()
    try:
        with redirect_stdout(f):
            exec(code, restricted_globals)
        output = f.getvalue()
    except Exception as e:
        # Capture the traceback
        error_trace = traceback.format_exc()
        output = f"Error executing code: {e}\nTraceback:\n{error_trace}"
    output_queue.put({"output": output})

def execute_python_code(code, timeout=10):
    output_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=execute_python_code_worker, args=(code, output_queue))
    process.start()
    process.join(timeout)
    
    if process.is_alive():
        process.terminate()
        process.join()
        return "Error: Code execution timed out."
    
    try:
        result = output_queue.get_nowait()
        if "output" in result:
            return result["output"]
        elif "error" in result:
            return result["error"]
        else:
            return "Error: Unknown issue occurred during code execution."
    except multiprocessing.queues.Empty:
        return "Error: No output received from the executed code."

def process_solutions(model_name, language, max_problem_number):
    results_dir = os.path.join('solutions', model_name, language)
    solutions_json_path = os.path.join('solutions', model_name, language, 'solutions.json')
    extension = get_extension(language)

    if not os.path.exists(results_dir):
        raise Exception(f"Directory '{results_dir}' does not exist.")

    solutions = {}
    python_files = sorted(os.listdir(results_dir))
    for solution_code in python_files:
        if not solution_code.endswith('.' + extension): continue
        solution_code_path = os.path.join(results_dir, solution_code)
        print(f"Processing for execution: {solution_code_path}")
        extlen = len(extension) + 1
        problem_number = solution_code[:-extlen]  # Remove extension
        if int(problem_number) > max_problem_number: break

        output = ""
        if language == 'python':
            with open(solution_code_path, 'r', encoding='utf-8') as file:
                code = file.read()

            # Execute the code and capture the output
            output = execute_python_code(code)
            #print(f"Executed {code}, raw output:{output}")
       
        # if the output has several lines, we only want the last one
        #print(f"Executed {solution_code}, raw output:{output}")
        output = output.strip().split('\n')[-1]
        print(f"Executed {solution_code}:{output}")
        solutions[problem_number] = output

        # Write the solutions to a JSON file. We write this after each solution to avoid losing progress.
        with open(solutions_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(solutions, json_file, indent=4)

    print(f"Executed all Python files and saved results to {solutions_json_path}")
    return solutions

def main():
    parser = ArgumentParser(description="Execute solutions and store results in a JSON file.")
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--language', required=False, default='python', help='Name of the programming language to use, default is python')
    parser.add_argument('--n100', action='store_true', help='only 100 problems') # this is the default
    parser.add_argument('--n200', action='store_true', help='only 200 problems')
    parser.add_argument('--n400', action='store_true', help='only 400 problems')
    parser.add_argument('--nall', action='store_true', help='all problems')

    args = parser.parse_args()
    model_name = args.model
    language = args.language
    max_problem_number = 100
    if args.n100: max_problem_number = 100
    if args.n200: max_problem_number = 200
    if args.n400: max_problem_number = 400
    if args.nall: max_problem_number = 9999

    solutions = process_solutions(model_name, language, max_problem_number)

    if len(solutions) == max_problem_number:
        # evaluate the solutions by comparing with the expected results
        with open('solutions.json', 'r', encoding='utf-8') as json_file:
            expected_solutions = json.load(json_file)
        points = 0.0
        count = 0
        for problem_number in solutions:
            if problem_number not in expected_solutions:
                print(f"Problem {problem_number} not found in expected solutions.")
                continue
            expected = expected_solutions[problem_number]
            solution = solutions[problem_number]
            expected_solution = expected['solution']
            if solution == expected_solution:
                points += expected_solutions[problem_number]['points']
            count += 1

        points = round(points / count, 2)
        print(f"Points: {points}")

        # open the benchmark file and update the points
        benchmark_file = 'benchmark.json'
        benchmark = {}
        with open(benchmark_file, 'r', encoding='utf-8') as json_file:
            benchmark = json.load(json_file)

        # update the benchmark entry
        entry = benchmark.get(model_name, {})
        series_name = f"{language}-{max_problem_number}"
        entry[series_name] = points
        benchmark[model_name] = entry

        # sort the benchmark with the highest points first, use the series name "python-100" as the key
        sorted_benchmark = dict(sorted(benchmark.items(), key=lambda item: -item[1].get("python-100", 0)))

        # write the updated benchmark file
        with open(benchmark_file, 'w', encoding='utf-8') as json_file:
            json.dump(sorted_benchmark, json_file, indent=4)
    else:
        print("Not all solutions were executed, so the benchmark was not updated.")

if __name__ == "__main__":
    main()
