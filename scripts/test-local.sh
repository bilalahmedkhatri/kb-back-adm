#! /usr/bin/env bash

# Exit in case of error
set -e

docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error

if [ $(uname -s) = "Linux" ]; then
    echo "Remove __pycache__ files"
    sudo find . -type d -name __pycache__ -exec rm -r {} \+
fi

docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml build
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml up -d
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml exec -T backend bash scripts/tests-start.sh "$@"
