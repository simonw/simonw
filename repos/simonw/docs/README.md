# docs cookiecutter template

I use this cookiecutter template to create `docs/` folders in my projects when I want to use Sphinx to document them.

This template uses the [Furo](https://github.com/pradyunsg/furo) theme and configures [myst-parser](https://myst-parser.readthedocs.io/en/latest/), allowing documentation to be written in Markdown.

## Usage

```bash
cookiecutter gh:simonw/docs
```
It will ask questions like this:
```
  [1/3] project (): shot-scraper
  [2/3] author (): Simon Willison
  [3/3] docs_directory (docs): 
```
Then it will create a `docs/` directory. To start using it:

```bash
cd docs
pip install -r requirements.txt
make livehtml
```
Create files called `something.md` in the `docs/` directory and add them to the `index.md` file's `toctree` directive to include them in the contents.
