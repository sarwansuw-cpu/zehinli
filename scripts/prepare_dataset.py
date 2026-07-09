"""
Türkmen korpusyny arassalamak we fine-tuning üçin taýýarlamak
"""

import json
import re
from pathlib import Path
from typing import List, Dict

class CorpusPreprocessor:
    def __init__(self, corpus_dir: Path, output_dir: Path):
        self.corpus_dir = corpus_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def clean_text(self, text: str) -> str:
        """Arassala we normalizirle"""
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^\w\säöüýňşçžÄÖÜÝŇŞÇŽ.,!?;:()\-"\'«»]', '', text)
        text = re.sub(r'\.{4,}', '...', text)
        text = re.sub(r'\s*\.\s*', '. ', text)
        text = re.sub(r'\s*,', ',', text)
        return text.strip()

    def is_quality_text(self, text: str) -> bool:
        if len(text) < 50:
            return False
        if len(text) > 10000:
            return False
        turkmen_chars = set("äöüýňşçžÄÖÜÝŇŞÇŽ")
        ratio = sum(1 for c in text if c in turkmen_chars) / max(len(text), 1)
        if ratio < 0.01:
            return False
        return True

    def merge_corpus(self) -> List[str]:
        all_texts = []
        for jsonl_file in sorted(self.corpus_dir.glob("*.jsonl")):
            with open(jsonl_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            record = json.loads(line)
                            text = self.clean_text(record.get("text", ""))
                            if self.is_quality_text(text):
                                all_texts.append(text)
                        except json.JSONDecodeError:
                            continue
        return all_texts

    def split_dataset(self, texts: List[str], train_ratio: float = 0.9):
        split_idx = int(len(texts) * train_ratio)
        train_texts = texts[:split_idx]
        val_texts = texts[split_idx:]

        with open(self.output_dir / "train.jsonl", "w", encoding="utf-8") as f:
            for t in train_texts:
                f.write(json.dumps({"text": t}, ensure_ascii=False) + "\n")

        with open(self.output_dir / "val.jsonl", "w", encoding="utf-8") as f:
            for t in val_texts:
                f.write(json.dumps({"text": t}, ensure_ascii=False) + "\n")

        # Create merged corpus for fine-tuning
        with open(self.output_dir / "corpus.jsonl", "w", encoding="utf-8") as f:
            for t in texts:
                f.write(json.dumps({"text": t}, ensure_ascii=False) + "\n")

        return train_texts, val_texts

    def run(self):
        print("Korpus arassalanýar we taýýarlanýar...")
        texts = self.merge_corpus()
        print(f"Jemi tekstler: {len(texts)}")
        train, val = self.split_dataset(texts)
        print(f"Okuw üçin: {len(train)} tekst")
        print(f"Barlag üçin: {len(val)} tekst")
        print(f"✅ Korpus taýýar: {self.output_dir / 'corpus.jsonl'}")

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    preprocessor = CorpusPreprocessor(
        corpus_dir=base / "data" / "corpus",
        output_dir=base / "data" / "processed"
    )
    preprocessor.run()
