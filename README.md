<!-- site-name:start -->
# Shaggy Goat Digital
<!-- site-name:end -->

A reusable, Docker-first Django and Wagtail template for client websites, using
PostgreSQL and Tailwind CSS.

The default Compose configuration runs Django and a Tailwind watcher for local
development. The [production configuration](#production-on-linode) runs
Gunicorn and builds Tailwind into the web image.

## Project layout

- [`backend/`](backend/README.md) contains the Django/Wagtail project and its
  Tailwind build files.
- [`frontend/`](frontend/README.md) is reserved for a future separately built
  frontend application.
- [`scripts/`](scripts/README.md) contains repository setup and data-transfer
  commands.
- [`instructions/`](instructions/README.md) contains project guidance and
  working notes.
- `compose.yaml` and `Dockerfile` at the root orchestrate the local services.

## What you need

- Docker Engine
- Docker Compose v2 (`docker compose`)

Python and Node dependencies run in containers; no host virtual environment is
needed. Python packages are pinned in `backend/requirements.txt`, and Tailwind's
npm dependencies are pinned by `backend/package-lock.json`.

`.gitignore` excludes environment files (except `.env.example`), generated
assets, uploads, logs, database backups, PDFs, office documents, and local data
exports. If a document is intentionally part of source code, add an explicit
allow-rule for it rather than broadly tracking local client files.

## First run

```bash
./scripts/init.sh
```

Open <http://localhost:8000/> for the site and <http://localhost:8000/admin/>
for Wagtail admin.

The initializer creates `.env` from `.env.example` only when `.env` is absent,
prompts for the site's display name and uses it in this README and
`WAGTAIL_SITE_NAME`, sets restrictive permissions, generates a Django secret
key only when blank, starts local Postgres, applies the checked-in migrations,
and starts Django and Tailwind. It offers to create the first Wagtail admin
account and skips that step if a superuser already exists. It preserves other
existing `.env` values and secrets.

## Useful commands

```bash
docker compose logs -f                 # Follow service logs
docker compose exec web python manage.py test
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec tailwind npm run build:css
./scripts/db-transfer.sh dump launch   # Write a portable Postgres archive
docker compose down                    # Stop containers; keep the database files
```

Django writes rotating logs under `backend/logs/` and sends INFO-and-higher
output to the container console. The log directory is ignored by Git.

The Postgres bind mount survives `docker compose down -v`.

## Production on Linode

From the server checkout, set up the production `.env` with `DJANGO_DEBUG=False`,
the site's host and HTTPS origin, and the production database credentials. Select
the Compose override in each deployment shell. It requires Compose 2.24.4 or
later.

```bash
export COMPOSE_FILE=compose.yaml:compose.production.yaml
docker compose config --quiet
docker compose build web
```

For the first launch using existing Wagtail content, keep the web service
stopped and follow the [database and media transfer](db/README.md#first-transfer-to-linode)
before running migrations. After the transfer, or when deploying a later code
update, run:

```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py collectstatic --noinput
docker compose run --rm web python manage.py check --deploy
docker compose up -d web
```

The image includes the compiled CSS, and `collectstatic` writes the files the
host proxy serves at `/static/` to `backend/staticfiles/`. Configure the HTTPS
proxy to forward application requests to `127.0.0.1:8000` and set
`X-Forwarded-Proto` from the incoming scheme. For filesystem uploads, serve
`/media/` from `backend/media/`. The production override uses the same
`./.pgdata` location as the base configuration.

## Database choices

### Where the database lives

The `db` service bind-mounts `./.pgdata`, so the data directory sits inside the
project instead of a Docker named volume. It is gitignored and disposable.

```
.pgdata/          live database (owned by uid 70, mode 0700 — not readable by your user)
db/dumps/         pg_dump archives, also gitignored
db/README.md      the full explanation
```

Postgres owns `.pgdata` and `ls` on it will say permission denied. That is
expected. Inspect it through the container:

```sh
docker compose exec db ls /var/lib/postgresql/data
```

Use the [database transfer runbook](db/README.md) for launch restores, local
snapshots, and Wagtail media. The database commands read the name and user from
the Compose `db` service. Its entrypoint needs to start as root to take ownership
of the mounted directory.

### Default: local Postgres in Docker

Django connects to the `db` Compose service using `DATABASE_HOST=db`. The
`./.pgdata` bind mount preserves content when containers stop or are rebuilt.
This is the normal development setup and works before a remote server exists.

### Optional: a database reached through an SSH tunnel

Prefer a local database for ordinary development. If you deliberately need to
connect to a separate development/staging database through a tunnel:

1. Open the tunnel on the host machine, forwarding a local port such as 15432
   to the remote Postgres port:

   ```bash
   ssh -N -L 15432:127.0.0.1:5432 your-user@your-server
   ```

2. In `.env`, set `DATABASE_HOST=host.docker.internal` and
   `DATABASE_PORT=15432`. The Compose `extra_hosts` entry makes the host
   reachable from the Django container on Linux.
3. Use credentials for that development/staging database, not production.

The local Postgres service may remain running, but Django will use the host and
port selected in `.env`. A container's `127.0.0.1` is the container itself, not
the laptop. Do not use `network_mode: host` as a shortcut; it removes normal
Compose network isolation and makes the setup Linux-specific.

For deployment, supply that environment with the target database's actual host
and credentials. When the app and database are separate containers on the same
Compose network, use the database service name. A host-installed database is
not reachable from an app container through `127.0.0.1`.

### Moving real content to a live site

You do **not** have to re-enter everything. Choose how to move initial content:

- **Small amount of content:** deploy the code, then enter approved pages and
  upload images through the live Wagtail admin. The live app saves them to the
  production database and storage; no database tunnel is needed.
- **Approved launch content already in local Postgres:** follow the [launch
  transfer runbook](db/README.md#first-transfer-to-linode) to dump the database,
  copy it with SCP, and restore it into an empty production database. Copy the
  media separately and review test content, local accounts, and Wagtail's site
  settings before opening traffic.
- **Production already has content:** do not replace its database with a local
  copy. Move only the selected pages and assets through a deliberate
  Wagtail-aware import, or create them in the live admin.

After launch, production is the source of truth for live content. Code
deployments apply migrations but do not overwrite production pages. Wagtail
image records refer to files stored separately by the configured media backend,
so a database backup alone does not move images. Keep development and production
media storage separate.

### Linode Object Storage

Local filesystem storage is the default, so a fresh clone works without bucket
credentials. To use a shared development bucket, set
`USE_LINODE_OBJECT_STORAGE=True` in `.env` and fill in the Linode endpoint,
region, bucket, and access keys. Give each site a unique
`LINODE_STORAGE_LOCATION`, such as `client-example/media`, so projects sharing
the development bucket do not overwrite each other's objects. Linode Object
Storage is accessed through its S3-compatible API; the configured endpoint is
Linode, not AWS.

For production, set the site's bucket name but keep the same location prefix.
Copy that prefix from the shared development bucket to the site's bucket with
`rclone` configured for Linode Object Storage; the database's stored file names
then continue to resolve. With both buckets in the same region, copy only that
site's prefix:

```bash
rclone copy \
  linode-development:COMMON_BUCKET/client-example/media \
  linode-production:SITE_BUCKET/client-example/media
```

Keep production credentials in the production `.env`, never in the starter or a
committed file. Use the same bucket region where practical to make the object
copy straightforward.

### Developing after launch

Use [production snapshots to refresh development](db/README.md#development-after-launch).
Deploy code and migrations independently of Wagtail content.

## Tailwind CSS

The `tailwind` service uses Node in Docker to watch Django templates and write
`backend/static/css/site.css`. The compiled CSS is generated locally and is
ignored by Git.

Shared palette, type, layout, and motion tokens live in
[`backend/static-src/css/tokens.css`](backend/static-src/css/tokens.css). Edit
there and rebuild the stylesheet.

For a one-time minified build, run
`docker compose exec tailwind npm run build:css`.

## Project guidance

`AGENTS.md` contains the shared working rules. Detailed conventions and the
plan/progress workflow live under `instructions/`; consult the router at
`instructions/project_conventions/directory.json` before reading topic files.

The Dockerfile uses the requested `python:3.14-slim` tag. That tag follows the
current Python 3.14 patch release when the image is rebuilt; pin a specific
patch tag if you later want rebuilds to preserve the exact interpreter patch.
