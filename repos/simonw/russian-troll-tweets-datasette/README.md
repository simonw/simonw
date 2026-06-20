# russian-troll-tweets-datasette

Published as a Datasette instance: https://russian-troll-tweets.datasettes.com/

Data from https://github.com/fivethirtyeight/russian-troll-tweets

I built the database by checking out the `fivethirtyeight/russian-troll-tweets` repo and running the following:

    csvs-to-sqlite *.csv tweets.db -t tweets \
        -c author -c region -c language -c post_type \
        -c account_type -c account_category \
        -f content -f author

I then used this trick to convert the date columns: https://gist.github.com/simonw/0df922918cc653e73baa8d003df4d872
