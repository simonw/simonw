# Building software on top of Large Language Models

A tutorial [presented at PyCon US 2025](https://us.pycon.org/2025/schedule/presentation/25/).

A full write-up with annotated slides [is available here on my blog](https://simonwillison.net/2025/May/15/building-on-llms/).

Here is **[the handout for the workshop](https://building-with-llms-pycon-2025.readthedocs.io/)**.

## Prerequisites for attendees

If you are attending this tutorial you will need a **laptop with a browser** and a **GitHub account**. The tutorial can be entirely completed using [GitHub Codespaces](https://github.com/features/codespaces), a free online development environment.

If you would prefer to run everything on your own machine you will need a **Python 3.9 or higher** local development environment with the ability to create a virtual environment and install packages using `pip`.

You can pre-install the packages we will be using like this:

```bash
git clone https://github.com/simonw/building-with-llms-pycon-2025
cd building-with-llms-pycon-2025
python -m venv venv
venv/bin/pip install -r requirements.txt
```

If you would like to explore **local models** and have both the space and the capacity to run them on your own machine you should download additional software prior to the workshop, as these large files should not be downloaded over the conference WiFi. This is *strictly optional* - the section of the workshop on local models will not assume that you have them available on your own machine.

For this section, I recommend installing [Ollama](https://ollama.com/). This free software is available for macOS, Linux, and Windows, and packages various LLMs for local use.

With Ollama installed you will need to download one or more models. Which model to get depends on your system's specifications. If you are on an Apple Silicon Mac (M1, M2 etc) I recommend:

- Up to 16GB of RAM: `qwen3:4b` (2.6GB). Download with `ollama pull qwen3:4b`.
- Up to 32GB of RAM: `qwen3:8b` (5.2GB). `ollama pull qwen3:8b`.
- Up to 64GB of RAM: `mistral-small3.1` (15GB) - 32GB users may find this option useful as well. `ollama pull mistral-small3.1`.

For Windows and Linux users the key thing to consider is the amount of VRAM available on your GPU - the above guidance should apply there as well, but I don't have much personal experience with Windows and Linux machines for running LLMs so I can't confidently provide a recommendation. Try the two smaller Qwen models first and see if Ollama can run them - you can use `ollama run qwen3:4b` and `ollama run qwen3:8b` to see if a chat interface starts running for those models.

Again, this step is *not required*. Many laptops will be unable to run these models, and the workshop is designed not to exclude anyone who does not have powerful enough hardware to experiment with models locally in this way.


## Tutorial description

Large Language Models such as GPT-4o, Claude and Google Gemini provide APIs that can be used to develop features that were almost impossibly difficult to build in the past, spanning areas that include human language understanding, image recognition and structured data extraction.

Building software that uses these APIs reliably and responsibly is a topic with a great deal of depth and a lot of hidden traps.

In this workshop we'll explore a range of proven techniques for building useful software on top of this wildly powerful but unreliable substrate.

Topics we will cover include:

* A review of the best currently available models
* Using multi-modal LLMs to analyze images, audio and video
* Use-cases that LLMs can be effectively applied to
* How to access the most capable models via their various APIs
* Prompt engineering
* Retrieval Augmented Generation (RAG)
* LLM tool usage
* Automated evaluations for LLM applications
* The latest options for running local models

Participants will obtain hands-on experience of building applications on LLMs. Necessary API keys will be provided.
