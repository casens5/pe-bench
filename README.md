# Project Euler LLM Benchmark

To identify the performance of Large Language Models to solve problems with domain-specific knowledge (here: programming)
we created a benchmark using the Project Euler series of challenging mathematical/computer programming problems.
Because we want to apply LLMs for coding with specific programming languages, we also want to measure how good
a LLM is at coding with that given programming language.

## Super-Human Performance
AI systems have domain-specific super-human perforances: chess-AI can compete against the best humans since 1997 where
a chess system "Deep Blue" defeated the world champion Garry Kasparov. Since then the best chess programs are super-human
and the same holds for most other games including Go, defeated by AlphaGo in 2016. So in domain-specific fields, AI programs
have super-human performance and with the "Project Euler LLM Benchmark" we want to measure how strongly LLM models have
super-human performances in the domain of coding or "being a programmer". See "Motivation" chapter below how we measure this.

## Results
The computed Benchmark "PE-Bench-Python-100" is the super-human performance factor to code in python, results are so far:

| Model                                     | Size (*10^9 Params) | Quantization (Bits) | Context Length (K) | PE-Bench-Python-100 |
| :---------------------------------------- | ------------------: | ------------------: | -----------------: | ------------------: |
| DeepSeek-V3                               |               671.0 |                  16 |                 64 |               15.58 |
| athene-v2:72b-q8_0                        |                72.7 |                   8 |                128 |                12.7 |
| qwen2.5:72b-instruct-q8_0                 |                72.7 |                   8 |                128 |               11.01 |
| qwen2.5-coder:14b-instruct-q8_0           |                14.8 |                   8 |                128 |                 9.7 |
| yi-coder:9b-chat-q8_0                     |                 8.8 |                   8 |                128 |                8.57 |
| vanilj/Phi-4:Q8_0                         |                14.7 |                   8 |                 16 |                7.81 |
| falcon3:10b-instruct-q8_0                 |                10.3 |                   8 |                 32 |                7.42 |
| tulu3:70b-q8_0                            |                70.6 |                   8 |                128 |                7.34 |
| llama3.1:70b-instruct-q8_0                |                70.6 |                   8 |                128 |                 6.6 |
| qwen2.5:7b-instruct-q8_0                  |                 7.6 |                   8 |                128 |                 6.4 |
| hf.co/bartowski/Anubis-70B-v1-GGUF:Q4_K_M |                70.6 |                   4 |                128 |                6.14 |
| qwen2.5-coder:7b-instruct-q8_0            |                 7.6 |                   8 |                128 |                6.13 |
| nemotron:70b-instruct-q8_0                |                70.6 |                   8 |                128 |                6.01 |
| yi-coder:9b-chat-q4_K_M                   |                 8.8 |                   4 |                128 |                5.87 |
| qwen2-math:72b-instruct-q8_0              |                72.7 |                   8 |                  4 |                5.64 |
| falcon3:7b-instruct-q8_0                  |                 7.5 |                   8 |                 32 |                5.57 |
| gemma2:27b-instruct-q8_0                  |                27.2 |                   8 |                  8 |                5.18 |
| opencoder:8b-instruct-q8_0                |                 7.8 |                   8 |                  8 |                4.53 |
| qwen2.5-coder:3b-instruct-q8_0            |                 3.1 |                   8 |                 32 |                4.32 |
| tulu3:8b-q8_0                             |                 8.0 |                   8 |                128 |                3.64 |
| exaone3.5:7.8b-instruct-q8_0              |                 7.8 |                   8 |                 32 |                3.55 |
| llama3.1:8b-instruct-q8_0                 |                 8.0 |                   8 |                128 |                3.32 |
| exaone3.5:32b-instruct-q8_0               |                32.0 |                   8 |                 32 |                2.96 |
| qwen2.5:3b-instruct-q8_0                  |                 3.1 |                   8 |                128 |                2.87 |
| granite3.1-dense:8b-instruct-q8_0         |                 8.2 |                   8 |                128 |                 2.8 |
| exaone3.5:2.4b-instruct-q8_0              |                 2.7 |                   8 |                 32 |                2.53 |
| qwen2-math:7b-instruct-q8_0               |                 7.6 |                   8 |                  4 |                2.49 |
| gemma2:9b-instruct-q8_0                   |                 9.2 |                   8 |                  8 |                2.46 |
| yi-coder:1.5b-chat-q8_0                   |                 1.5 |                   8 |                128 |                 2.3 |
| opencoder:1.5b-instruct-q8_0              |                 1.9 |                   8 |                  4 |                 2.2 |
| llama3.2:latest                           |                3.21 |                   4 |                128 |                2.14 |
| qwen2.5:1.5b-instruct-q8_0                |                 1.5 |                   8 |                128 |                1.98 |
| qwen2.5-coder:1.5b-instruct-q8_0          |                 1.5 |                   8 |                 32 |                1.95 |
| falcon3:3b-instruct-q8_0                  |                 3.2 |                   8 |                 32 |                1.89 |
| codegemma:7b-instruct-q8_0                |                 9.0 |                   8 |                  8 |                1.81 |
| granite3.1-dense:2b-instruct-q8_0         |                 2.5 |                   8 |                128 |                1.07 |
| qwen2.5:0.5b-instruct-q8_0                |                 0.5 |                   8 |                128 |                1.01 |
| granite3.1-moe:3b-instruct-q8_0           |                 3.3 |                   8 |                128 |                0.78 |
| qwen2-math:1.5b-instruct-q8_0             |                 1.5 |                   8 |                  4 |                0.61 |
| gemma2:2b-instruct-q8_0                   |                 2.6 |                   8 |                  8 |                0.39 |
| falcon3:1b-instruct-q8_0                  |                 1.7 |                   8 |                  8 |                0.25 |
| granite3.1-moe:1b-instruct-q8_0           |                 1.3 |                   8 |                128 |                0.24 |
| llama3.2:1b-instruct-q8_0                 |                 1.2 |                   8 |                128 |                0.23 |
| qwen2.5-coder:0.5b-instruct-q8_0          |                 0.5 |                   8 |                 32 |                0.13 |

