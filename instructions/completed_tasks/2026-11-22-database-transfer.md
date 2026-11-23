# Database transfer

- Reuse the Compose dump and restore helpers behind one transfer command.
- Add a transactional restore mode for an empty launch database and document
  how to refresh development from live content and media.
- Verify the round trip and refusal against disposable Postgres containers.

Implemented in `scripts/db-transfer.sh` and the dump and restore helpers.
The runbook in `db/README.md` covers launch, local refresh, and separate media
transfer. Disposable PostgreSQL 17 checks passed for the round trip, sequence
values, private file permissions, duplicate labels, confirmation, non-empty
targets, and a truncated archive. Linode deployment remains separate.
