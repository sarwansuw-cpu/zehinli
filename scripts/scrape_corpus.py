"""
Türkmen dilindäki tekstleri ýygnamak skripti
Sources: kitaphana.net, enedilim.com, ajapsozluk.com
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from pathlib import Path
from typing import Set, List, Optional
from urllib.parse import urljoin

class TurkmenCorpusScraper:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.seen_urls: Set[str] = set()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ZehinliEA/1.0"
        })

    def is_turkmen_text(self, text: str) -> bool:
        """Check if text contains Turkmen characters"""
        turkmen_chars = set("äöüýňşçžÄÖÜÝŇŞÇŽ")
        return bool(set(text) & turkmen_chars)

    def extract_text(self, html: str, selector: str = "p, h1, h2, h3, h4, li, td") -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        texts = []
        for tag in soup.select(selector):
            text = tag.get_text(strip=True)
            if len(text) > 20 and self.is_turkmen_text(text):
                texts.append(text)
        return texts

    def scrape_enedilim(self):
        print("📖 Enedilim.com sahypasyndan tekst ýygnalýar...")
        try:
            resp = self.session.get("https://enedilim.com/", timeout=15)
            texts = self.extract_text(resp.text)
            self._save_texts(texts, "enedilim_main")
            print(f"  ✓ {len(texts)} tekst tapyldy")

            # Scrape dictionary pages
            for letter in "aäbçdefghijklmnoöprsştuüwyýz":
                try:
                    url = f"https://enedilim.com/s%C3%B6zluk/{letter}"
                    resp = self.session.get(url, timeout=10)
                    texts = self.extract_text(resp.text)
                    self._save_texts(texts, f"enedilim_dict_{letter}")
                    time.sleep(1)
                except Exception as e:
                    print(f"  ✗ {letter}: {e}")
        except Exception as e:
            print(f"  ✗ Enedilim: {e}")

    def scrape_kitaphana(self):
        print("📖 Kitaphana.net sahypasyndan tekst ýygnalýar...")
        try:
            resp = self.session.get("https://kitaphana.net/", timeout=15)
            soup = BeautifulSoup(resp.text, "html.parser")

            # Find book links
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if "/kitap/" in href or "/book/" in href:
                    full_url = urljoin("https://kitaphana.net", href)
                    if full_url not in self.seen_urls:
                        self.seen_urls.add(full_url)
                        try:
                            time.sleep(1)
                            book_resp = self.session.get(full_url, timeout=10)
                            texts = self.extract_text(book_resp.text)
                            if texts:
                                self._save_texts(texts, f"kitaphana_{len(self.seen_urls)}")
                                print(f"  ✓ {len(texts)} tekst ({full_url[:50]}...)")
                        except Exception:
                            continue
        except Exception as e:
            print(f"  ✗ Kitaphana: {e}")

    def scrape_ajapsozluk(self):
        print("📖 Ajapsozluk.com sahypasyndan sözler ýygnalýar...")
        try:
            resp = self.session.get("https://ajapsozluk.com/", timeout=15)
            texts = self.extract_text(resp.text)
            turkmen_words = [t for t in texts if self.is_turkmen_text(t)]
            self._save_texts(turkmen_words, "ajapsozluk_main")
            print(f"  ✓ {len(turkmen_words)} söz tapyldy")
        except Exception as e:
            print(f"  ✗ Ajapsozluk: {e}")

    def _save_texts(self, texts: List[str], source: str):
        if not texts:
            return
        filepath = self.output_dir / f"{source}.jsonl"
        with open(filepath, "a", encoding="utf-8") as f:
            for text in texts:
                record = {"text": text, "source": source}
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def run(self):
        print("=" * 50)
        print("Türkmen korpusyny ýygnamak başlandy")
        print("=" * 50)
        self.scrape_enedilim()
        self.scrape_kitaphana()
        self.scrape_ajapsozluk()
        print(f"\n✅ Korpus ýygnaldy: {self.output_dir}")
        print(f"   Jemi faýllar: {len(list(self.output_dir.glob('*.jsonl')))}")

if __name__ == "__main__":
    output_dir = Path(__file__).resolve().parent.parent / "data" / "corpus"
    scraper = TurkmenCorpusScraper(output_dir)
    scraper.run()
