# Database transfer

Run these commands from the repository root on each host. The transfer script
uses the Compose service called `db` and reads its database name and role from
inside that container. On Linode, use your production Compose configuration
and set `COMPOSE_FILE` if it has a different filename. If production uses
host-installed or managed Postgres, use its native `pg_dump` and `pg_restore`
against that database. Use PostgreSQL 17 on both ends for this workflow.
[PostgreSQL dump and version compatibility](https://www.postgresql.org/docs/17/app-pgdump.html)

## First transfer to Linode

Build and configure the production deployment first. Keep the web service and
other writers stopped and leave the destination database fresh. Restore before
running the initial Django migrations. Use the same application revision on
both hosts for the transfer and apply any pending migrations afterward.

On your workstation, replace `user@linode` with your SSH destination.

```bash
./scripts/db-transfer.sh dump launch
scp -p db/dumps/launch.dump user@linode:
ssh user@linode
```

On Linode, after pulling the repository and configuring the production
environment, run this from the checkout.

```bash
./scripts/db-transfer.sh restore ~/launch.dump
```

The script shows the host and target database and asks you to type the database
name. It checks for existing application objects and restores in one transaction.
It uses the target role for object ownership and skips source grants.
[PostgreSQL restore options](https://www.postgresql.org/docs/17/app-pgrestore.html)

Copy Wagtail uploads separately. For filesystem storage, preserve the paths
under `backend/media/` in the destination's media root. For object storage, copy
the site's prefix into the destination bucket as described in the
[Linode storage setup](../README.md#linode-object-storage). Check the Wagtail
site hostname, port, root page, and accounts before opening traffic.

## Development after launch

**Production owns live content.** Deploy code and migrations through Git.
Publish content through Wagtail, or deliberately import selected pages and
their assets when content was built on staging. Two-way database sync has to
resolve competing edits, deletions, and Wagtail's page and revision relationships.

**Refresh development on demand.** Run
`./scripts/db-transfer.sh dump live-snapshot` on Linode under the production
Compose configuration, then pull it with SCP from your workstation. For an exact
snapshot, create a new database owned by the existing local Postgres role, set
`POSTGRES_DB` in the local `.env` to that name, and use
`./scripts/db-transfer.sh restore db/dumps/live-snapshot.dump`. Switching the
local database name back lets you return to your earlier working copy.
For a refresh in your existing local database, stop local writers, save a
checkpoint, and use the existing replacement helper.

```bash
mkdir -p db/dumps
scp -p user@linode:/path/to/checkout/db/dumps/live-snapshot.dump db/dumps/
./scripts/db-transfer.sh dump before-refresh
./scripts/db-restore.sh db/dumps/live-snapshot.dump
docker compose run --rm web python manage.py migrate
```

The replacement helper overwrites objects present in the archive. Local-only
objects can remain or interfere with restore, so use a fresh target when the
schemas have diverged. Refresh only a confirmed local target, use a sanitized
snapshot when live records include private data, and copy needed uploads to
separate development storage. Update local Wagtail site settings and use local
email and integration settings before exercising the refreshed site.

**Back up production separately.** For scheduled recovery backups, retain
dated database archives and corresponding media backups off the server and
periodically test restoration to an isolated database. Use access-controlled
storage. Archives can include Wagtail drafts, users, password hashes, and
contact submissions. Keep them out of Git.

The default Compose data directory is `.pgdata/`, owned by Postgres. Portable
archives live in `db/dumps/`. Both are ignored by Git.
