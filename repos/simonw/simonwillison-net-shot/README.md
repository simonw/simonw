# shot-scraper-template

Quickly create a new GitHub repository that takes automated screenshots of a web page using [shot-scraper](https://github.com/simonw/shot-scraper).

## How to get started

Visit https://github.com/simonw/shot-scraper-template/generate

<img width="500" alt="Screenshot of the interface for creating a new repository with this template, showing the URL pasted into the description field" src="https://user-images.githubusercontent.com/9599/158208859-ee12e174-5c5f-40c0-b5f2-e3df15f1ee4f.png">

Pick a name for your new repository, and paste **the URL** of the page you would like to take screenshots of into the **description field**.

Then click **Create repository from template**.

Your new repository will be created, and a script will run which will do the following:

- Add a `shots.yml` file to your repository containing the URL of the page you requested
- Take a screenshot of that URL and add that to you repository as a file called `shot.png`

You can then edit that `shots.yml` file to customize your screenshot, or add more URLs - see below.

## Re-taking the screenshot

To re-take the screenshot:

- Click "Actions"
- Select the "Take screenshots" workflow
- Click the "Run workflow" menu item
- Click the green "Run workflow" button

<img width="600" alt="image" src="https://user-images.githubusercontent.com/9599/158210618-4b361520-4fbb-4a90-ab8c-f729776dd8f0.png">


The repository will keep a history of every previous version of each screenshot, which is useful for keeping track of visual changes to a page.

## Configuring the screenshots

The initial `shots.yml` file in your repository should look like this:

```yaml
- url: https://simonwillison.net/
  output: shot.png
  height: 800
```

To change the name of the file that the screenshot is saved to, change `output: shot.png` to a different file name.

To take a full height image of the page, remove the `height: 800` line.

To add additional screenshots, add them to the YAML file like this:

```yaml
- url: https://simonwillison.net/
  output: shot.png
  height: 800
- url: https://www.example.com/
  output: example.png
  height: 800
```
Further options are described in the [shot-scraper README file](https://github.com/simonw/shot-scraper#taking-multiple-screenshots).
