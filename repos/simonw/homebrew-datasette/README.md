# homebrew-datasette

To install [Datasette](https://github.com/simonw/datasette) using Homebrew:

    brew tap simonw/datasette
    brew install simonw/datasette/datasette

You can confirm that the install worked using:

    $ datasette --version
    datasette, version 0.46

## Installing plugins

[Datasette plugins](https://datasette.readthedocs.io/en/stable/plugins.html) need to be installed into the same Python environment as `datasette`.

The easiest way to install them is to use the new `datasette install` command:

    datasette install datasette-vega

If you want to install them using `pip` instead you can do this:

    /usr/local/opt/datasette/libexec/bin/pip install datasette-vega

Run `datasette plugins` to see a list of currently installed plugins.
