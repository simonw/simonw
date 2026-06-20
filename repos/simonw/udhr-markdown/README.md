# Universal Declaration of Human Rights in Markdown

Markdown exports of the [Universal Declaration of Human Rights](https://www.un.org/en/about-us/universal-declaration-of-human-rights) translations extracted from the [udhr npm package](https://www.npmjs.com/package/udhr).

Run:

```sh
npm install
npm run generate
```

Each generated file is written to `declarations/{code}.md`, where `code` is the unique `udhr` package code for that translation. Partial translations are written to `declarations/{code}-partial.md`.

Files are Markdown with YAML frontmatter.

Text obtained via the `udhr` npm package, which distributes Unicode/HTML representations of the UDHR under the MIT License and identifies its source material as the Unicode UDHR corpus derived from OHCHR translations.
