# sba-loans-covid-19-datasette

Notes on how I created https://sba-loans-covid-19.datasettes.com/

Twitter thread: https://twitter.com/simonw/status/1280283053726691329

Interesting queries:

* [Top NAICS codes by number of loans](https://sba-loans-covid-19.datasettes.com/loans_150k_plus?sql=with+counts+as+%28select+NAICSCode%2C+count%28*%29+as+num_loan_recipients+from+foia_150k_plus+group+by+NAICSCode+order+by+num_loan_recipients+desc%29%0D%0Aselect+counts.NAICSCode%2C+counts.num_loan_recipients%2C+naics_2017.name%2C+%27https%3A%2F%2Fsba-loans-covid-19.datasettes.com%2Floans_150k_plus%2Ffoia_150k_plus%3F_facet%3DCity%26_facet%3DState%26_facet%3DRaceEthnicity%26_facet%3DBusinessType%26_facet%3DGender%26_facet%3DVeteran%26NAICSCode%3D%27+%7C%7C+NAICSCode+as+view_them+from+counts+join+naics_2017+on+counts.NAICSCode+%3D+naics_2017.id)

## Data source

I'm using the `150k plus/foia_150k_plus.csv` file from the zip archive released here: https://sba.app.box.com/s/wz72fqag1nd99kj3t9xlq49deoop6gzf

Accompanying press release: https://home.treasury.gov/news/press-releases/sm1052

More downloads (e.g. per-state): https://home.treasury.gov/policy-issues/cares-act/assistance-for-small-businesses/sba-paycheck-protection-program-loan-level-data

## Converting to SQLite

I used [csvs-to-sqlite](https://github.com/simonw/csvs-to-sqlite) to convert the file to SQLite and make it searchable like this:

    csvs-to-sqlite PPP\ Data\ 150k\ plus.csv \
        -t foia_150k_plus \
        loans_150k_plus.db \
        -c LoanRange \
        -c City \
        -c State \
        -c BusinessType \
        -c RaceEthnicity \
        -c Gender \
        -c Veteran \
        -c NonProfit \
        -d DateApproved \
        -c Lender \
        -c CD \
        -f BusinessName \
        -f Address

I added indexes to all of the foreign keys and optimized the database like this:

    sqlite-utils index-foreign-keys loans_150k_plus.db
    sqlite-utils optimize loans_150k_plus.db

## Adding NAICS codes

The `NAICSCode` column contains six digit NAICS codes, which correspond to different industries.

I downloaded the "6-digit 2017 Code File" XLS file from https://www.census.gov/eos/www/naics/downloadables/downloadables.html and opened it in Numbers, then exported the data back out again as a two column CSV: [naics_2017.csv](https://github.com/simonw/sba-loans-covid-19-datasette/blob/main/naics_2017.csv)

Then I ran the following commands - using [sqlite-utils](https://sqlite-utils.readthedocs.io/en/stable/cli.html) - to import that data and set it up as a foreign key from the `NAICSCode` column.

    # First create the table with an integer primary key and a text column
    sqlite-utils create-table loans_150k_plus.db naics_2017 id integer name text --pk=id
    # Now import the data into it
    sqlite-utils insert loans_150k_plus.db naics_2017 naics_2017.csv --csv
    # Configure the foreign key
    sqlite-utils add-foreign-key loans_150k_plus.db foia_150k_plus NAICSCode naics_2017 id
    # Add an index to that column
    sqlite-utils create-index loans_150k_plus.db foia_150k_plus NAICSCode

## Publishing to Cloud Run

I published the database by running the following command:

    datasette publish cloudrun \
        loans_150k_plus.db \
        --service sba-loans \
        --memory 2Gi \
        --extra-options "--config facet_time_limit_ms:2000" \
        --install datasette-block-robots \
        -m metadata.yml
