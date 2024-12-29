import os
import json
import requests
import urllib3
from argparse import ArgumentParser

def read_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def process_problem_files(problems_dir, template_content, endpoint, language, max_problem_number=9999, skip_existing=False):
    results_dir = os.path.join('solutions', endpoint["name"], language)
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
            content = ollama_client(endpoint, prompt)

            # Save the response to a file
            with open(result_file_path, 'w', encoding='utf-8') as result_file:
                result_file.write(content)
            print(f"Processed problem {problem_number} and saved response to {result_file_path}")
        except Exception as e:
            print(f"Failed to process problem {problem_number}: {e}")

def ollama_client(endpoint, prompt='Hello World', temperature=0.0, max_tokens=4096):

    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Prepare the API endpoint URL
    stoptokens = ["[/INST]", "<|im_end|>", "<|end_of_turn|>", "<|eot_id|>", "<|end_header_id|>", "<EOS_TOKEN>", "</s>", "<|end|>"]

    # Set headers and payload
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    if endpoint.get("key", ""):
        headers['Authorization'] = 'Bearer ' + endpoint["key"]
        stoptokens = []

    modelname = endpoint["model"]
    messages = []
    # o1 has special requirements
    if not modelname.startswith("o1"):
        messages.append({"content": "You are a helpful assistant", "role": "system"})
    else:
        temperature = 1.0 # o1 models need temperature 1.0
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": modelname,
        "messages": messages,
        "stop": stoptokens,
        "temperature": temperature,
        #"max_tokens": max_tokens,
        "max_completion_tokens": max_tokens,
        "response_format": { "type": "text" },
        "stream": False
    }

    try:
        response = requests.post(endpoint["endpoint"], headers=headers, json=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # print(f"Failed to access api: {e}")
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
        #print(data)
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
    parser.add_argument('--endpoint', required=False, default='', help='Name of an <endpoint>.json file in the endpoints directory')
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

    # construct the endpoint object
    endpoint_name = args.endpoint
    endpoint = {}
    if endpoint_name:
        endpoint_path = os.path.join('endpoints', f"{endpoint_name}.json")
        print(f"Using endpoint file {endpoint_path}")
        if not os.path.exists(endpoint_path):
            raise Exception(f"Endpoint file {endpoint_path} does not exist.")
        with open(endpoint_path, 'r', encoding='utf-8') as file:
            endpoint = json.load(file)
    else:
        # construct the endpoint object from command line arguments considering that ollama is the endpoint
        api_base='http://localhost:11434'
        endpoint = {
            "name": model_name,
            "model": model_name,
            "key": "",
            "endpoint": f"{api_base}/v1/chat/completions",
        }
    problems_dir = 'problems'
    template_path = os.path.join('templates', 'template_' + language + '.md')

    if not os.path.exists(problems_dir):
        raise Exception(f"Problems directory {problems_dir} does not exist.")

    if not os.path.exists(template_path):
        raise Exception(f"Template file {template_path} does not exist.")

    template_content = read_template(template_path)
    process_problem_files(problems_dir, template_content, endpoint, language, max_problem_number = max_problem_number, skip_existing = args.skip_existing)

if __name__ == "__main__":
    main()
