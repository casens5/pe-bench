from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import json
import sys
import io
import re
import subprocess
import signal
from contextlib import contextmanager


def install_missing_packages(code: str):
    """
    Scan the code for import statements, determine if each package is installed,
    and install it via pip if not.
    """
    # Regex patterns for import lines:
    # - Pattern 1 matches: import package[.subpackage] [as alias][, package2 [as alias2], ...]
    # - Pattern 2 matches: from package import something
    pattern_import = (
        r"^\s*import\s+((?:[a-zA-Z0-9_]+(?:\s+as\s+[a-zA-Z0-9_]+)?(?:\s*,\s*)?)+)"
    )
    pattern_from = r"^\s*from\s+([a-zA-Z0-9_]+)\s+import\s+"

    packages_to_install = set()
    for line in code.splitlines():
        # Check "import foo[, bar]"
        match_import = re.match(pattern_import, line)
        if match_import:
            # Split multiple imports and handle 'as' aliases
            imports = match_import.group(1).split(",")
            for imp in imports:
                # Take just the package name, before any 'as' statement
                package = imp.strip().split(" as ")[0].strip()
                packages_to_install.add(package)
            continue

        # Check "from foo import bar"
        match_from = re.match(pattern_from, line)
        if match_from:
            packages_to_install.add(match_from.group(1))

    # Attempt to import each package, install if that fails
    for package in packages_to_install:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing missing package: {package}")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package], check=True
            )


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def log_to_file(text: str, filename: str = "log.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{text}\n")


def test_problem(problem, model_name):
    print("beginning problem ", problem["id"], "\n\n")
    template = """
        Solve this math/programming challenge by writing a python script.  You can import any packages you need.  Solutions are allowed 60 seconds to run using moderate hardware.  Format your solution like this:

        SOLUTION:
        ```
        def solution():
            # your solution here
            return answer
        ```

        Question: {question}
    """
    if "supplement" in problem:
        if "supplement_2" in problem:
            template += """
            the additional data required to solve the problem are plaintext strings in the namespace as `SUPPLEMENT` and `SUPPLEMENT_2`.  here are some snippets of the first 1000 characters of the data:
            `SUPPLEMENT`:
            ```
            {supplement}
            ```
            `SUPPLEMENT_2`:
            ```
            {supplement_2}
            ```
            """
        else:
            template += """the additional data required to solve the problem is a plaintext string in the namespace as `SUPPLEMENT`.  here's a snippet of the first 1000 characters:
            `SUPPLEMENT`:
            ```
            {supplement}
            ```
            """

    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model=model_name)
    chain = prompt | model

    input_vars = {"question": problem["statement"]}
    if "supplement" in problem:
        input_vars["supplement"] = problem["supplement"][:1000]

    print("model responding")
    try:
        with time_limit(900):
            llm_response = chain.invoke(input_vars)
        print("model responded")
    except TimeoutException:
        print("model timed out")
        return False

    output = io.StringIO()
    sys.stdout = output

    namespace = {}
    result = None

    pattern = r"SOLUTION:\s*```(?:\w+\n)?(.*?)```"
    match = re.search(pattern, llm_response, re.DOTALL)

    if match:
        llm_code = match.group(1)
        if "supplement" in problem:
            namespace["SUPPLEMENT"] = problem["supplement"]

        if "supplement_2" in problem:
            namespace["SUPPLEMENT_2"] = problem["supplement_2"]

        try:
            install_missing_packages(llm_code)
            try:
                with time_limit(60):
                    exec(llm_code, namespace)

                    if "solution" in namespace:
                        result = namespace["solution"]()
                    else:
                        print("no solution() function found in model's response")
                        result = None

            except TimeoutException:
                print("Solution timed out after 60 seconds")
                result = None
            except Exception as e:
                print(f"Error in solution execution: {e}")
                result = None
        except Exception as e:
            print(f"Error in code setup: {e}")
            result = None
    else:
        print("no regex match found in model's response")
        result = None

    sys.stdout = sys.__stdout__

    print("Captured Output:", output.getvalue())
    print("Result:", result)
    return str(result) == str(problem["solution"])


with open("problems.json", "r") as f:
    problems = json.load(f)

model_name = "deepseek-r1:14b"
all_problems_sorted = sorted(
    [p for p in problems if "supplement" not in p],
    key=lambda p: float(p.get("difficulty", "100%").rstrip("%")),
)

hard_300 = [p["id"] for p in all_problems_sorted[600:]]

with open("hard_300.json", "w") as f:
    json.dump(hard_300, f, indent=2)


def run_benchmark(model_name):
    wins = []
    for problem in problems[:100]:
        if test_problem(problem, model_name):
            wins.append(problem["id"])
        log_to_file(f"loop {i} problem {problem['id']} wins: {wins}", "log.txt")

    try:
        with open("results-100-1shot.json", "r") as f:
            existing_results = json.load(f)
    except FileNotFoundError:
        existing_results = []

    new_result = {"model": model_name, "successes": len(wins), "successful_tests": wins}

    print("hi", new_result)
    existing_results.append(new_result)

    with open("results-100-1shot.json", "w") as f:
        json.dump(existing_results, f, indent=2)


"""
i = 0
while i < 5:
    run_benchmark(model_name)
    i += 1
"""
