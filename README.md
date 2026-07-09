# Zehinli EA (Emeli Aň)

Türkmen dilinde doklad, referat, konspekt we prezentasiýa generirlemek üçin emeli aň sistemsy.

## Mümkinçilikler
- Doklad generirlemek
- Referat generirlemek
- Konspekt generirlemek
- Prezentasiýa generirlemek (tekst + suratlar)
- Türkmen diliniň grammatikasyna we orfografiýasyna doly eýerýär

## Gurnama

```bash
git clone https://github.com/sarwansuw-cpu/zehinli.git
cd zehinli
pip install -r requirements.txt
```

## Ulanylyşy

```bash
python main.py
```

ýa-da web interfeýs üçin:

```bash
python webui.py
```

## Teknologiýalar
- Model: Qwen2.5-7B-Instruct (fine-tuned türkmen dilinde)
- Surat generasiýasy: Stable Diffusion XL
- Backend: FastAPI
- Web interfeýs: Gradio
- Framework: Unsloth (LoRA fine-tuning)