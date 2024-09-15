#!/bin/bash
set -e

# Pull the latest image from Docker Hub
docker pull sankeerthbd/aws:latest

# Stop and remove any existing container with the same name
if [ "$(docker ps -q -f name=flask-app-container)" ]; then
    docker stop flask-app-container
    docker rm flask-app-container
fi

# Run a new container from the pulled image
docker run -d -p 5000:5000 --name flask-app-container sankeerthbd/aws:latest
