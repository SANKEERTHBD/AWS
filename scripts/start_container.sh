#!/bin/bash
set -e

docker pull sankeerthbd/aws

docker run -d -p 5000:5000 sankeerthbd/aws
