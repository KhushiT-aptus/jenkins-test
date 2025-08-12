#!/bin/bash
set -e
SERVER="$1"
REGISTRY="$2"
IMAGE="$3"
TAG="$4"
USERNAME="$5"
PASSWORD="$6"

ssh -o StrictHostKeyChecking=no "$SERVER" "
    echo '$PASSWORD' | docker login $REGISTRY -u $USERNAME --password-stdin &&
    export TAG=$TAG &&
    cd /home/aptus/pie-dev-dir/pie_new_backend &&
    docker-compose pull &&
    docker-compose up -d --remove-orphans
"
