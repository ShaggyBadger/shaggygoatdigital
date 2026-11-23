# Production restart

Add an executable script in the repository root to build the production image,
wait for Postgres, apply migrations, collect static files, and recreate the web
container. Document it in the Linode setup instructions and verify command
ordering, failure handling, and startup with disposable containers.

The root script selects the production Compose files and exits before web
recreation when a preparatory command fails. Both first startup and a repeat
deployment completed in disposable Compose containers. The repeat run preserved
the Postgres container and replaced Gunicorn, and the collected Tailwind file
was present. The Compose-built image served an HTTPS-forwarded HTTP request.
A simulated migration failure stopped the script before static collection.
