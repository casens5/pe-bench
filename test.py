import os
import json
import requests
import urllib3
from argparse import ArgumentParser

def test(model_name, language, skip_existing):
    # call inference.py
    if skip_existing:
        os.system(f"python3 inference.py --model {model_name} --language {language} --skip_existing")
    else:
        os.system(f"python3 inference.py --model {model_name} --language {language}")

    # call codeextraction.py
    os.system(f"python3 codeextraction.py --model {model_name} --language {language}")

    # call execute.py
    os.system(f"python3 execute.py --model {model_name} --language {language}")

def ollama_list(api_base='http://localhost:11434'):
    # call api http://localhost:11434/api/tags with http get request
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    endpoint = f"{api_base}/api/tags"
    response = requests.get(endpoint, verify=False)
    response.raise_for_status()
    data = response.json()
    models_list = data['models']
    models_dict = {}
    for entry in models_list:
        # get parameter_size and quantization_level from data
        model = entry['model']
        details = entry['details']
        attr = {}
        parameter_size = details['parameter_size']
        quantization_level = details['quantization_level']
        parameter_size = parameter_size[:-1]
        try:
            parameter_size = float(parameter_size)
            attr['parameter_size'] = parameter_size
        except ValueError:
            pass
        quantization_level_char = quantization_level[1:2]
        try:
            quantization_level = int(quantization_level_char)
            attr['quantization_level'] = quantization_level
        except ValueError:
            pass
        models_dict[model] = attr
    return models_dict

def main():
    parser = ArgumentParser(description="Run the complete pipeline to execute solutions and store results in a JSON file.")
    parser.add_argument('--allmodels', action='store_true', help='loop over all models provided by ollama and run those which are missing in benchmark.json')
    parser.add_argument('--model', required=False, default='llama3.2:latest', help='Name of the model to use, default is llama3.2:latest')
    parser.add_argument('--language', required=False, default='python', help='Name of the language to use, default is python')
    parser.add_argument('--skip_existing', action='store_true', help='if set, skip problems that already have a solution')

    args = parser.parse_args()
    model_name = args.model
    language = args.language
    skip_existing = args.skip_existing

    if args.allmodels:
        # loop over all models provided by ollama and run those which are missing in benchmark.json
        with open('benchmark.json', 'r', encoding='utf-8') as json_file:
            benchmark = json.load(json_file)
        # load models from ollama
        models = ollama_list()
        for model in models:
            if model in benchmark:
                entry = benchmark[model]
                # check if attributes parameter_size and quantization_level are present in benchmark.json
                if not '_parameter_size' in entry and models[model].get('parameter_size', None):
                    entry['_parameter_size'] = models[model].get('parameter_size', None)
                if not '_quantization_level' in entry and models[model].get('quantization_level', None):
                    entry['_quantization_level'] = models[model].get('quantization_level', None)
                entry = dict(sorted(entry.items(), key=lambda item: item[0]))
                benchmark[model] = entry
            else:
                # run the model
                test(model, language, skip_existing)
                # load benchmark.json again because the test has updated it
                with open('benchmark.json', 'r', encoding='utf-8') as json_file:
                    benchmark = json.load(json_file)
                # add metadata to benchmark.json
                entry = benchmark[model]
                # check if attributes parameter_size and quantization_level are present in benchmark.json
                if models[model].get('parameter_size', None):
                    entry['_parameter_size'] = models[model].get('parameter_size', None)
                if models[model].get('quantization_level', None):
                    entry['_quantization_level'] = models[model].get('quantization_level', None)
                entry = dict(sorted(entry.items(), key=lambda item: item[0]))
                benchmark[model] = entry
            # write the updated benchmark file
            with open('benchmark.json', 'w', encoding='utf-8') as json_file:
                json.dump(benchmark, json_file, indent=4)
    else:
        test(model_name, language, skip_existing)

if __name__ == "__main__":
    main()
