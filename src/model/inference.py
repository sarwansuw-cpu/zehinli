import torch
from unsloth import FastLanguageModel
from typing import List, Optional
from config.settings import Config

class ZehinliModel:
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.tokenizer = None
        self.model_path = model_path or Config.MODEL_NAME
        self._load_model()

    def _load_model(self):
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.model_path,
            max_seq_length=Config.MAX_SEQ_LENGTH,
            dtype=None,
            load_in_4bit=Config.USE_4BIT,
        )
        FastLanguageModel.for_inference(self.model)

    def generate(
        self,
        prompt: str,
        system_prompt: str = "Sen türkmen dilinde gürleýän emeli aň. Türkmen diliniň grammatikasyna we orfografiýasyna doly eýerýärsiň.",
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=0.9,
            repetition_penalty=1.1,
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract assistant response
        if "assistant" in response:
            response = response.split("assistant")[-1].strip()
        return response

    def generate_stream(self, prompt: str, system_prompt: str = None):
        if system_prompt is None:
            system_prompt = "Sen türkmen dilinde gürleýän emeli aň. Türkmen diliniň grammatikasyna we orfografiýasyna doly eýerýärsiň."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        for token in self.model.generate(**inputs, max_new_tokens=2048, temperature=0.7, streamer=None):
            yield self.tokenizer.decode(token, skip_special_tokens=True)
