# AI counter app from my talk at PyCon US 2024

I built this project for my [Imitation Intelligence](https://simonwillison.net/2024/Jul/14/pycon/) talk.

This little macOS app listens through the microphone and increments a visible counter any time anyone says "AI" or "Artificial Intelligence".

You need to download and extract the model file from here: https://alphacephei.com/vosk/models

Get the `vosk-model-en-us-0.22-lgraph` 128MB zip file and uncompress it. You need to have that `vosk-model-en-us-0.22-lgraph` folder in the same folder as `counter.py`

Then:
```bash
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python counter.py
```
Here's [the ChatGPT transcript](https://chatgpt.com/share/58f2352d-1f17-495b-94f1-4eb44cd574b9) I used to help build the tool.

And a screenshot showing what the counter looks like:

![macOS screenshot - a white rectangle in the top right shows the number four](https://github.com/simonw/count-ai/assets/9599/5955465e-2011-4572-8865-85284b7409e7)
