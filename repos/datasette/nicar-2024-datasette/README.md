# NICAR24 Datasette Workshop

[Friday March 8th, 11:30am](https://schedules.ire.org/nicar-2024/index.html#1110) in [Baltimore, Maryland](https://schedules.ire.org/nicar-2024)

Your instructors:

- Simon Willison
- Alex Garcia

## Getting Help

- [Datasette on Discord](https://datasette.io/discord)
- The `#proj-datasette` channel in the [News Nerdery Slack](https://newsnerdery.org/)
- The [Github Discussions page on Datasette](https://github.com/simonw/datasette/discussions)

## How to run Datasette on a laptop

This will be a walkthrough of the Datasette open source project! This can be ran either on the conference-provided laptops, as long as you have a working Python environment (ie can `pip install`) packages.

### 1. Installing Datasette and `sqlite-utils`

On the command line, run:

```bash
pip install datasette sqlite-utils
```

To make sure it installed correctly:

```bash
datasette --version

sqlite-utils --version
```

For this workshop, we will use the [`datasette-upload-csvs`](https://github.com/simonw/datasette-upload-csvs) plugin, which can be installed with:

```bash
datasette install datasette-upload-csvs
```

### 2. Uploading a CSV

We will be working with the [San Fransisco Supplier Contracts](https://data.sfgov.org/City-Management-and-Ethics/Supplier-Contracts/cqi5-hm2d/about_data)
dataset. [Download the CSV here](https://gist.githubusercontent.com/asg017/144d059dbad77135a50ef3cd8590aad5/raw/sf_supplier_contracts.csv).

Now startup Datasette with an empty database like so:

```bash
datasette --create nicar24.db --root
```

<details>
<summary>Explanation of flags</summary>
<li>The <code>--create</code> flag will create the <code>nicar24.db</code> database for you. Without it, an <code>nicar24.db file not found</code> error would be raised</li>
<li>The <code>--root</code> flag will print out a signed URL, which grants a view higher privileges, like uploading CSVs.
</details>

Copy+paste the `http://127.0.0.1:8001/-/auth-token?token=...` URL into a web browser. You should see "root" in the top-right corner.

Navigate to the top-right corner menu and select "Upload CSVs". Drag+ drop the `sf_supplier_contracts.csv` file, and name the table `sf_supplier_contracts`.

After importing is complete, you'll have a new `sf_supplier_contracts` table to explore!

### 3. Building a search engine on NICAR24 Sessions

Now we'll focus on a 2nd way to import data, using the `sqlite-utils` CLI. Download the [`nicar-2024-schedule.csv`](https://schedules.ire.org/nicar-2024/nicar-2024-schedule.csv) file to your project folder.

To import the CSV to your SQLite database, we'll use `sqlite-utils` like so:

```bash
sqlite-utils insert nicar24.db sessions nicar-2024-schedule.csv  --csv
```

Start Datasette back up with:

```bash
datasette nicar24.db
```

<details>
<summary>No need for the <code>--create</code> or <code>--root</code> flags!</summary>
Since the <code>nicar24.db</code> database has been created, and we aren't uploading CSVs through the Datasette interface anymore, there's no need for those flags anymore.
</details>

Open `http://127.0.0.1:8001` and checkout the new `sessions` table.

If we want to add a search field to the session_description column, we could run:

```bash
sqlite-utils enable-fts nicar24.db sessions session_description
```

## Introduction to Datasette Cloud

Datasette Cloud is a collaborative space for your newsroom to share and analyze data

It's all built on open source Datasette components: if you want to build your own you are welcome to do so! It will probably cost you more time than having us run it for you though.

Each organization gets a "space" - a private space to collaborate on data.

### 1. Creating a space

Let's create a space now:

- Go to https://www.datasette.cloud/ and create an account - I recommend sign in with Google, that way you don't have to deal with Yet Another Password.
- Enter the invite code we distributed in the session...
- ... and create a space. Datasette Cloud is built on top of [Fly.io](https://fly.io/) which means we can run your space in many different locations around the world. The default in Virginia works just fine though.
- Spaces can take up to a minute to be created the first time.
  - Each space runs on a separate container, for security and to ensure the performance of one space doesn't impact any others
  - We'll start you with 2GB of volume space but this can be increased up to 500GB
  - Your data is continually backed up to a private S3 bucket using Litestream. You can download snapshots of the data directly.
  - Philosophically, avoiding lockin is very important to us. You should be able to extract your data at any time, in an open format

![The create a space UI, with a map to help you pick the global location for your space](create-space.png)

### 2. Importing some data

Once the space is up and running! Let's import some data. There are several ways to load data into Datasette Cloud:
- Uploading CSV files
- Importing CSV files from a URL
- Using the Datasette Cloud API
- ... and a new option using AI, which we'll try out shortly

Let's start with an import from a URL - we'll use the Global Power Plants example on the site.

- Click "The Global Power Point Database" to get started
- Once it has imported, rename that table:
  - Table actions -> Edit table schema -> Enter a new name -> Click "Rename"
- And we get our first visualization! Because it has latitude and longitude columns we can see it on a map.

### 2. Uploading CSV files

Next we'll upload some CSV data.
- Download a copy of the CSV of Baltimore Grocery Stores from https://data.baltimorecity.gov/datasets/baltimore::grocery-stores/explore
- Click "Upload CSV files" on the homepage and drag on the file
- This gets a map too!

Let's try a larger CSV
- Download the CSV of Baltimore City Employee Salaries from https://catalog.data.gov/dataset/baltimore-city-employee-salaries-b820d
- Upload the file
- Edit schema to change the type on `annualSalary` and `grossPay` to float. This means we can sort them.
- Let's start exploring! Find the highest paid employee.
- We can run a custom SQL query to see the department with the highest average:
  ```sql
  select agencyName, avg(grossPay) from Baltimore_City_Employee_Salaries
  group by agencyName
  order by avg(grossPay) desc
  ```

### 3. Running an enrichment

[Enrichments](https://enrichments.datasette.io/) are a powerful new Datasette feature ([introduced here](https://simonwillison.net/2023/Dec/1/datasette-enrichments/)) which allow you to run data modification operations against rows in a table. They are based around plugins, which means new enrichments can be added with [very little code](https://enrichments.datasette.io/en/stable/developing.html).

Now we'll use the regular expression enrichment to add a `hireYear` column:

- Table actions -> Enrich selected data -> Regular expressions
- Source column: `hireDate`
- Capture mode: "Store first match in single column"
- Regular expression: `(\d{4})-.*`
- Output column: `hireYear`

![Screenshot of the enrich data interface with those form fields filled out](enrich-regular-expression.png)

### 4. Building a search engine

We'll repeat the exercise from earlier with the NICAR schedule. This time, upload the `nicar-2024-schedule.csv` file to Datasette Cloud to create a table.

Now we can enable full-text search using the interface:

- Table actions -> Configure full-text-search
- Select `session_title` and `session_description`
- Click the blue button

### 5. Enriching with GPT-4

Let's write a haiku for every NICAR session!

- Table actions -> Enrich selected data -> AI analysis with OpenAI GPT
- Model: `gpt-3.5-turbo` - it's very fast, cheap and writes terrible but entertaining haikus
- Prompt: `{{ session_title }} {{ session_description }}`
- System prompt: `Turn this into a haiku`
- Output column: `haiku`
- Start the enrichment

You can use haiku column -> cog menu -> Show not-blank rows to see the haikus it has written so far.

### 6. Publishing a table

Everything in Datasette Cloud is private, but you can publish individual tables to make them available to anyone with the URL.

Try this on the `nicar-2024-schedule` table:

- Table actions -> Make table public
- Confirm that you want to change the privacy for the table
- The table is now available to anyone at `your-subdomain.datasette.site/data/nicar-2024-schedule`

You can tell if a table is public due to the lack of a padlock icon (we'll be making this more clear soon).

Published tables include the search and filtering interface, and support both `.json` API access and `.csv` exports.

### 7. Extracting data into a table with AI

**[datasette-extract](https://github.com/datasette/datasette-extract)** is a brand new (built just in time for this conference) Datasette plugin that lets you enter unstructured data into a Datasette table using the OpenAI GPT-4 model.

Let's use it to load up a table with data copied from a website.

https://bachddsoc.org/calendar/ is a calendar of upcoming events at the [Bach Dancing & Dynamite Society](https://en.wikipedia.org/wiki/Bach_Dancing_%26_Dynamite_Society) jazz venue in Half Moon Bay (I just created their Wikipedia page!)

We're going to start an events calendar for the city, without any tedious data entry.

Start on your `/data` database  is page. 
- Database actions -> Create table with extracted data

Visit https://bachddsoc.org/calendar/ and copy and paste a chunk of text from the page. Don't worry about the format.

Configure the table as follows:
- Table name: `events`
- Columns:
  - `event_title`
  - `event_date` - Hint: `YYYY-MM-DD`
  - `venue_name`
  - `venue_address`
  - `start_time` - Hint: `HH:MM 24hr`
  - `description`

Now scroll down and click "Extract".

Watch as the extraction process pulls the events out of the unstructured text and writes them to your new `/data/events` table!

### 8. Extracting structured data from an image

I took [a photograph of a flier](https://static.simonwillison.net/static/2024/comedy-luau.jpeg) for an event in Half Moon Bay a while ago. Let's import that event as well.

From the new `events` table click:
- Table actions -> Extract data into this table

Drag the photograph onto the textarea, or select it with the file upload field.

Now wait for a few seconds... and if all goes well the event will be added to the table as well.

## Using the Datasette Cloud (and Datasette) API

Datasette has had a powerful read-only JSON API since it first launched.

One of the signature features of the forthcoming [Datasette 1.0](https://docs.datasette.io/en/latest/changelog.html) is the new [JSON write API](https://docs.datasette.io/en/latest/json_api.html#the-json-write-api), for writing data directly to a Datasette instance.

Let's use the API to import a JSON file directly into Datasette Cloud.

### 1. Create an API key

Use the burger menu at the top right of Datasette Cloud and select "Create API token".

This form allows you to create finely grained API keys. You can create a long-lived key that can do anything your user can do, or you can set an expiration time on it. You can also limit an API key to specific operations, either against everything or against specific databases or tables.

For the moment let's keep things simple: create an API key with the default settings, but set it to expire in an hour.

You'll only see the API key once, so copy and paste it out to your notes.

### 2. Try it out with `curl`

Let's try our new API key. Run the following command in the terminal:
```bash
export DS_KEY='dsatok_...'
```
Now let's make an API call:
```bash
curl 'https://your-subdomain.datasette.cloud/data.json' \
  -H "Authorization: Bearer $DS_KEY"
```
This returns details about every table in your database.

A more interesting thing to do is tag on a SQL query:
```bash
curl 'https://your-subdomain.datasette.cloud/data.json?sql=select+*+from+events' \
  -H "Authorization: Bearer $DS_KEY"
```
This should return the results of that query to your terminal.

### 3. Install and use dclient

[dclient](https://dclient.datasette.io) is a command-line tool for interacting with the Datasette API in a more convenient way. Install it like this:

```bash
pip install dclient
```
To tell it about your key, run `dclient auth set`:

```bash
dclient auth add https://your-subdomain.datasette.cloud/
# Token: paste your token here
```

Now any calls you make to that URL will automatically include the token:
```bash
dclient query https://your-subdomain.datasette.cloud/data 'select * from events'
```
One last convenience: create an alias for that URL like this:
```bash
dclient alias add dc https://your-subdomain.datasette.cloud/data
```
And now you can do this:
```bash
dclient query dc 'select * from events'
```

### 4. Upload JSON using dclient

With all of the above setup, let's import the NICAR JSON schedule.

Grab the file from https://schedules.ire.org/nicar-2024/nicar-2024-schedule.json

Now run the following:
```bash
dclient insert dc nicar_schedule nicar-2024-schedule.json \
  --create --alter --pk session_id
```
This should create a table called `nicar_schedule` in your instance with the `session_id` column set as the primary key.

The `--create` option causes the table to be created if it does not exits yet. The `--alter` option is needed because this JSON file has later objects that have keys that were not present earlier on, so the table needs to be altered to fit them.

## Advanced API usage

Here are some more advanced uses of the Datasette Cloud API:

- https://demos.datasette.site/data/documents is a public searchable database of documents added to the Federal Register. It is populated by [this scheduled GitHub Action](https://github.com/simonw/federal-register-to-datasette/blob/6e46f167de6ff312ef5338121cf2879483aba33b/.github/workflows/main.yml), described in detail in [Getting started with the Datasette Cloud API](https://www.datasette.cloud/blog/2023/datasette-cloud-api/).
- https://simon.datasette.site/data/feed is a feed of content from my blog. It's written to by [this Val Town](https://www.val.town/v/simonw/feedToDatasetteCloud) scheduled JavaScript task, described in [Running a scheduled function on Val Town to import Atom feeds into Datasette Cloud](https://til.simonwillison.net/valtown/scheduled).

## Final demos

- `datasette-comments`
- ChatGPT talking to Datasette - https://gist.github.com/simonw/d6425fd997e61cf517aa196fe988638c
- `datasette-scribe`
