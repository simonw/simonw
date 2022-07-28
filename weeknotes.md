# Tools I use for my weeknotes

I use these to help write [my weeknotes](https://simonwillison.net/tags/weeknotes/):

- [TILs created in the past two weeks, as Markdown](https://til.simonwillison.net/tils?sql=select+%27*+%5B%27+%7C%7C+title+%7C%7C+%27%5D%28https%3A%2F%2Ftil.simonwillison.net%2F%27+%7C%7C+topic+%7C%7C+%27%2F%27+%7C%7C+slug+%7C%7C+%27%29%27+as+md+from+til+where+created_utc+%3E%3D+date%28%27now%27%2C+%27-14+days%27%29+order+by+created_utc+limit+101)
- I get releases from [this page](https://github.com/simonw/simonw/blob/main/releases.md)
- [My recent commits across all projects on GitHub](https://github.com/search?o=desc&q=author%3Asimonw&s=committer-date&type=Commits)
- [Niche museums visited](https://www.niche-museums.com/browse?sql=select+%27*+[%27+||+name+||+%27](https%3A%2F%2Fwww.niche-museums.com%2F%27+||+id+||+%27)%27+as+md+from+museums+where+created+%3E%3D+date(%27now%27%2C+%27-21+days%27)+order+by+created) in the past three weeks
- [Closed issues in my repos, sorted by when they were most recently updated](https://github.com/issues?q=is%3Aclosed+is%3Aissue+user%3Asimonw+user%3Adogsheep+sort%3Aupdated-desc) - add `closed:>2022-07-20` to that search to see issues that were closed after the specified date

## Template

```
### Weeknotes:

#### Museums this week

...

#### Releases this week

...

#### TIL this week

...
```
