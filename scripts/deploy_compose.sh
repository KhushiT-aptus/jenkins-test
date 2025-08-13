#!/bin/bash
set -euo pipefail

SERVER="$1"
REGISTRY="$2"
IMAGE="$3"
TAG="$4"
USERNAME="$5"
PASSWORD="$6"

log() {
    echo -e "\033[1;34m[DEPLOY]\033[0m $1"
}

error_exit() {
    echo -e "\033[1;31m[ERROR]\033[0m $1" >&2
    exit 1
}

log "Starting deployment to $SERVER..."
log "Image: $REGISTRY/$IMAGE:$TAG"

# Run commands on remote server
ssh -o StrictHostKeyChecking=no "$SERVER" bash -s <<EOF || error_exit "SSH command failed"
set -euo pipefail

echo "[REMOTE] Logging into Docker registry..."
if ! echo "$PASSWORD" | docker login "$REGISTRY" -u "$USERNAME" --password-stdin; then
    echo "[REMOTE ERROR] Docker login failed."
    exit 1
fi

export TAG="$TAG"

if [ ! -d "/home/aptus/jenkins-test" ]; then
    echo "[REMOTE ERROR] Directory /home/aptus/jenkins-test does not exist."
    exit 1
fi

cd /home/aptus/jenkins-test

echo "[REMOTE] Pulling updated images..."
docker-compose pull || { echo "[REMOTE ERROR] Docker compose pull failed."; exit 1; }

echo "[REMOTE] Starting services..."
docker-compose up -d --remove-orphans || { echo "[REMOTE ERROR] Docker compose up failed."; exit 1; }

echo "[REMOTE] Deployment successful!"
EOF

log "Deployment to $SERVER completed successfully."
