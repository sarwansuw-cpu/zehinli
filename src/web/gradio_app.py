import gradio as gr
from src.generators.report_generator import ReportGenerator
from src.generators.image_generator import ImageGenerator
from src.templates.template_manager import TemplateManager

generator = ReportGenerator()
image_gen = ImageGenerator()
templates = TemplateManager()

def generate_text(template, topic, length, content_detail, source, source_text, slide_count):
    if not topic and not source_text:
        return "Tema ýa-da tekst ýazmaly!"
    try:
        result = generator.generate(
            template_name=template,
            topic=topic or "Bellik edilmedi",
            length=length,
            content_detail=content_detail,
            source=source,
            source_text=source_text,
            slide_count=int(slide_count),
        )
        return result
    except Exception as e:
        return f"Ýalňyşlyk: {str(e)}"

def generate_image(prompt, negative_prompt=""):
    if not prompt:
        return None, "Surat beýanyny ýazmaly!"
    try:
        img_bytes = image_gen.generate(prompt, negative_prompt)
        if img_bytes:
            import tempfile, os
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            tmp.write(img_bytes)
            tmp.close()
            return tmp.name, "Surat üstünlikli döredildi!"
        return None, "Surat generirlemek başartmady. API açary barlaň."
    except Exception as e:
        return None, f"Ýalňyşlyk: {str(e)}"

template_list = templates.list_templates()

with gr.Blocks(title="Zehinli EA", theme=gr.themes.Soft()) as app:
    gr.Markdown("# Zehinli EA (Emeli Aň)")
    gr.Markdown("Türkmen dilinde doklad, referat, konspekt we prezentasiýa generirlemek")

    with gr.Tab("Tekst generirlemek"):
        with gr.Row():
            with gr.Column(scale=1):
                template_dd = gr.Dropdown(
                    choices=template_list,
                    value=template_list[0],
                    label="Görnüşi"
                )
                length_dd = gr.Dropdown(
                    choices=["gysga (200 söz)", "orta (500 söz)", "uzyn (1000 söz)"],
                    value="orta (500 söz)",
                    label="Uzynlygy"
                )
                slide_count = gr.Number(value=10, label="Slayd sany (prezentasiýa üçin)", visible=False)
                def update_visibility(template):
                    return gr.update(visible=(template == "prezentasiya"))
                template_dd.change(fn=update_visibility, inputs=template_dd, outputs=slide_count)

            with gr.Column(scale=2):
                topic = gr.Textbox(label="Tema", placeholder="Temany ýazyň...")
                content_detail = gr.Textbox(label="Goşmaça maglumatlar (islege görä)", placeholder="Tema barada goşmaça maglumat...", lines=3)
                source = gr.Textbox(label="Çeşme (referat üçin)", placeholder="Kitap/makala ady...")
                source_text = gr.Textbox(label="Tekst (konspekt üçin)", placeholder="Konspekt ediljek teksti ýazyň...", lines=5)

                generate_btn = gr.Button("Generirlemek", variant="primary")
                output = gr.Markdown(label="Netije")

                generate_btn.click(
                    fn=generate_text,
                    inputs=[template_dd, topic, length_dd, content_detail, source, source_text, slide_count],
                    outputs=output
                )

    with gr.Tab("Surat generirlemek"):
        with gr.Row():
            with gr.Column():
                img_prompt = gr.Textbox(
                    label="Surat beýany",
                    placeholder="Suratda näme bolmaly?",
                    lines=3
                )
                img_neg = gr.Textbox(
                    label="Bolmaly däl zatlar (islege görä)",
                    placeholder="Suratda bolmaly däl zatlar...",
                    lines=2
                )
                img_btn = gr.Button("Surat döret", variant="primary")
            with gr.Column():
                img_output = gr.Image(label="Döredilen surat")
                img_status = gr.Textbox(label="Status")

        img_btn.click(
            fn=generate_image,
            inputs=[img_prompt, img_neg],
            outputs=[img_output, img_status]
        )

    with gr.Tab("Kömek"):
        gr.Markdown("""
        ## Zehinli EA ulanylyşy

        **Tekst generirlemek:**
        1. Görnüşini saýlaň (doklad, referat, konspekt, prezentasiýa)
        2. Temany ýazyň
        3. Uzynlygy saýlaň
        4. "Generirlemek" düwmesine basyň

        **Surat generirlemek:**
        1. Surat beýanyny ýazyň (türkmen dilinde)
        2. "Surat döret" düwmesine basyň

        **Bellik:** Ilkinji gezek ulanylanda model ýüklenýär, bu birnäçe minut wagt alyp biler.
        """)

def run_gradio():
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )

if __name__ == "__main__":
    run_gradio()
