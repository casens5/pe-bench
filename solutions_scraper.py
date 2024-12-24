import os
import requests
import json

# URL of the file to be downloaded
url = "https://raw.githubusercontent.com/lucky-bai/projecteuler-solutions/refs/heads/master/Solutions.md"

# Output filename for the markdown file
output_filename_md = "solutions.md"

# Output filename for the JSON file
output_filename_json = "solutions.json"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Write the content of the response to a file named solutions.md
    with open(output_filename_md, 'w', encoding='utf-8') as file:
        file.write(response.text)

    print(f"Downloaded {url} and saved it as {output_filename_md}")

    # Parse the downloaded markdown file and create a dictionary
    solutions_dict = {}
    with open(output_filename_md, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            # Skip lines that do not start with a number followed by a dot
            if line[0].isdigit() and (line[1] == '.' or line[2] == '.' or line[3] == '.'):
                parts = line.split()
                if len(parts) > 1:
                    # Extract the problem number and solution
                    problem_number_str = parts[0][:-1]  # Remove the dot at the end
                    problem_number = int(problem_number_str)
                    solution = parts[1]

                    # Format the key with leading zeros (e.g., "0001", "0002", ...)
                    formatted_key = f"{problem_number:04d}"

                    # Add to the dictionary
                    solutions_dict[formatted_key] = solution

    # Write the dictionary to a JSON file
    with open(output_filename_json, 'w', encoding='utf-8') as json_file:
        json.dump(solutions_dict, json_file, indent=4)

    print(f"Parsed and saved data to {output_filename_json}")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
