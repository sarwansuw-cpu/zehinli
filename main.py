#!/usr/bin/env python3
"""
Zehinli EA (Emeli Aň) - Türkmen emeli aň sistemsy
"""

import argparse
import uvicorn
from config.settings import Config

def main():
    parser = argparse.ArgumentParser(description="Zehinli EA - Türkmen emeli aň sistemsy")
    parser.add_argument("--mode", choices=["web", "api", "train"], default="web",
                        help="Iş režimi: web (Gradio), api (FastAPI), train (oқатmak)")
    parser.add_argument("--port", type=int, default=Config.PORT)
    parser.add_argument("--host", default=Config.HOST)

    args = parser.parse_args()

    if args.mode == "web":
        from src.web.gradio_app import run_gradio
        run_gradio()
    elif args.mode == "api":
        uvicorn.run("src.web.api:app", host=args.host, port=args.port, reload=True)
    elif args.mode == "train":
        from src.model.fine_tune import train_on_turkmen_corpus
        train_on_turkmen_corpus(
            corpus_path=Config.PROCESSED_DIR / "corpus.jsonl",
            output_dir=Config.BASE_DIR / "models" / "zehinli-v1",
        )

if __name__ == "__main__":
    main()
