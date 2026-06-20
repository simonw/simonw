# pypi-rename cookiecutter template

Cookiecutter template for creating renamed PyPI packages

## What is this for?

If you want to rename a Python package that you have published on [PyPI](https://pypi.org/) you should follow [these steps](https://www.python.org/dev/peps/pep-0423/#how-to-rename-a-project):

* Create a renamed version of the package
* Publish it to PyPI under the new name
* Now create a final release under the old name which does the following:
  - Tells users about the name change
  - Depends on the new name, so anyone who runs `pip install oldname` will get the new name as a dependency

This cookiecutter template helps create that final release under the old name.

## Installation

You'll need to have [cookiecutter](https://cookiecutter.readthedocs.io/) installed. I recommend [pipx](https://pipxproject.github.io/pipx/) for this:

    pipx install cookiecutter

Regular `pip` will work OK too.

## Usage

Run `cookiecutter gh:simonw/pypi-rename` and then answer the prompts. Here's an example run:

    $ cookiecutter gh:simonw/pypi-rename
    new_package_name []: my-old-package-name
    old_package_name []: my-new-package-name
    old_package_new_version []: 0.2

For `old_package_new_version` you should enter a version that is higher than the most recent version that was published for the package which you are renaming.

This will create a directory called `my-old-package-name` ready to be published to PyPI.

See https://github.com/simonw/pypi-rename-demo for the output of this example.

## Publishing your renamed package to PyPI

First, publish a version of your package under the NEW name.

Now you can use the package created by this template as the last released version under the old name.

This will display a README on PyPI explaining that the module has been renamed, and will also ensure that anyone who runs `pip install my-old-package-name` will get the new package, since the new package is the only dependency for the old renamed package.

Here's an example run, first creating the package using `cookiecutter` and `python -m build`:
```bash
% cookiecutter gh:simonw/pypi-rename
  [1/3] new_package_name (): click-default-group
  [2/3] old_package_name (): click-default-group-wheel
  [3/3] old_package_new_version (): 1.2.3
% cd click-default-group-wheel
% python -m build
* Creating virtualenv isolated environment...
* Installing packages in isolated environment... (setuptools >= 40.8.0, wheel)
* Getting build dependencies for sdist...
...
Successfully built click-default-group-wheel-1.2.3.tar.gz and click_default_group_wheel-1.2.3-py3-none-any.whl
```
And then uploading it to PyPI with `twine` - using a [PyPI API token](https://pypi.org/help/#apitoken) (pasted in as the password):
```bash
% twine upload dist/click*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: __token__
Enter your password: 
Uploading click_default_group_wheel-1.2.3-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.3/4.3 kB • 00:00 • ?
Uploading click-default-group-wheel-1.2.3.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.1/4.1 kB • 00:00 • ?

View at:
https://pypi.org/project/click-default-group-wheel/1.2.3/
```
