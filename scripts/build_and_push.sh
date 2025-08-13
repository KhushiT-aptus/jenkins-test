#!/bin/bash
set -e

IMAGE_TAG="$1"
REGISTRY="$2"
CREDS="$3"  

# username and password extractions from creds
USERNAME=$(echo "$CREDS" | cut -d':' -f1)
PASSWORD=$(echo "$CREDS" | cut -d':' -f2)

echo "🔹 Logging into Docker registry: $REGISTRY"
echo "$PASSWORD" | docker login "$REGISTRY" -u "$USERNAME" --password-stdin

echo "🔹 Building Docker image: $IMAGE_TAG"
docker build -t "$IMAGE_TAG" .

echo "🔹 Pushing Docker image: $IMAGE_TAG"
docker push "$IMAGE_TAG"

echo "✅ Pushed Image Successfully"
