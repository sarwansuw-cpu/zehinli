import requests
import base64
from io import BytesIO
from typing import Optional
from config.settings import Config

class ImageGenerator:
    def __init__(self):
        self.hf_token = Config.HF_TOKEN
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

    def generate(self, prompt: str, negative_prompt: str = "") -> Optional[bytes]:
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": negative_prompt,
                "num_inference_steps": 25,
                "guidance_scale": 7.5,
            }
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                return response.content
            else:
                # Try Replicate as fallback
                return self._generate_replicate(prompt, negative_prompt)
        except Exception:
            return self._generate_replicate(prompt, negative_prompt)

    def _generate_replicate(self, prompt: str, negative_prompt: str = "") -> Optional[bytes]:
        if not Config.REPLICATE_API_KEY:
            return None
        try:
            resp = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers={"Authorization": f"Token {Config.REPLICATE_API_KEY}"},
                json={
                    "version": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    "input": {
                        "prompt": prompt,
                        "negative_prompt": negative_prompt,
                        "num_outputs": 1,
                    }
                },
                timeout=30
            )
            if resp.status_code == 201:
                prediction_id = resp.json().get("id")
                import time
                for _ in range(30):
                    status = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers={"Authorization": f"Token {Config.REPLICATE_API_KEY}"}
                    ).json()
                    if status.get("status") == "succeeded":
                        img_url = status["output"][0]
                        img_data = requests.get(img_url).content
                        return img_data
                    elif status.get("status") == "failed":
                        return None
                    time.sleep(2)
        except Exception:
            return None

    def image_to_base64(self, image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode("utf-8")
