---
title: Okaywave Visual Q&A
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
python_version: "3.10"
---

# Okaywave Visual Q&A

Okaywave is a small image-question-answering demo based on the repository's
Hugging Face notebook. Upload an image, enter a question, and receive an answer
from `allenai/Molmo2-8B` through the Hugging Face Inference Providers router.

The Space calls the hosted inference API; it does not download or run the model
inside the Space. Image content and the question are sent to the inference
provider for each request.

## Run locally

Requires Python 3.10 or later and a Hugging Face token with access to Inference
Providers.

```bash
python -m venv .venv
# Activate the virtual environment for your operating system.
python -m pip install -r requirements.txt
```

Set `HF_TOKEN` in your shell, then start the app:

```bash
python app.py
```

Do not commit the token. The app reports a configuration message when
`HF_TOKEN` is not set.

## Hugging Face Spaces setup

Create a new **Gradio** Space and import this repository, or connect the Space
to this repository after merging the app changes. The README metadata selects
Gradio SDK version 5.49.1 and `app.py` as the entry point. In the Space's
Settings → Repository secrets, add `HF_TOKEN` with a Hugging Face token that
has Inference Providers access. The token is read only from the environment and
is never included in the UI or application responses.

Inference provider availability, model access, rate limits, and any usage costs
depend on the Hugging Face account and provider configuration.
