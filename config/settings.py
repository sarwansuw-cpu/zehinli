import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    PROJECT_NAME = "Zehinli EA"
    VERSION = "0.1.0"

    # Model
    MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
    MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", str(BASE_DIR / "models"))
    DEVICE = os.getenv("DEVICE", "cuda")
    USE_4BIT = os.getenv("USE_4BIT", "true").lower() == "true"

    # Fine-tuning
    LORA_R = 16
    LORA_ALPHA = 32
    LORA_DROPOUT = 0.05
    MAX_SEQ_LENGTH = 2048
    BATCH_SIZE = 4
    LEARNING_RATE = 2e-4
    NUM_EPOCHS = 3

    # Corpus
    CORPUS_DIR = BASE_DIR / "data" / "corpus"
    PROCESSED_DIR = BASE_DIR / "data" / "processed"

    # API Keys
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY", "")

    # Web
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "7860"))

    # Sources
    SOURCES = [
        "https://kitaphana.net",
        "https://enedilim.com",
        "https://ajapsozluk.com",
    ]
