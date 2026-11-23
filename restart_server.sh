#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$(realpath -- "${BASH_SOURCE[0]}")")"
compose=(docker compose -f compose.yaml -f compose.production.yaml)

"${compose[@]}" build web
"${compose[@]}" up -d --wait db
"${compose[@]}" run --rm --no-deps -T web python manage.py migrate --noinput
"${compose[@]}" run --rm --no-deps -T web python manage.py collectstatic --noinput
"${compose[@]}" up -d --no-deps --force-recreate --wait web
"${compose[@]}" ps web db
