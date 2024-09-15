#!/bin/bash
set -e

docker pull sankeerthbd/aws:latest

docker run -d -p 5000:5000 sankeerthbd/aws
