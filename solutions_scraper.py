import os
import json
import requests
from bs4 import BeautifulSoup

def parse_html_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the table with id 'problems_table'
    table = soup.find('table', id='problems_table')
    if not table:
        raise ValueError("No table found with id 'problems_table'")
    
    result = {}
    
    # Find all rows in the table
    rows = table.find_all('tr')
    
    # Skip the header row
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) != 3: continue
        
        # Extract ID
        id_text = cols[0].get_text(strip=True)
        if not id_text.isdigit(): continue
        id_num = int(id_text)
        id_str = f"{id_num:04d}"  # Pad with leading zeros to make 4 characters
        
        # Extract Title
        title_tag = cols[1].find('a')
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            title = cols[1].get_text(strip=True)
        
        # Extract Solved By
        solved_by_text = cols[2].get_text(strip=True)
        if solved_by_text.isdigit():
            solved_by = int(solved_by_text)
        else:
            # Handle cases where 'Solved By' is not purely digits
            solved_by = solved_by_text
        
        # Add to result dictionary
        result[id_str] = {
            "title": title,
            "solved_by": solved_by
        }
    
    return result

def scrape_statistics():
    # Iterate over the Project Euler Problem Archives
    base_url = "https://projecteuler.net/archives;page="

    statistics = {}

    for i in range(1, 20):
        # Create the full URL for the current problem
        url = f"{base_url}{i}"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Scraping Project Euler Problem Archives page {i}...")
            # get the html
            html_content = response.text

            # Parse the HTML and get the data
            data = parse_html_table(html_content)

            # Add the data to the statistics dictionary
            statistics.update(data)
            print(f"Total problems found so far: {len(statistics)}")
    
    # sort the dictionary by key
    statistics = dict(sorted(statistics.items()))
    return statistics
    
def scrape_solutions():
    url = "https://raw.githubusercontent.com/lucky-bai/projecteuler-solutions/refs/heads/master/Solutions.md"
    response = requests.get(url)
    solutions_dict = {}

    if response.status_code == 200:
        # read the content of the response line by line
        lines = response.text.splitlines()
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

    return solutions_dict

def main():
    print("Scraping Project Euler Problem Statistics...")
    statistics_dict = scrape_statistics()
    print("Scraping Project Euler Problem Solutions...")
    solutions_dict = scrape_solutions()

    # combine the two dictionaries
    for key, value in statistics_dict.items():
        if key in solutions_dict:
            statistics_dict[key]["solution"] = solutions_dict[key]

    # find the number of participants
    participants = 1325386 # taken from the web page https://projecteuler.net/about
    #participants = max(statistics_dict.values(), key=lambda x: x["solved_by"])["solved_by"]

    # assign a difficulty level to each problem
    for key, value in statistics_dict.items():
        solved_by = value["solved_by"]
        
        # points and percentage of users who solved the problem
        points = participants / solved_by
        percentage_solved = 100 / points

        statistics_dict[key]["percentage_solved"] = percentage_solved
        statistics_dict[key]["points"] = points

    output_filename_json = "solutions.json"
    with open(output_filename_json, 'w', encoding='utf-8') as json_file:
        json.dump(statistics_dict, json_file, indent=4)

if __name__ == "__main__":
    main()