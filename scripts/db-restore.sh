#!/usr/bin/env bash
# Restore an archive into the Compose database.
set -euo pipefail

PROJECT_ROOT="$(dirname "$(dirname "$(realpath "${BASH_SOURCE[0]}")")")"
cd "$PROJECT_ROOT"

restore_options=(--clean --if-exists)
if [[ "${1:-}" == --empty ]]; then
  restore_options=()
  shift
fi

if [[ $# -ne 1 ]]; then
  printf 'Usage: %s [--empty] path/to/file.dump\n' "$0" >&2
  exit 2
fi

dump="$1"
[[ -f "$dump" && -s "$dump" ]] || { printf 'Missing or empty dump: %s\n' "$dump" >&2; exit 1; }

docker compose up -d --wait db < /dev/null

if [[ ${#restore_options[@]} -eq 0 ]]; then
  target="$(docker compose exec -T db sh -c 'printf "%s" "$POSTGRES_DB"' < /dev/null)"
  printf 'Restore %s into Compose database %s on %s?\n' "$dump" "$target" "$(hostname)"
  read -r -p "Type the target database name to confirm: " confirmation
  [[ -n "$target" && "$confirmation" == "$target" ]] || { printf 'Restore cancelled.\n' >&2; exit 1; }

  # template1's default user namespace is public, with no user relations.
  occupied="$(docker compose exec -T db sh -c '
    psql -XAt -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "$1"
  ' sh "
    SELECT EXISTS (
      SELECT FROM pg_namespace
      WHERE left(nspname, 3) <> 'pg_' AND nspname NOT IN ('public', 'information_schema')
      UNION ALL SELECT FROM pg_class WHERE relnamespace = 'public'::regnamespace
      UNION ALL SELECT FROM pg_proc WHERE pronamespace = 'public'::regnamespace
      UNION ALL SELECT FROM pg_type WHERE typnamespace = 'public'::regnamespace
      UNION ALL SELECT FROM pg_extension WHERE extname <> 'plpgsql'
      UNION ALL SELECT FROM pg_largeobject_metadata
    );")"
  if [[ "$occupied" != f ]]; then
    printf 'Target database %s already contains objects. Restore into a fresh database.\n' "$target" >&2
    exit 1
  fi
fi

docker compose exec -T db sh -c \
  'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --no-owner --no-acl --single-transaction --exit-on-error "$@"' \
  sh "${restore_options[@]}" < "$dump"

printf 'Restored %s\n' "$dump"
