# Production container

Build Tailwind and package Django with Gunicorn in `Dockerfile.prod`. Add a
Compose override for Linode that retains the Postgres data path and makes
collected static files available to the host proxy. Document build, restore,
and startup order in the README. Verify the merged configuration, image build,
static collection, and a request to Gunicorn.

The production Compose configuration keeps the application port on loopback and
preserves the Postgres bind mount. A backend-only build context permits rebuilds
with a populated Postgres data directory. The image build, Django system check,
static collection, and Gunicorn HTTP smoke test passed locally. Server cutover
remains part of the launch plan.
