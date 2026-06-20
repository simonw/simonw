# django-screenshots

Automates taking screenshots of Django, with the goal of providing screenshots to use in the Django documentation.

## Running locally

To run this locally:

```bash
git clone https://github.com/simon/django-screenshots
cd django-screenshots
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
python generate.py
```

This starts a localhost server with the example Django project in `testproject/` and then takes screenshots using [shot-scraper](https://shot-scraper.datasette.io/) based on the configuration in [shots.yml](https://github.com/simonw/django-screenshots/blob/main/shots.yml).

Screenshots are written to the [screenshots/](https://github.com/simonw/django-screenshots/tree/main/screenshots) directory.

## Running in GitHub Actions

Any commits to `main` will run the script in GitHub Actions. This will generate screenshots in `screenshots/` and then commit them back to the repository.

## Adding new screenshots

New screenshots can be added to `shots.yml`. The documentation for that is here: https://shot-scraper.datasette.io/en/stable/multi.html
