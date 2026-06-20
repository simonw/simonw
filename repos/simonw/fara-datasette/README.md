# fara-datasette

> ❗️**Obsolete**
>
> This repository has been replaced by https://github.com/simonw/fara-history

This code pulls the latest CSVs from https://efile.fara.gov/ords/f?p=API:BULKDATA and loads them into a SQLite database suitable for publishing using [Datasette](https://datasette.readthedocs.io/)



## Running the code

Clone this repo and `pip install -r requirements.txt`

Create the `fara.db` file by running `python fetch_data.py`

Start exploring it in [Datasette](https://github.com/simonw/datasette) using:

    datasette fara.db -m metadata.json
