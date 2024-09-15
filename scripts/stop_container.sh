#!/bin/bash
set -e

# Stop the running container (if any)
if [ "$(docker ps -q -f name=flask-app-container)" ]; then
    docker stop flask-app-container
    docker rm flask-app-container
else
    echo "No container named 'flask-app-container' is running."
fi
