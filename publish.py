import json
from argparse import ArgumentParser

with open('benchmark.json', 'r', encoding='utf-8') as json_file:
    benchmark = json.load(json_file)

with open('README.md', 'r', encoding='utf-8') as md_file:
    readme = md_file.read()

# find markdown-table in the README.md
table = ""
start = False
for line in readme.split("\n"):
    if line.startswith("| Model"):
        start = True
    if start:
        table += line + "\n"
    # detect end of table: this happens when an empty line is found
    if start and line == "":
        break

print(table)

# produce new markdown-table from benchmark json
# first find largest key entry
maxkey = 0
for key, value in benchmark.items():
    if len(key) > maxkey: maxkey = len(key)
col_size = "Size (*10^9 Params)"
col_quant = "Quantization (Bits)"
col_context = "Context Length (K)"
col_bench_python_100 = "PE-Bench-Python-100"

newtable =  "| Model" + " "*(maxkey-5) + " | " + col_size + " | " + col_quant + " | " + col_context + " | " + col_bench_python_100 + " |\n"
newtable += "| :" + "-"*(maxkey-1) + " | " + "-"*(len(col_size)-1) + ": | " + "-"*(len(col_quant)-1) + ": | " + "-"*(len(col_context)-1) + ": | " + "-"*(len(col_bench_python_100)-1) + ": |\n"
for key, value in benchmark.items():
    col_size_v = str(value.get('_parameter_size', ''))
    col_quant_v = str(value.get('_quantization_level', ''))
    col_context_v = str(value.get('_context_size', ''))
    col_bench_python_100_v = str(value.get('python-100', ''))
    newtable += "| " + key + " "*(maxkey - len(key)) 
    newtable += " | " + " "*(len(col_size) - len(col_size_v)) + col_size_v
    newtable += " | " + " "*(len(col_quant) - len(col_quant_v)) + col_quant_v
    newtable += " | " + " "*(len(col_context) - len(col_context_v)) + col_context_v
    newtable += " | " + " "*(len(col_bench_python_100) - len(col_bench_python_100_v)) + col_bench_python_100_v + " |\n"

newtable += "\n" # make sure that the table has an empty line again

print(newtable)

# now replace the old table with the new table in the readme file
new_readme = readme.replace(table, newtable)
#print(new_readme)

# store the new readme
with open('README.md', 'w', encoding='utf-8') as md_file:
    md_file.write(new_readme)
