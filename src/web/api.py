from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.generators.report_generator import ReportGenerator
from src.generators.image_generator import ImageGenerator
from src.templates.template_manager import TemplateManager

app = FastAPI(title="Zehinli EA API", version="0.1.0")
generator = ReportGenerator()
image_gen = ImageGenerator()
templates = TemplateManager()

class GenerateRequest(BaseModel):
    template: str
    topic: str
    length: str = "orta"
    content_detail: str = ""
    source: str = ""
    source_text: str = ""
    slide_count: int = 10

class GenerateResponse(BaseModel):
    text: str
    template: str

class ImageRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""

@app.get("/")
def root():
    return {"message": "Zehinli EA - Türkmen emeli aň sistemsy"}

@app.get("/templates")
def list_templates():
    return {"templates": templates.list_templates()}

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    try:
        text = generator.generate(
            template_name=req.template,
            topic=req.topic,
            length=req.length,
            content_detail=req.content_detail,
            source=req.source,
            source_text=req.source_text,
            slide_count=req.slide_count,
        )
        return GenerateResponse(text=text, template=req.template)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-image")
def generate_image(req: ImageRequest):
    try:
        img_bytes = image_gen.generate(req.prompt, req.negative_prompt)
        if img_bytes:
            from fastapi.responses import Response
            return Response(content=img_bytes, media_type="image/png")
        raise HTTPException(status_code=500, detail="Surat generirlemek başartmady")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
