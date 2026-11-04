#! /usr/bin/env sh

# Exit in case of error
set -e
set -x

docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml build
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml up -d
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml exec -T backend bash scripts/tests-start.sh "$@"
docker compose --env-file .env -f docker/compose.yml -f docker/compose.override.yml down -v --remove-orphans
