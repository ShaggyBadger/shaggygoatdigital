#!/usr/bin/env bash
# Transfer a Compose PostgreSQL database between hosts.
set -euo pipefail

scripts_dir="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

case "${1:-}" in
  dump)
    shift
    exec "$scripts_dir/db-dump.sh" "$@"
    ;;
  restore)
    shift
    exec "$scripts_dir/db-restore.sh" --empty "$@"
    ;;
  *)
    printf 'Usage: %s dump [label] | restore <archive.dump>\n' "$0" >&2
    exit 2
    ;;
esac
