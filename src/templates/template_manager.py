from typing import Dict, List, Optional
from pydantic import BaseModel

class Template(BaseModel):
    name: str
    description: str
    system_prompt: str
    user_prompt_template: str
    output_format: str  # "text" | "markdown" | "pptx"

class TemplateManager:
    def __init__(self):
        self.templates: Dict[str, Template] = {
            "doklad": Template(
                name="Doklad",
                description="Tema boýunça giňişleýin doklad taýýarlar",
                system_prompt="Sen türkmen dilinde doklad ýazýan emeli aň. Resmi we ylmy stilde ýazýarsyň. Türkmen diliniň grammatikasyna we orfografiýasyna doly eýerýärsiň.",
                user_prompt_template="""Tema: {topic}

Doklady aşakdaky gurluşda ýaz:
1. Giriş - temanyň ähmiýeti
2. Esasy bölüm - temany jikme-jik aç
3. Netije - esasy netijeler

Dokladyň uzynlygy: {length} söz

Mazmuny:
{content_detail}""",
                output_format="markdown"
            ),
            "referat": Template(
                name="Referat",
                description="Kitap ýa-da makala esasynda gysgaça referat ýazýar",
                system_prompt="Sen türkmen dilinde referat ýazýan emeli aň. Gysga we manyly ýazýarsyň. Türkmen diliniň grammatikasyna we orfografiýasyna doly eýerýärsiň.",
                user_prompt_template="""Çeşme: {source}
Tema: {topic}

Referaty aşakdaky gurluşda ýaz:
1. Umumy maglumat
2. Esasy mazmun
3. Sohbet netijesi

Referatyň uzynlygy: {length} söz""",
                output_format="markdown"
            ),
            "konspekt": Template(
                name="Konspekt",
                description="Teksti gysga we düşnükli konspekt görnüşinde ýazýar",
                system_prompt="Sen türkmen dilinde konspekt ýazýan emeli aň. Gysga, tertipli we düşnükli ýazýarsyň. Türkmen diliniň grammatikasyna we orfografiýasyna doly eýerýärsiň.",
                user_prompt_template="""Tekst: {source_text}

Konspekti aşakdaky ýaly tertipde ýaz:
• Esasy düşünjeler
• Möhüm maglumatlar
• Sözler we manylary""",
                output_format="markdown"
            ),
            "prezentasiya": Template(
                name="Prezentasiýa",
                description="Tema boýunça prezentasiýa taýýarlar (slaydlar)",
                system_prompt="Sen türkmen dilinde prezentasiýa taýýarlaýan emeli aň. Her slayd gysga we düşnükli bolmaly. Türkmen diliniň grammatikasyna we orfografiýasyna doly eýerýärsiň.",
                user_prompt_template="""Tema: {topic}
Slayd sany: {slide_count}

Her slayd üçin:
- Slayd ady
- Esasy 3-4 nokat
- Surat teklibi (islenýän suratyň beýany)""",
                output_format="markdown"
            ),
        }

    def get_template(self, name: str) -> Optional[Template]:
        return self.templates.get(name)

    def list_templates(self) -> List[str]:
        return list(self.templates.keys())

    def format_prompt(self, template_name: str, **kwargs) -> tuple:
        tmpl = self.get_template(template_name)
        if not tmpl:
            raise ValueError(f"Template '{template_name}' tapylmady")
        prompt = tmpl.user_prompt_template.format(**kwargs)
        return tmpl.system_prompt, prompt, tmpl.output_format
