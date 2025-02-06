import os
import requests
import json

# Base URL for Project Euler problems
base_url = "https://projecteuler.net/minimal="

# Directory to save the files
output_dir = "problems"

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

filename = "problems.json"
problems = []

# Loop through numbers from 1 to 913
for problem_id in range(1, 914):
    # Create the full URL for the current problem
    url = f"{base_url}{problem_id}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Format the filename with leading zeros (e.g., 0001.txt, 0002.txt, ...)

        # Create the full file path
        filepath = os.path.join(output_dir, filename)

        text = response.text

        # replace all "<p>" with "" and all "</p>" with "\n"
        text = text.replace("<p>", "").replace("</p>", "\n")

        problems.append({"id": problem_id, "statement": text})

    else:
        print(f"Failed to download {url}, status code: {response.status_code}")

with open(filename, "w", encoding="utf-8") as f:
    json.dump(problems, f, indent=2, ensure_ascii=False)
