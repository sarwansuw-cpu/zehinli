# Zehinli EA — Session Memory

## Project Overview
- **Name:** Zehinli EA (Emeli Aň)
- **Purpose:** Türkmen dilinde doklad, referat, konspekt we prezentasiýa generirlemek
- **GitHub:** https://github.com/sarwansuw-cpu/zehinli.git
- **Token:** [REDACTED]

## Architecture
| Component | Technology |
|---|---|
| Language Model | Qwen2.5-7B-Instruct + LoRA (Unsloth) |
| Image Generation | Stable Diffusion XL (Hugging Face API) |
| Backend | FastAPI |
| Web Interface | Gradio (in Turkmen) |
| Fine-tuning Framework | Unsloth |
| Templates | doklad, referat, konspekt, prezentasiýa |

## Corpus
- **Sources:** kitaphana.net, enedilim.com, ajapsozluk.com
- **Total texts collected:** 2084
- **Training set:** 1875 texts
- **Validation set:** 209 texts
- **Location:** `data/processed/corpus.jsonl`

## Files Created
- `config/settings.py` — project configuration
- `src/model/inference.py` — model loading and generation
- `src/model/fine_tune.py` — Unsloth LoRA fine-tuning pipeline
- `src/templates/template_manager.py` — 4 template types
- `src/generators/report_generator.py` — text generation
- `src/generators/image_generator.py` — SDXL image generation
- `src/web/api.py` — FastAPI backend
- `src/web/gradio_app.py` — Gradio UI (Turkmen language)
- `main.py` — entry point
- `scripts/scrape_corpus.py` — Turkmen corpus scraper
- `scripts/prepare_dataset.py` — data cleaning/preparation
- `notebooks/zehinli_finetune_colab.ipynb` — Colab fine-tuning notebook (JSON issues, cached)
- `notebooks/zehinli_finetune_colab.py` — Colab fine-tuning script (clean version, recommended)
- `memoryzehinli.md` — session memory file

## User's Server
- **Type:** G8 Dedicated
- **Specs:** 256GB RAM, 128 vCPU, 2621GB storage, 40 Gbps
- **No GPU** — fine-tuning must be done on Google Colab
- **Purpose:** Hosting FastAPI + Gradio web interface

## Current Status
- ✅ Project structure created
- ✅ Corpus collected and processed (2084 texts)
- ✅ Colab notebook created (.ipynb + .py versions)
- ✅ **FIXED:** torch/torchvision version conflict & git clone error
- ⏳ User needs to push fixes to GitHub, then re-run in Colab

## Colab Training
**Рекомендуемый способ:**
1. Открыть https://colab.research.google.com/
2. Создать **"Новый ноутбук"**
3. Вставить в первую ячейку:
   ```
   !wget -O zehinli_train.py https://raw.githubusercontent.com/sarwansuw-cpu/zehinli/main/notebooks/zehinli_finetune_colab.py
   !python3 zehinli_train.py
   ```
4. **ВАЖНО:** Среда выполнения → Сменить среду выполнения → T4 GPU
5. Среда выполнения → Выполнить всё

**Что исправлено:**
- **Ошибка torch/torchvision:** Colab теперь (2026) поставляется с torch 2.13.0. Старый скрипт пытался force-reinstall torch 2.5.0, что не сработало. Теперь: `pip uninstall -y torch` → `pip install unsloth[colab-new]` (unsloth сам тянет совместимый torch).
- **Ошибка `!pip install` в .py:** Скрипт содержал `!pip` (IPython магия), не работал через `python3`. Переписан на `subprocess.check_call`.
- **Ошибка git clone:** При повторном запуске `git clone` падал. Теперь проверка `if os.path.exists`: `git pull` вместо `git clone`.
- **TRL:** Вместо `git+https://github.com/huggingface/trl.git` используется стабильный `trl` из pip.

## Notes
- DeepSeek V4 Flash cannot be self-hosted — using Qwen2.5-7B instead
- Fine-tuning requires GPU (Colab free tier works)
- Web interface can run on server without GPU (CPU inference)
- Interface language: Turkmen (Türkmen)
