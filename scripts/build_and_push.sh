#!/bin/bash
set -e
IMAGE_TAG="$1"
REGISTRY="$2"
PASSWORD="$3"
USERNAME="$4"
DOCKER_REGISTRY = "info@aptusdatalabs.com"

docker build -t "$IMAGE_TAG" .
echo "$PASSWORD" | docker login "DOCKER_REGISTRY" -u "$USERNAME" --password-stdin
docker push "$IMAGE_TAG"
docker logout "$REGISTRY"
