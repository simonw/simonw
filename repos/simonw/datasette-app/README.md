# Datasette Desktop

A macOS desktop application that wraps [Datasette](https://datasette.io/). See [Building a desktop application for Datasette](https://simonwillison.net/2021/Aug/30/datasette-app/) for background on this project.

## Installation

Grab the latest release from [the releases page](https://github.com/simonw/datasette-app/releases). Download `Datasette.app.zip`, uncompress it and drag `Datasette.app` to your `/Applications` folder - then double-click the icon.

The first time you launch the app it will install the latest version of Datasette, which could take a little while. Subsequent application launches will be a lot quicker.

## Application features

- Includes a full copy of Python which stays separate from any other Python versions you may have installed
- Installs the latest Datasette release the first time it runs
- The application can open existing SQLite database files or read CSV files into an in-memory database
- It can also create a new, empty SQLite database file and create tables in that database by importing CSV data
- By default the server only accepts connections from your computer, but you can use "File -> Access Control -> Anyone on my networks" to make it visible to other computers on your network (or devices on your [Tailscale](https://tailscale.com/) network).
- Datasette plugins can be installed using the "Install Plugin" menu item

## How it works

The app consists of two parts: the Electron app, and a custom Datasette plugin called [datasette-app-support](https://github.com/simonw/datasette-app-support).

You can install a development version of the app like so:

    # Clone the repo
    git clone https://github.com/simonw/datasette-app
    cd datasette-app
    
    # Download standalone Python
    ./download-python.sh
    
    # Install Electron dependencies and start it running:
    npm install
    npm start

When the app first starts up it will create a Python virtual environment in `~/.datasette-app/venv` and install both Datasette and the `datasette-app-support` plugin into that environment.

To run the Electron tests:

    npm test

The Electron tests may leave a `datasette` process running. You can find the process ID for this using:

    ps aux | grep xyz

Then use `kill PROCESS_ID` to terminate it.

![datasette-app](https://user-images.githubusercontent.com/9599/131289203-18186b26-49a4-46e9-8925-b9e4745f3252.png)

## How to develop plugins

You can develop new Datasette plugins directly against your installation of Datasette Desktop. The [Writing Plugins](https://docs.datasette.io/en/stable/writing_plugins.html) documentation mostly applies as-is, but the one extra thing you will need to do is to install an editable version of your plugin directly into the virtual environment used by Datasette Desktop.

To do this, first create a new plugin in a folder called `datasette-your-new-plugin` with a `setup.py`, as described in the plugin documentation. The easiest way to do that is using the [datasette-plugin cookiecutter template](https://github.com/simonw/datasette-plugin).

Then `cd` into that directory and run the following:

    ~/.datasette-app/venv/bin/pip install -e .

This will install the plugin into your Datasette Desktop environment, such that any edits you make to the files in that directory will be picked up the next time the embedded Datasette server is restarted.

You can restart the server either by quitting and restarting the Datasette Desktop application, or by enabling the Debug menu ("Datasette -> About Datasette -> Enable Debug Menu") and then using "Debug -> Restart Server".

## Release process

To ship a new release, increment the version number in `package.json` and then [create a new release](https://github.com/simonw/datasette-app/releases/new) with a matching tag.

Then [run a deploy](https://github.com/simonw/datasette.io/actions/workflows/deploy.yml) of [datasette.io](https://datasette.io/) to update the latest release link that is displayed on the [datasette.io/desktop](https://datasette.io/desktop) page.
