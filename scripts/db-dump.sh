#!/usr/bin/env bash
# Dump the Compose database into db/dumps/.
set -euo pipefail
umask 077

PROJECT_ROOT="$(dirname "$(dirname "$(realpath "${BASH_SOURCE[0]}")")")"
cd "$PROJECT_ROOT"

label="${1:-$(date -u +%Y%m%dT%H%M%SZ)}"
if [[ $# -gt 1 || ! "$label" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]]; then
  printf 'Usage: %s [label using letters, numbers, dots, underscores or hyphens]\n' "$0" >&2
  exit 2
fi

target="db/dumps/${label}.dump"
mkdir -p db/dumps
temporary="$(mktemp db/dumps/.archive.XXXXXXXX.dump)"
trap 'rm -f -- "$temporary"' EXIT

docker compose up -d --wait db >/dev/null
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -Fc "$POSTGRES_DB"' > "$temporary"

if [[ ! -s "$temporary" ]]; then
  printf 'Dump produced an empty file.\n' >&2
  exit 1
fi

if ! ln -T -- "$temporary" "$target"; then
  printf 'Could not publish %s. Choose an unused label and try again.\n' "$target" >&2
  exit 1
fi

printf 'Wrote %s (%s)\n' "$target" "$(du -h "$target" | cut -f1)"
