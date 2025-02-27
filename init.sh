#!/bin/bash

OLLAMA_PERSIST_DIR="/storage/ollama"

# 1) Install or restore Ollama binary
if [ ! -f "$OLLAMA_PERSIST_DIR/bin/ollama" ]; then
    curl -fsSL https://ollama.com/install.sh | sh
    mkdir -p "$OLLAMA_PERSIST_DIR/bin"
    mv /usr/local/bin/ollama "$OLLAMA_PERSIST_DIR/bin/ollama"
else
    echo "Ollama binary already in persistent storage."
fi

ln -sf "$OLLAMA_PERSIST_DIR/bin/ollama" /usr/local/bin/ollama

echo 'hi'
# 2) Persist the ~/.ollama folder
if [ ! -d "$OLLAMA_PERSIST_DIR/data" ]; then
    mkdir -p "$OLLAMA_PERSIST_DIR/data"
    if [ -d "$HOME/.ollama" ]; then
        mv "$HOME/.ollama"/* "$OLLAMA_PERSIST_DIR/data/"
        rm -rf "$HOME/.ollama"
    fi
fi

echo 'a'
if [ -d "$HOME/.ollama" ] || [ -L "$HOME/.ollama" ]; then
    rm -rf "$HOME/.ollama"
fi

echo 'b'
mkdir -p "$OLLAMA_PERSIST_DIR"
ln -s "$OLLAMA_PERSIST_DIR" "$HOME/.ollama"

echo 'c'
# 3) Start the Ollama server
nohup ollama serve > /dev/null 2>&1 &

until curl -s http://localhost:11434 > /dev/null; do
    sleep 1
done

echo 'e'
# 4) Create/activate a persistent Python venv
if [ ! -d "/storage/python_env" ]; then
    python3 -m venv /storage/python_env
fi

echo 'f'
source /storage/python_env/bin/activate
pip install --upgrade pip
#pip install langchain-ollama
pip install langchain

# 5) Check and pull required models
MODELS=(
"qwen:0.5b" \
"qwen:1.8b" \
"qwen:4b" \
"mistral:7b" \
"deepseek-r1:1.5b" \
"phi4:14b" \
"llama3.2:1b" \
"llama3.2:3b" \
"llama3.1:8b" \
"gemma:2b" \
"gemma2:2b" \
"qwen2:0.5b" \
"qwen2:1.5b" \
"qwen2.5:0.5b" \
"qwen2.5:1.5b" \
"qwen2.5:3b" \
"qwen2.5-coder:0.5b" \
"qwen2.5-coder:1.5b" \
"qwen2.5-coder:3b")

echo 'g'
for MODEL in "${MODELS[@]}"; do
    if ! ollama list | grep -q "$MODEL"; then
        echo "Pulling $MODEL..."
        ollama pull "$MODEL"
    else
        echo "$MODEL already exists"
    fi
done

echo 'h'
# Make sure we have the models directory properly linked
[ -L "$HOME/.ollama/models" ] && rm "$HOME/.ollama/models"
[ -d "$HOME/.ollama/models" ] && rm -rf "$HOME/.ollama/models"
ln -s "$OLLAMA_PERSIST_DIR/data/models" "$HOME/.ollama/models"

echo "Ollama setup complete."