# Project Euler LLM Benchmark

To identify the performance of Large Language Models to solve problems with domain-specific knowledge (here: programming)
we created a benchmark using the Project Euler series of challenging mathematical/computer programming problems.
Because we want to apply LLMs for coding with specific programming languages, we also want to measure how good
a LLM is at coding with that given programming language.

## Results
The computed Benchmarks are so far:

| Model                      | Size (Billion Parameters) | Quantization (Bits)| PE-Bench-Python-100 |
| :------------------------- | ------------------------: | -----------------: | ------------------: |
| athene-v2:72b-q8_0         |                      72.7 |                  8 |               12.70 |
| vanilj/Phi-4:Q8_0          |                      14.7 |                  8 |                7.81 |
| nemotron:70b-instruct-q8_0 |                      70.6 |                  8 |                6.01 |
| llama3.2:latest            |                       3.2 |                  8 |                2.14 |
| qwen2.5:0.5b-instruct-q8_0 |                     0.494 |                  8 |                1.01 |
| qwen2.5-coder:0.5b         |                     0.494 |                  8 |                0.13 |

This shows that even very small models like the llama3.2 model has a two-fold super-human performance at solving those problems.

## Motivation

Solving specific tasks by coding programs requires a high degree of accuracy and efficiency.
Challenging problems, such as those presented by Project Euler, test whether LLMs can comprehend complex problems
and translate that understanding into effective solutions. 

The Project Euler LLM Benchmark (PE-Bench) has therefore instances in Python and Java (and more to come).
A PE-Bench-Python performance number compares the ability of an LLM to be successful with coding with the ability of a
human to solve a problem in the Project Euler Archive. We use the statistics provided by Project Euler to compute a
likelihood to be able to solve a problem and assign points using the inverse value of the likelihood. For each problem
that a LLM can solve, we add those points and compute the average for solving the first 100 problems. This results
in the PE-Bench-Python-100 and PE-Bench-Java-100 performance numbers. A performance number over 1 indicates a
super-human performance.

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

