#!/bin/bash

# Wait for Ollama server to start
echo "Waiting for Ollama server to start..."
sleep 10

# Create the model
echo "Creating cyber-compass model..."
docker compose exec ai-service ollama create cyber-compass -f /Modelfile

echo "Model creation complete!"