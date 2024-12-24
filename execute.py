import os
import json
import sys
from argparse import ArgumentParser
from io import StringIO
from contextlib import redirect_stdout
import traceback

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

def execute_python_code(code):
    # Define allowed built-ins (modify as needed)
    allowed_builtins = {
        'print': print,
        'range': range,
        'len': len,
        'int': int,
        'float': float,
        'str': str,
        'sum': sum,
        # Add other safe built-ins as necessary
    }

    # Define allowed modules (modify as needed)
    allowed_modules = {
        'math': __import__('math'),
        # Add other allowed modules here
    }

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
    return output


def process_psolutions(model_name, language):
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

        output = ""
        if language == 'python':
            with open(solution_code_path, 'r', encoding='utf-8') as file:
                code = file.read()

            # Execute the code and capture the output
            output = execute_python_code(code)

        # if the output has several lines, we only want the last one
        print(f"Executed {solution_code}, raw output:{output}")
        output = output.split('\n')[-1]
        print(f"Executed {solution_code}:{output}")
        solutions[problem_number] = output

        # Write the solutions to a JSON file after processing all files
        with open(solutions_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(solutions, json_file, indent=4)

    print(f"Executed all Python files and saved results to {solutions_json_path}")

def main():
    parser = ArgumentParser(description="Execute solutions and store results in a JSON file.")
    parser.add_argument('--model_name', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--language', required=False, default='python', help='Name of the programming language to use, default is python')

    args = parser.parse_args()
    model_name = args.model_name
    language = args.language

    process_psolutions(model_name, language)

if __name__ == "__main__":
    main()
