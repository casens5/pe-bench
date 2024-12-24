import os
import json
import sys
from argparse import ArgumentParser
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import (
    safe_builtins,
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence
)
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython.PrintCollector import PrintCollector
import math

def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    allowed_modules = {'math'}
    if name in allowed_modules:
        return __import__(name, globals, locals, fromlist, level)
    else:
        raise ImportError(f"Importing module '{name}' is not allowed.")

def execute_python_code(code):
    try:
        # Compile the code with RestrictedPython
        compiled_code = compile_restricted(
            code,
            '<string>',
            'exec'
        )

        if compiled_code is None:
            raise Exception("Compilation failed. Please check the code for syntax errors.")

        # Define allowed built-ins
        allowed_builtins = safe_builtins.copy()
        allowed_builtins.update({
            'sum': sum,
            'range': range,
            'len': len,
            'int': int,
            'float': float,
            'str': str,
            # Add other safe built-ins if necessary
        })

        # Create a restricted environment with custom __import__
        restricted_globals = {
            '__builtins__': allowed_builtins,
            '_getiter_': default_guarded_getiter,
            '_print_': PrintCollector,  # Handle print statements
            '__import__': safe_import,  # Override __import__
            '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
            '_unpack_sequence_': guarded_unpack_sequence,
            'math': math  # Pre-injected allowed module
        }

        # Execute the compiled code in the restricted environment
        exec(compiled_code, restricted_globals)

        # Retrieve the captured printed output
        output = restricted_globals.get('printed', '')

    except Exception as e:
        # Capture traceback for detailed error information
        import traceback
        error_trace = traceback.format_exc()
        output = f"Error executing code: {e}\nTraceback:\n{error_trace}"

    return output

def process_python_files(model_name):
    python_dir = os.path.join('solutions', model_name, 'python')
    solutions_json_path = os.path.join('solutions', model_name, 'solutions.json')

    if not os.path.exists(python_dir):
        raise Exception(f"Python directory {python_dir} does not exist.")

    solutions = {}
    python_files = sorted(os.listdir(python_dir))

    # Iterate over all Python files in the directory
    for python_file in python_files:
        if python_file.endswith('.py'):
            python_path = os.path.join(python_dir, python_file)

            with open(python_path, 'r', encoding='utf-8') as file:
                code = file.read()

            print(f"Loaded {python_file}:\n{code}\n")

            # Extract the problem number from the filename
            problem_number = os.path.splitext(python_file)[0]

            # Execute the code and capture the output
            output = execute_python_code(code)
            print(f"Executed {python_file}:\n{output}\n")

            # Store the result in the solutions dictionary
            solutions[problem_number] = output

    # Write the solutions to a JSON file after processing all files
    with open(solutions_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(solutions, json_file, indent=4)

    print(f"Executed all Python files and saved results to {solutions_json_path}")

def main():
    parser = ArgumentParser(description="Execute Python solutions and store results in a JSON file.")
    parser.add_argument('--model_name', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')

    args = parser.parse_args()

    model_name = args.model_name

    process_python_files(model_name)

if __name__ == "__main__":
    main()
