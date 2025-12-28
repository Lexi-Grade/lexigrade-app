#!/usr/bin/env bash
set -e

IMAGE=lexigrade-ollama:latest
TMP_IMAGE=/tmp/lexigrade-ollama.tar
API_IMAGE=lexigrade-api:latest
API_TMP_IMAGE=/tmp/lexigrade-api.tar

echo "🔨 Building Ollama image..."
docker build -t $IMAGE ./ollama

echo "📦 Saving image..."
docker save $IMAGE -o $TMP_IMAGE

echo "📦 Importing image into k3s (requires sudo)..."
sudo k3s ctr images import $TMP_IMAGE

echo "🧹 Cleaning up..."
rm -f $TMP_IMAGE

echo "✅ Done"



echo "🔨 Building LexiGrade API image..."
docker build -f server/infra/k8s/api/Dockerfile . -t $API_IMAGE

echo "📦 Saving API image..."
docker save $API_IMAGE -o $API_TMP_IMAGE

echo "📦 Importing API image into k3s (requires sudo)..."
sudo k3s ctr images import $API_TMP_IMAGE

echo "🧹 Cleaning up..."
rm -f $API_TMP_IMAGE

echo "✅ All images built successfully"