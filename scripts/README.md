# Scripts

Repository-level setup and data-transfer commands live here. Run them from the
repository root:

- `./scripts/init.sh` creates local environment configuration, enforces
  restrictive `.env` permissions, prompts for a site name, generates a secret
  when needed, applies the checked-in migrations, and starts the development
  services. It does not generate migrations.
- `./scripts/export_initial_database.sh` creates and uploads a one-time local
  database backup for an approved initial content transfer.
- `./scripts/db-transfer.sh dump [label]` writes a private Postgres archive to
  `db/dumps/`. `./scripts/db-transfer.sh restore <dump>` restores to a confirmed,
  empty Compose database. See the [transfer runbook](../db/README.md).
- `db-dump.sh` and `db-restore.sh` are the underlying helpers. The direct
  `db-restore.sh <dump>` command drops the archive's matching database objects
  and is intended for local development.
- `configure_local_site.py` is invoked inside the Docker Python environment by
  the initializer; it updates the README title and Wagtail site name and
  preserves an existing secret unless explicitly rotated.
