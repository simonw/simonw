# webvid-datasette

A Datasette instance for searching through 10m videos included in the [WebVid-10M](https://m-bain.github.io/webvid-dataset/) training set used for the [Make-A-Video](https://makeavideo.studio/) model by Meta AI.

Browse and search the videos at https://webvid.datasette.io/webvid/videos

More on this project: [Exploring 10m scraped Shutterstock videos used to train Meta’s Make-A-Video text-to-video model](https://simonwillison.net/2022/Sep/29/webvid/)

## Building the database

I downloaded the CSV file (2.7 GB) like this:
```bash
wget http://www.robots.ox.ac.uk/~maxbain/webvid/results_10M_train.csv
```
Then I loaded it into a `webvid-full.db` SQLite database [using this trick](https://til.simonwillison.net/sqlite/import-csv) like so:

```bash
sqlite3 webvid-full.db <<EOS
.mode csv
.import results_10M_train.csv videos
EOS
```
The CSV file turned out to have a small number of duplicates (based on video ID) - videos which were in there more than once due to being crawled with an updated caption.

I used this SQL query to identify those:

```sql
select videoid, contentUrl, duration, page_dir, name, count(*)
from videos group by videoid
having count(*) > 1
```
I then created a smaller `webvid.db` database using a number of steps now contained in the [build-webvid-db.sh](build-webvid-db.sh) file.

I published the result to Fly as a custom Docker container.
