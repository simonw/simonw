## granite-4.1-3b quantized comparisons

This project ran the same prompt against each of the quantized models in [unsloth/granite-4.1-3b-GGUF](https://huggingface.co/unsloth/granite-4.1-3b-GGUF). You can see the resulting SVGs at [simonw.github.io/granite-4.1-3b-gguf-pelicans/](https://simonw.github.io/granite-4.1-3b-gguf-pelicans/).

Here's the [Codex transcript](https://gisthost.github.io/?d56cc7d112673a063a818de7529dbe89) used to create these files.

*Following text was written by GPT-5.5 and Code CLI:*

----

Prompt:

```text
Generate an SVG of a pelican riding a bicycle
```

The GGUF files with actual model data were run largest to smallest using `/opt/homebrew/Cellar/llama.cpp/8950/bin/llama-completion`. The generated model text for each run was saved as a Markdown file with the same base name as the GGUF file, for example `granite-4.1-3b-Q4_K_M.gguf` produced `granite-4.1-3b-Q4_K_M.md`.

The main generation command shape was:

```shell
/opt/homebrew/Cellar/llama.cpp/8950/bin/llama-completion \
  -m "$model" \
  -p 'Generate an SVG of a pelican riding a bicycle' \
  -n 1024 \
  --ctx-size 4096 \
  --temp 0.7 \
  --no-display-prompt
```

`granite-4.1-3b-UD-IQ2_M.gguf` repeatedly produced an unfinished SVG path at the original settings, so it was rerun with a stronger repetition penalty to get a closable SVG block:

```shell
/opt/homebrew/Cellar/llama.cpp/8950/bin/llama-completion \
  -m granite-4.1-3b-UD-IQ2_M.gguf \
  -p 'Generate an SVG of a pelican riding a bicycle' \
  -n 1024 \
  --ctx-size 4096 \
  --temp 0.4 \
  --repeat-penalty 1.35 \
  --repeat-last-n 128 \
  --no-display-prompt
```

The three initially skipped files were ordinary Git LFS pointer files. Their pointers referenced real objects on the Hugging Face remote, but these three filenames were missing from `.gitattributes`, so `git lfs pull` did not smudge them into full GGUF files. They were fetched explicitly and the missing LFS tracking entries were added to `.gitattributes`:

```shell
git lfs fetch origin \
  --include="granite-4.1-3b-UD-Q2_K_XL.gguf,granite-4.1-3b-UD-Q4_K_XL.gguf,granite-4.1-3b-IQ4_NL.gguf" \
  --exclude=""

git lfs checkout \
  granite-4.1-3b-UD-Q2_K_XL.gguf \
  granite-4.1-3b-UD-Q4_K_XL.gguf \
  granite-4.1-3b-IQ4_NL.gguf
```

In a separate extraction step, the SVG block from each Markdown output was saved as a same-basename `.svg` file. The extractor took the first `<svg` through the last `</svg>` in each Markdown file and normalized malformed SVG namespace values to `http://www.w3.org/2000/svg` so browsers had a better chance of displaying the files. The extracted SVGs are still model outputs and may contain imperfect or nonsensical markup. `granite-4.1-3b-UD-IQ2_M.svg` and `granite-4.1-3b-UD-Q2_K_XL.svg` needed additional small XML repairs after extraction because those models emitted malformed attributes or unmatched tags; the raw Markdown transcripts remain unchanged.

`index.html` was then generated as a static gallery. It displays the extracted SVGs with the source GGUF file name, GGUF size, Markdown link, and SVG link. The gallery is ordered by GGUF file size from largest to smallest.

Runnable model files used:

| GGUF file | Bytes | Size |
| --- | ---: | ---: |
| `granite-4.1-3b-BF16.gguf` | 6809656384 | 6.34 GiB |
| `granite-4.1-3b-UD-Q8_K_XL.gguf` | 4284472640 | 3.99 GiB |
| `granite-4.1-3b-Q8_0.gguf` | 3619691840 | 3.37 GiB |
| `granite-4.1-3b-UD-Q6_K_XL.gguf` | 3048299840 | 2.84 GiB |
| `granite-4.1-3b-Q6_K.gguf` | 2795617600 | 2.60 GiB |
| `granite-4.1-3b-UD-Q5_K_XL.gguf` | 2453939520 | 2.29 GiB |
| `granite-4.1-3b-Q5_K_M.gguf` | 2437012800 | 2.27 GiB |
| `granite-4.1-3b-Q5_K_S.gguf` | 2377825600 | 2.21 GiB |
| `granite-4.1-3b-Q4_1.gguf` | 2181217600 | 2.03 GiB |
| `granite-4.1-3b-UD-Q4_K_XL.gguf` | 2152381760 | 2.00 GiB |
| `granite-4.1-3b-Q4_K_M.gguf` | 2099502400 | 1.96 GiB |
| `granite-4.1-3b-Q4_K_S.gguf` | 1998372160 | 1.86 GiB |
| `granite-4.1-3b-Q4_0.gguf` | 1991163200 | 1.85 GiB |
| `granite-4.1-3b-IQ4_NL.gguf` | 1991163200 | 1.85 GiB |
| `granite-4.1-3b-IQ4_XS.gguf` | 1894497600 | 1.76 GiB |
| `granite-4.1-3b-UD-Q3_K_XL.gguf` | 1794667840 | 1.67 GiB |
| `granite-4.1-3b-Q3_K_M.gguf` | 1725578560 | 1.61 GiB |
| `granite-4.1-3b-Q3_K_S.gguf` | 1566817600 | 1.46 GiB |
| `granite-4.1-3b-UD-IQ3_XXS.gguf` | 1416576320 | 1.32 GiB |
| `granite-4.1-3b-UD-Q2_K_XL.gguf` | 1414548800 | 1.32 GiB |
| `granite-4.1-3b-UD-IQ2_M.gguf` | 1285053760 | 1.20 GiB |
