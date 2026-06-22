# moebius-web

In-browser image inpainting with the [Moebius](https://github.com/hustvl/Moebius) model
(0.22B parameters, ECCV'26), running client-side via
[ONNX Runtime Web](https://onnxruntime.ai/docs/tutorials/web/) on the WebGPU backend.

- **Live demo:** https://simonw.github.io/moebius-web/
- **Model weights (ONNX):** https://huggingface.co/simonw/Moebius-ONNX

Ported to ONNX by Claude Opus 4.8. [Full Claude Code transcript](https://gisthost.github.io/?58039ba5c1ca3ed177e8659168996ee4).

Paint over a region of an image to replace it; the denoising loop runs locally on your GPU.
The first run downloads ~1.27 GB of weights from Hugging Face (then browser-cached). A
WebGPU-capable browser (recent Chrome or Safari) is required.

## How it works

Moebius conditions on a learned embedding table rather than a text encoder, so there is no
tokenizer or text model. The export is three ONNX graphs — VAE encoder, UNet, VAE decoder —
and the sampling loop (DDIM with classifier-free guidance, 9-channel latent assembly,
pre/post-processing) runs in TypeScript. See [`web/src/pipeline.ts`](web/src/pipeline.ts).

Notes:
- Fixed 512×512 resolution (the model's cross-attention uses a position embedding tied to the
  trained resolution); non-square inputs are letterboxed.
- VAE `scaling_factor = 0.13025` (a custom VAE, not the usual SD `0.18215`).
- The self-attention `pos_conv` is exported as Conv2d rather than Conv3d so the graph compiles
  on Safari's Metal WebGPU backend.

## Repository layout

| Path | What |
|------|------|
| `web/` | Vite + TypeScript app (the demo). |
| `python/` | Reference inference, ONNX export, fp32↔fp16, full-pipeline parity checks. |
| `web/test/verify.mjs` | Headless Node check of the TS port vs the validated reference. |
| `plan.md`, `notes.md` | Working plan and lab log. |

## Develop

```bash
cd web
npm install
# point the app at local model files, or set VITE_MODEL_BASE to the HF repo:
npm run dev
```

The model files (`unet.onnx`, `vae_encoder.onnx`, `vae_decoder.onnx`) are not in this repo —
they live in the [Hugging Face model repo](https://huggingface.co/simonw/Moebius-ONNX). For
local dev, symlink them into `web/public/models/`, or build with
`VITE_MODEL_BASE=https://huggingface.co/simonw/Moebius-ONNX/resolve/main`.

## Deploy

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds `web/` (with the GitHub
Pages base path and the Hugging Face model base) and deploys to GitHub Pages.

## License

Apache 2.0, inherited from the upstream [hustvl/Moebius](https://github.com/hustvl/Moebius).
The model is by Duan, Xu, et al.; this repository is a browser port and ONNX conversion.
