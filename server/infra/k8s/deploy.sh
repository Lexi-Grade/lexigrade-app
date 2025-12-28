#!/usr/bin/env bash
set -e
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml


echo "Deploying LexiGrade to k3s..."
kubectl apply -f ./server/k8s/namespace.yaml
kubectl apply -f ./server/k8s/ollama/deployment.yaml
kubectl apply -f ./server/k8s/ollama/service.yaml
kubectl apply -f ./server/infra/k8s/api/deployment.yaml
kubectl apply -f ./server/infra/k8s/api/service.yaml

echo "Done"
