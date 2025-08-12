#!/bin/bash
set -e
IMAGE_TAG="$1"
REGISTRY="$2"
PASSWORD="$3"
USERNAME="$4"

docker build -t "$IMAGE_TAG" .
echo "$PASSWORD" | docker login "$REGISTRY" -u "$USERNAME" --password-stdin
docker push "$IMAGE_TAG"
docker logout "$REGISTRY"