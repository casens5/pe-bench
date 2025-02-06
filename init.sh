#!/bin/bash

curl -fsSL https://ollama.com/install.sh | sh

pip install langchain-ollama 

ollama serve &

while true; do
    if ollama ps 2>&1 | grep -qv "Error: could not connect to ollama app"; then
        break
    else
        sleep 3
    fi
done

ollama pull llama3.2:1b
