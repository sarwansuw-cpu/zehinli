from typing import Optional
from src.model.inference import ZehinliModel
from src.templates.template_manager import TemplateManager

class ReportGenerator:
    def __init__(self, model: Optional[ZehinliModel] = None):
        self.model = model or ZehinliModel()
        self.templates = TemplateManager()

    def generate(
        self,
        template_name: str,
        topic: str,
        length: str = "orta",
        content_detail: str = "",
        source: str = "",
        source_text: str = "",
        slide_count: int = 10,
    ) -> str:
        kwargs = {
            "topic": topic,
            "length": length,
            "content_detail": content_detail,
            "source": source,
            "source_text": source_text,
            "slide_count": slide_count,
        }

        system_prompt, user_prompt, fmt = self.templates.format_prompt(template_name, **kwargs)
        return self.model.generate(user_prompt, system_prompt=system_prompt)
