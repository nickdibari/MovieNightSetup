#!/bin/bash
set -euo pipefail

# Tail the MovieNight log on the running container

log_filename="thelog.log"
container_name=$(docker ps --filter status=running --filter ancestor=movienight --format "{{.Names}}")

docker exec -it "$container_name" sh -c "tail -f $log_filename"

