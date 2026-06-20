# alpine-edit

[Microsoft Edit](https://devblogs.microsoft.com/commandline/edit-is-now-open-source/) packaged as a Docker container to run on a Mac

To run `edit` against the files in your current directory, run this:
```bash
docker run --platform linux/arm64 -it --rm -v $(pwd):/workspace ghcr.io/simonw/alpine-edit
```

Here's [background on this project](https://simonwillison.net/2025/Jun/21/edit-is-now-open-source/) on my blog plus a TIL on [Publishing a Docker container for Microsoft Edit to the GitHub Container Registry](https://til.simonwillison.net/github/container-registry).