This shows that even very small models like the llama3.2 model has a two-fold super-human performance at solving those problems.

## Motivation

Solving specific tasks by coding programs requires a high degree of accuracy and efficiency.
Challenging problems, such as those presented by Project Euler, test whether a person (or an AI system) can comprehend complex
problems and translate that understanding into effective solutions. 

Because the Project Euler has statistics about the number of solved problems we have the ability to compute the likelihood for
a human to solve the problem. The given counts of course also reflect several other causes for not solving the problem (not enough
interest, not enough time, not visible at the time the contestant has subscribed to the project) which cannot be easily integrated into
our measurement method; however Project Euler started 2015 with more than 160 problems so it is feasable to select only the first 100
problems for the PE-Bench-Python-100 benchmark. 

## Scoring Method

We create the benchmark with the following concept:
- We have a fixed number of `participants = 1325386` and a number of participants who solved each problem `solved_by`
- Each Problem has a specific likelihood to be solved, which is `percentage_solved = solved_by / participants` (must be multiplied with 100 to get the percentage number)
- Each Problem gets a number of points assigned that a participants gets as score, which is `points = participants / solved_by`

So this leads to the effect, that an average person can solve each problem with an performance indicator of `1` (percentage_solved * points).
Therefore the average number of points for solving 100 problems is also `1`. This gives us a nice baseline for human performance.

### Data Sources

The data is scraped from the Project Euler web page and from other sources:

```
python3 problems_scraper.py
```

This loads all problems from https://projecteuler.net/ and stores them intoo the `problems` folder.

```
python3 solutions_scraper.py
```

This loads all solutions from https://raw.githubusercontent.com/lucky-bai/projecteuler-solutions/refs/heads/master/Solutions.md
and combines them with the number of solutions that users have submitted from https://projecteuler.net/archives
The result is stored in `solutions.json`. There also the data is enrichted with `percentage_solved` and `points`.

### Score Computation

If we ask a LLM to solve 100 problems, add the achieved points for each correctly solved problem and divide it by 100, we get the performance
number for that LLM which compares to human performance by that average number. A performance value of `2` would mean "two-fold super-human performance".
In our test, small models like "llama3.2" already have that super-human performance.
A performance number over 1 indicates a super-human performance. It turns out that almost all LLMs have super-human performance.

The score used for the benchmark is computed in three steps:

#### Inference

For a given model and a given programming language, we loop over all (or 1..100) problems within the `problems` directory and perform the following task:
- load the problem description, i.e. from `problems/0001.txt`
- insert the problem description into a prompt template, i.e. from `templates/template_python.md`
- sending the resulting prompt to the selected LLM model using an api call to the ollama `/v1/chat/completions` endpoint
- storing the answer from the model into `solutions/<model_name>/<language>/0001.md

This results in 100 answer files. This can be done calling

```
python3 inference.py --model <model_name>
```

#### Code Extraction

Code is embedded into code blocks of the answer of the llm. We want to extract this in such a way, that a code interpreter can execute the file
directly. This is done with the script

```
python3 codeextraction.py --model <model_name>
```

#### Code Execution and Evaluation

Finally the code is executed within a protected environment. This is done with

```
python3 execute.py --model <model_name>
```

where the python code is executed within. The resulting output line is truncated, only the last line is used. That line is compared
to the actual solution from the `solutions.json` file. The process does the code execution for all 100 problem solutions and adds up all the
points for the corresponding problem. This sum is divided by 100 and is the final score for the model.

## Installation

As a preparation step for the tests, we must download the test cases from project euler with this script:
```
python3 problems_scraper.py
```

All over 900 tests are then stored in the `problems` folder. For our 100-bench-series, we use only the first 100.

## Test Preparation
To compute the benchmark, we use ollama as local inference engine.
To run a test (i.e. for the model `athene-v2:72b-q8_0`), the following command sequence is required:

```
python3 inference.py --language python --model athene-v2:72b-q8_0
python3 codeextraction.py --language python --model athene-v2:72b-q8_0
python3 execute.py --language python --model athene-v2:72b-q8_0
```

However, it is not convenient to do so, instead you can also call

```
python3 test.py --language python --model athene-v2:72b-q8_0
```

That computes all steps and updates the solutions.json file. 

You can also call

```
python3 test.py --language python --allmodels --skip_existing
```

which loads the list of models from ollama and iterates over all models stored with ollama.
This will take some time, if you have a large model collection in ollama maybe this takes
longer than a week.
