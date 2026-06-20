# Dogsheep

Dogsheep is a collection of tools for *personal analytics* using [SQLite](https://www.sqlite.org/) and [Datasette](https://github.com/simonw/datasette).

Big internet companies know a *lot* about us. By exporting that data back out of them we can see what they know and maybe learn something interesting about ourselves.

Read more about Dogsheep on my blog: [simonwillison.net/tags/dogsheep](https://simonwillison.net/tags/dogsheep/)

Watch [Personal Data Warehouses: Reclaiming Your Data](https://simonwillison.net/2020/Nov/14/personal-data-warehouses/) for a demo  of Dogsheep in action.

## Dogsheep tools

These tools, maintained by the Dogsheep project, let you export your data into a SQLite database for further analysis.

* **[twitter-to-sqlite](https://github.com/dogsheep/twitter-to-sqlite)** uses the Twitter API or Twitter's "export your data" zip archive to create a database of your tweets, followers, people you follow, favourited tweets and much more besides.
* **[healthkit-to-sqlite](https://github.com/dogsheep/healthkit-to-sqlite)** converts your Apple HealthKit export into a database, with details of your heart rate, workouts, step count and more.
* **[swarm-to-sqlite](https://github.com/dogsheep/swarm-to-sqlite)** imports your checkin history from Foursquare Swarm.
* **[apple-notes-to-sqlite](https://datasette.io/tools/apple-notes-to-sqlite)** saves Apple Notes data to a database.
* **[inaturalist-to-sqlite](https://github.com/dogsheep/inaturalist-to-sqlite)** imports the wildlife and plants you have spotted on [iNaturalist](https://www.inaturalist.org/).
* **[google-takeout-to-sqlite](https://github.com/dogsheep/google-takeout-to-sqlite)** imports data from Google Takeout, which can include your Google Maps location history, your search history on Google and more to come.
* **[genome-to-sqlite](https://github.com/dogsheep/genome-to-sqlite)** imports your genome from [23andMe](https://www.23andme.com/) into a SQLite database.
* **[github-to-sqlite](https://github.com/dogsheep/github-to-sqlite)** imports repositories you have created or starred on GitHub.
* **[pocket-to-sqlite](https://github.com/dogsheep/pocket-to-sqlite)** imports articles you have saved using [Pocket](https://getpocket.com/).
* **[hacker-news-to-sqlite](https://github.com/dogsheep/hacker-news-to-sqlite)** imports stories and comments posted to [Hacker News](https://news.ycombinator.com/).
* **[dogsheep-photos](https://github.com/dogsheep/dogsheep-photos)** imports metadata about photos from Apple Photos, including machine learning labels. See [Using SQL to find my best photo of a pelican according to Apple Photos](https://simonwillison.net/2020/May/21/dogsheep-photos/).
* **[dogsheep-beta](https://github.com/dogsheep/dogsheep-beta)** is a search index which combines data from all of the other sources into a single faceted search interface.
* **[evernote-to-sqlite](https://github.com/dogsheep/evernote-to-sqlite)** converts exported Evernote files in the ENEX format into a SQLite database.

## Tools by other developers

These tools help bring the Dogsheep philosophy to life.

* **[beeminder-to-sqlite](https://github.com/bcongdon/beeminder-to-sqlite)** by Ben Congdon saves your goals and data points from [Beeminder](https://www.beeminder.com/).
* **[goodreads-to-sqlite](https://github.com/rixx/goodreads-to-sqlite)** by Tobias Kunze imports your reading history from [Goodreads](https://www.goodreads.com/).
* **[pinboard-to-sqlite](https://github.com/jacobian/pinboard-to-sqlite)** by Jacob Kaplan-Moss saves your bookmarks from [Pinboard](https://pinboard.in/).
* **[todoist-to-sqlite](https://github.com/bcongdon/todoist-to-sqlite)** by Ben Congdon saves your tasks and projects from [Todoist](https://todoist.com/).
* **[parkrun-to-sqlite](https://github.com/mrw34/parkrun-to-sqlite)** by Mark Woodbridge imports your [parkruns](https://www.parkrun.com).
