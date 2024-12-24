import os
import requests

# Base URL for Project Euler problems
base_url = "https://projecteuler.net/minimal="

# Directory to save the files
output_dir = "problems"

# Ensure the directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through numbers from 1 to 913
for i in range(1, 914):
    # Create the full URL for the current problem
    url = f"{base_url}{i}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Format the filename with leading zeros (e.g., 0001.txt, 0002.txt, ...)
        filename = f"{i:04d}.txt"

        # Create the full file path
        filepath = os.path.join(output_dir, filename)

        text = response.text
        # replace all "<p>" with "" and all "</p>" with "\n"
        text = text.replace("<p>", "").replace("</p>", "\n")

        # Write the content of the response to a text file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)

        print(f"Downloaded {url} and saved it as {filepath}")
    else:
        print(f"Failed to download {url}, status code: {response.status_code}")
