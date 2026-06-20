# simonwillisonblog-backup

Uses [db-to-sqlite](https://github.com/simonw/db-to-sqlite) and [sqlite-diffable](https://github.com/simonw/sqlite-diffable) to pull a backup of the Heroku PostgreSQL database running https://simonwillison.net/ and store it as newline-delimited JSON in this GitHub repository.

Runs as a GitHub Actions workflow, see [.github/workflows/backup.yml](https://github.com/simonw/simonwillisonblog-backup/blob/main/.github/workflows/backup.yml).

Deploys a Datasette instance to https://datasette.simonwillison.net/
