# shot-scraper-template

Quickly create a new GitHub repository that takes automated screenshots of a web page using [shot-scraper](https://github.com/simonw/shot-scraper).

Read more about how this works in [Instantly create a GitHub repository to take screenshots of a web page](https://simonwillison.net/2022/Mar/14/shot-scraper-template/).

[simonw/simonwillison-net-shot](https://github.com/simonw/simonwillison-net-shot) is an example repository created using this template.

## How to get started

Visit https://github.com/simonw/shot-scraper-template/generate

<img width="500" alt="Screenshot of the interface for creating a new repository with this template, showing the URL pasted into the description field" src="https://user-images.githubusercontent.com/9599/158208859-ee12e174-5c5f-40c0-b5f2-e3df15f1ee4f.png">

Pick a name for your new repository, and paste **the URL** of the page you would like to take screenshots of into the **description field** (including the `http://` or `https://`).

Then click **Create repository from template**.

Your new repository will be created, and a script will run which will do the following:

- Add a `shots.yml` file to your repository containing the URL of the page you requested
- Take a screenshot of that URL and add that to your repository as a file called `shot.png`

You can then edit that `shots.yml` file to customize your screenshot, or add more URLs - see below.

If the script does not run when the repository is first created you may need to **Enable Actions** first:

- Click the "Actions" tab
- Clice "Enable Actions"
- Run the "Take screenshots" workflow as described below

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
Other useful options include:

- `wait: 3000` to add a 3 second delay before taking the shot (in case some things need more time to load)
- `javascript: ...` to execute custom JavaScript before taking the shot - to activate menus or hide elements or similar
- `quality: 80` to save a smaller, lower quality JPEG image

This example takes a shot of the LA Times homepage after hiding ads and the terms of service prompt:

```yaml
- url: https://www.latimes.com/
  output: latimes.jpg
  width: 1600
  height: 1600
  quality: 80
  wait: 2000
  javascript: |
    document.querySelectorAll(
      '[data-ad-rendered],#ensNotifyBanner'
    ).forEach(el => el.style.display = 'none')
```
Further options are described in the [shot-scraper README file](https://github.com/simonw/shot-scraper#taking-multiple-screenshots).

## Installing fonts for more languages

The default Ubuntu used by GitHub Actions does not include fonts for many languages, including Chinese and Japanese.

You can modify the `shots.yml` file to install extra fonts by adding this section, between the "Cache Playwright browsers" and "Install dependencies" steps:

```yaml
    - name: Cache Playwright browsers
      uses: actions/cache@v2
      with:
        path: ~/.cache/ms-playwright/
        key: ${{ runner.os }}-browsers
    - name: Install extra fonts
      run: |
        sudo apt-get install fonts-arphic-ukai fonts-arphic-uming fonts-ipafont-mincho fonts-ipafont-gothic fonts-unfonts-core
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
```
