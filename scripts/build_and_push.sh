#!/bin/bash
set -e
IMAGE_TAG="$1"
REGISTRY="$2"
PASSWORD="$3"
USERNAME="$4"

if [ -z "$IMAGE_TAG" ] || [ -z "$DOCKER_REGISTRY" ] || [ -z "$DOCKER_PASSWORD" ] || [ -z "$DOCKER_USERNAME" ]; then
    echo "Usage: $0 <image_tag> <registry> <password> <username>"
    exit 1
fi

echo "🔹 Logging into Docker registry: $DOCKER_REGISTRY"
echo "$DOCKER_PASSWORD" | docker login "$DOCKER_REGISTRY" -u "$DOCKER_USERNAME" --password-stdin

echo "🔹 Building Docker image: $IMAGE_TAG"
docker build -t "$IMAGE_TAG" .

echo "🔹 Pushing Docker image: $IMAGE_TAG"
docker push "$IMAGE_TAG"

echo "Pushed Image Successfully"
