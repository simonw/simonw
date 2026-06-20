# Template repository for creating new Python libraries

This GitHub [template repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/creating-a-repository-from-a-template) can be used to create a new repository with the skeleton of a Python library, based on the [python-lib](https://github.com/simonw/python-lib) cookiecutter.

Start here: https://github.com/simonw/python-lib-template-repository/generate

The name of your repository will be the name of the Python package that you publish to [PyPI](https://pypi.org/), so make sure that name is not taken already!

Add a one-line description of your repository, then click "Create repository from template".

![Screenshot of the create repository interface](https://user-images.githubusercontent.com/9599/131230293-7ed5760e-b385-407e-bbf1-c6fc7540d3fe.png)

Once created, your new repository will execute a GitHub Actions workflow that uses cookiecutter to rewrite the repository to the desired state. This make take 30 seconds or so.

You can see an example of a repository generated using this template here:

- https://github.com/simonw/python-lib-template-demo

## GitHub Actions setup by this repository

The `test.yml` GitHub Actions workflow will run your tests automatically any time you push a change to the repo.

The `publish.yml` Action runs when you create a new GitHub release. It can build and upload your package to [PyPI](https://pypi.org/).

For this to work you need to create an account on PyPI and configure your new GitHub repository as a "trusted publisher".

See [Publishing your library as a package to PyPI](https://github.com/simonw/python-lib#publishing-your-library-as-a-package-to-pypi) for details.
