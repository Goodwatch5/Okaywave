import base64
import io
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image
import gradio as gr


MODEL = "allenai/Molmo2-8B"
INFERENCE_URL = "https://router.huggingface.co/v1/chat/completions"
MAX_IMAGE_SIZE = (1536, 1536)


def answer_image_question(image: Image.Image | None, question: str) -> str:
    token = os.environ.get("HF_TOKEN")
    if not token:
        return "The demo is not configured yet. Add an HF_TOKEN secret to the Space settings."
    if image is None:
        return "Upload an image to ask a question about it."
    if not question or not question.strip():
        return "Enter a question about the image."

    prepared = image.convert("RGB")
    prepared.thumbnail(MAX_IMAGE_SIZE)
    buffer = io.BytesIO()
    prepared.save(buffer, format="JPEG", quality=85, optimize=True)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("ascii")
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question.strip()},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        },
                    },
                ],
            }
        ],
        "max_tokens": 512,
    }
    request = Request(
        INFERENCE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=90) as response:
            result = json.loads(response.read())
    except HTTPError as error:
        if error.code in (401, 403):
            return "Hugging Face rejected the Space token. Check the HF_TOKEN secret and its Inference Providers access."
        if error.code == 429:
            return "The inference provider is busy or rate-limited. Try again shortly."
        return f"The inference request failed with HTTP {error.code}."
    except (URLError, TimeoutError):
        return "Could not reach the Hugging Face inference service. Try again shortly."
    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
        return "The inference service returned an unexpected response."

    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return "The inference service returned an unexpected response."
    if not isinstance(content, str) or not content.strip():
        return "The model returned an empty answer."
    return content.strip()


demo = gr.Interface(
    fn=answer_image_question,
    inputs=[
        gr.Image(type="pil", label="Image"),
        gr.Textbox(
            label="Question",
            placeholder="What is happening in this image?",
            lines=2,
        ),
    ],
    outputs=gr.Textbox(label="Answer", lines=6),
    title="Okaywave Visual Q&A",
    description=(
        "Ask a question about an image. Okaywave sends the image and question "
        "to the Hugging Face Inference Providers router using Molmo2."
    ),
    examples=None,
)


if __name__ == "__main__":
    demo.launch()
