#!/bin/bash

TIMEOUT=60
INTERVAL=2
elapsed=0

# Function to check if Docker daemon is running
is_docker_running() {
    pgrep -x "dockerd" &>/dev/null && docker version &>/dev/null
}

echo "Waiting for Docker to start..."
until is_docker_running; do
    sleep $INTERVAL
    elapsed=$((elapsed + INTERVAL))
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "Error: Docker did not start within $TIMEOUT seconds."
        exit 1
    fi
done

echo "Starting ollama service"
if [ "$(docker ps -q -f name=ollama)" ]; then
    echo "Ollama container is already running."
elif [ "$(docker ps -aq -f name=ollama)" ]; then
    echo "Ollama container exists, restarting existing container..."
    docker restart ollama
else
    echo "Starting new ollama container..."
    docker pull ollama/ollama:latest
    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
fi

echo "Starting Elasticsearch service"
if [ "$(docker ps -q -f name=elasticsearch)" ]; then
    echo "Elasticsearch container is already running."
elif [ "$(docker ps -aq -f name=elasticsearch)" ]; then
    echo "Elasticsearch container exists, restarting existing container..."
    docker restart elasticsearch
else
    echo "Starting new Elasticsearch container..."
    docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2
    docker run --name elasticsearch -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -d -t docker.elastic.co/elasticsearch/elasticsearch:8.12.2
fi

echo "Installing poetry"
pip3 install poetry
poetry config virtualenvs.in-project true 

echo "Installing dependencies"
poetry install --directory server
if ! grep -q 'export PATH="$PWD/server/.venv/bin:$PATH"' ~/.bashrc; then
    echo 'export PATH="$PWD/server/.venv/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
fi

echo "Pulling LLMs"
python setup/pull_models.py

echo "Uploading embeddings"
python data/upload_embeddings.py
