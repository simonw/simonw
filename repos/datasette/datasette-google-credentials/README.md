# datasette-google-credentials

A [Datasette](https://datasette.io/) plugin for securely handling Google credentials like [OAuth connections](https://developers.google.com/identity/protocols/oauth2) and [service accounts](https://docs.cloud.google.com/iam/docs/service-account-overview). Secrets are stored in [Datasette's internal database](#TODO).

With `datasette-google-credentials` Datasette actors with permission can link their Google account in Datasette through OAuth, to bring in their own Google data (Google Sheets, Calendar, etc.). Or they can provide a service account JSON file and allow others in their team to access documents that the service account has access to. 

This plugin only handles credentials. Other plugins like [`datasette-google-sheets`](https://github.com/datasette/datasette-google-sheets) can use this plugin to handle all the credentials/permissions, while implementing user features themselves (accessing Google Sheets data, BigQuery data, etc.).

This is an early alpha under active development.
