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

The `publish.yml` Action runs when you create a new GitHub release. It will build and upload your package to [PyPI](https://pypi.org/).

For this to work, you need to create an environment in your GitHub repository called `release`. You then need to configure PyPI with a new "pending publisher" with the following settings:

- PyPI Project Name: `datasette-name-of-your-plugin`
- Owner: Your GitHub username or organization
- Repository name: The name of your repository
- Workflow name: `publish.yml`
- Environment name: `release`

See [Publish releases to PyPI from GitHub Actions without a password or token](https://til.simonwillison.net/pypi/pypi-releases-from-github) for details.