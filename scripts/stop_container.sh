#!/bin/bash
set -e

# Stop the running container (if any)
if [ "$(docker ps -q -f name=aws-container)" ]; then
    docker stop aws-container
    docker rm aws-container
else
    echo "No container named 'aws-container' is running."
fi
