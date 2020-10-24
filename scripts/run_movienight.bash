#!/bin/bash
set -euo pipefail

docker run \
    -d \
    --rm \
    -p 127.0.0.1:8089:8089 \
    -p 1935:1935 \
    -v ~/MovieNight/settings.json:/config/settings.json \
    movienight

