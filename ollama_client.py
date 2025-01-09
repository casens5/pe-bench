import json
import urllib3
import requests

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

def ollama_chat_endpoint(api_base='http://localhost:11434', model_name='llama3.2:latest'):
    endpoint = {
        "name": model_name,
        "model": model_name,
        "key": "",
        "endpoint": f"{api_base}/v1/chat/completions",
    }
    return endpoint

def ollama_chat(endpoint, prompt='Hello World', temperature=0.0, max_tokens=4096):

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

    modelname = endpoint["model"]
    messages = []
    
    # o1 has special requirements
    if modelname.startswith("o1") or modelname.startswith("gpt-o1"):
        temperature = 1.0 # o1 models need temperature 1.0
    else:
        messages.append({"content": "You are a helpful assistant", "role": "system"})
    if modelname.startswith("4o") or modelname.startswith("gpt-4o"):
        # reduce number of stoptokes to 4
        stoptokens = ["[/INST]", "<|im_end|>", "<|end_of_turn|>", "<|eot_id|>"]

    messages.append({"role": "user", "content": prompt})

    if modelname.startswith("o1") or modelname.startswith("4o"):
        stoptokens = []

    payload = {
        "model": modelname,
        "messages": messages,
        "temperature": temperature,
        "response_format": { "type": "text" },
        "stream": False
    }
    if len(stoptokens) > 0:
        payload["stop"] = stoptokens
    if modelname.startswith("o1"):
        payload["max_completion_tokens"] = max_tokens
    else:
        payload["max_tokens"] = max_tokens

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
            raise Exception("No response from the API: " + str(data))
        message = choices[0].get('message', {})
        content = message.get('content', '')
        return content
    except json.JSONDecodeError:
        raise Exception("Failed to parse JSON response from the API.")


def main():
    models_dict = ollama_list()
    print(models_dict)
    answer = ollama_chat(ollama_chat_endpoint())
    print(answer)

if __name__ == "__main__":
    main()