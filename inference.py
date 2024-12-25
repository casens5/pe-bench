import os
import json
import requests
import urllib3
from argparse import ArgumentParser

def read_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def process_problem_files(problems_dir, template_content, api_base, model_name, language, max_problem_number=9999, skip_existing=False):
    results_dir = os.path.join('solutions', model_name, language)
    os.makedirs(results_dir, exist_ok=True)

    for problem_file in sorted(os.listdir(problems_dir)):
        if not problem_file.endswith('.txt'): continue
        problem_number = problem_file[:-4]  # Remove .txt extension
        if int(problem_number) > max_problem_number: break
        problem_path = os.path.join(problems_dir, problem_file)
        result_file_path = os.path.join(results_dir, f"{problem_number}.md")
        if skip_existing and os.path.exists(result_file_path):
            print(f"Skipping problem {problem_number} as it already has a solution.")
            continue

        with open(problem_path, 'r', encoding='utf-8') as file:
            problem_content = file.read()

        # Construct the prompt using the template
        prompt = template_content.replace('$$$PROBLEM$$$', problem_content)

        try:
            content = ollama_client(api_base, model_name, prompt)

            # Save the response to a file
            with open(result_file_path, 'w', encoding='utf-8') as result_file:
                result_file.write(content)
            print(f"Processed problem {problem_number} and saved response to {result_file_path}")
        except Exception as e:
            print(f"Failed to process problem {problem_number}: {e}")

def ollama_client(api_base='http://localhost:11434', model_name='llama3.2:latest', prompt='Hello World', temperature=0.0, max_tokens=10000):

    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Prepare the API endpoint URL
    endpoint = f"{api_base}/v1/chat/completions"
    stoptokens = ["[/INST]", "<|im_end|>", "<|end_of_turn|>", "<|eot_id|>", "<|end_header_id|>", "<EOS_TOKEN>", "</s>", "<|end|>"]

    # Set headers and payload
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stop": stoptokens,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "max_completion_tokens": max_tokens,
        "stream": False
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Get the error message from the response
        if response:
            try:
                data = response.json()
                message = data.get('message', {})
                content = message.get('content', '')
                raise Exception(f"API request failed: {content}")
            except json.JSONDecodeError:
                raise Exception(f"API request failed: {e}")

    # Parse the response
    try:
        data = response.json()
        choices = data.get('choices', [])
        if len(choices) == 0:
            raise Exception("No response from the API.")
        message = choices[0].get('message', {})
        content = message.get('content', '')
        return content
    except json.JSONDecodeError:
        raise Exception("Failed to parse JSON response from the API.")

def main():
    parser = ArgumentParser(description="Process Euler problems and send them to an LLM.")
    parser.add_argument('--api_base', required=False, default='http://localhost:11434', help='API base URL for the LLM, default is http://localhost:11434')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--language', required=False, default='python', help='Name of the programming language to use, default is python')
    parser.add_argument('--skip_existing', action='store_true', help='if set, skip problems that already have a solution')
    parser.add_argument('--n100', action='store_true', help='only 100 problems') # this is the default
    parser.add_argument('--n200', action='store_true', help='only 200 problems')
    parser.add_argument('--n400', action='store_true', help='only 400 problems')
    parser.add_argument('--nall', action='store_true', help='all problems')

    args = parser.parse_args()

    api_base = args.api_base
    model_name = args.model
    language = args.language
    max_problem_number = 100
    if args.n100: max_problem_number = 100
    if args.n200: max_problem_number = 200
    if args.n400: max_problem_number = 400
    if args.nall: max_problem_number = 9999

    problems_dir = 'problems'
    template_path = os.path.join('templates', 'template_' + args.language + '.md')

    if not os.path.exists(problems_dir):
        raise Exception(f"Problems directory {problems_dir} does not exist.")

    if not os.path.exists(template_path):
        raise Exception(f"Template file {template_path} does not exist.")

    template_content = read_template(template_path)
    process_problem_files(problems_dir, template_content, api_base, model_name, language, max_problem_number = max_problem_number, skip_existing = args.skip_existing)

if __name__ == "__main__":
    main()
