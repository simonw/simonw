# Stanford School Enrollment Project in Datasette

Previous codename: [Project Pelican](https://simonwillison.net/search/?q=%22project+pelican%22)

See [About the Stanford School Enrollment Project 
](https://docs.google.com/document/d/1WRm4KZPDGL1USPaf0E1AIa7gbyeKncv04Pg_rM1N7po/edit) for detailed background and documentation on this data release.

This repository powers the Datasette instance hosted at https://stanford-school-enrollment-project.datasette.io/ - it uses GitHub Actions to import CSV data from [Big Local News](https://biglocalnews.org/) and then load and transform it using [sqlite-utils](https://sqlite-utils.datasette.io/en/stable/cli.html), then publishes it to [Google Cloud Run](https://cloud.google.com/run) using [datasette publish](https://docs.datasette.io/en/stable/publish.html#publishing-to-google-cloud-run).
