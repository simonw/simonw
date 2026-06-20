# Template repository for creating new Datasette plugins

This GitHub [template repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/creating-a-repository-from-a-template) can be used to create a new repository with the skeleton of a Datasette plugin, based on the [datasette-plugin](https://github.com/simonw/datasette-plugin) cookiecutter.

Start here: https://github.com/simonw/datasette-plugin-template-repository/generate

Call your new repository `datasette-something` - where the `something' describes your new plugin. You can use additional hyphens - examples of valid plugin repository names include:

- `datasette-places-on-a-map`
- `datasette-emoji`

Add a one-line description of your repository, then click "Create repository from template".

![Screenshot of the create repository form](https://user-images.githubusercontent.com/9599/131229113-76b3d853-44d2-4ea2-8e29-9b09398b885f.png)

Once created, your new repository will execute a GitHub Actions workflow that uses cookiecutter to rewrite the repository to the desired state. This make take 30 seconds or so.

You can see an example of a repository generated using this template here:

- https://github.com/simonw/datasette-plugin-template-repository-demo

## GitHub Actions setup by this repository

The `test.yml` GitHub Actions workflow will run your tests automatically any time you push a change to the repo.

The `publish.yml` Action runs when you create a new GitHub release. It can build and upload your package to [PyPI](https://pypi.org/).

For this to work, you need to create an API token for your PyPI account and add that to your repository as a secret called `PYPI_TOKEN`.

See [Publishing your plugin as a package to PyPI](https://github.com/simonw/datasette-plugin#publishing-your-plugin-as-a-package-to-pypi) for details.