# inaturalist-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/inaturalist-to-sqlite.svg)](https://pypi.org/project/inaturalist-to-sqlite/)
[![CircleCI](https://circleci.com/gh/dogsheep/inaturalist-to-sqlite.svg?style=svg)](https://circleci.com/gh/dogsheep/inaturalist-to-sqlite)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dogsheep/inaturalist-to-sqlite/blob/master/LICENSE)

Create a SQLite database containing your observation history from [iNaturalist](https://www.inaturalist.org/).

## How to install

    $ pip install inaturalist-to-sqlite

## Usage

    $ inaturalist-to-sqlite inaturalist.db yourusername

(Or try `simonw` if you don't yet have an iNaturalist account)

This will import all of your iNaturalist observations into a SQLite database called `inaturalist.db`.