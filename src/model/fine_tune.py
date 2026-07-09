from unsloth import FastLanguageModel
import torch
from datasets import Dataset
from transformers import TrainingArguments
from trl import SFTTrainer
from pathlib import Path

def prepare_model():
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="Qwen/Qwen2.5-7B-Instruct",
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        use_rslora=True,
    )
    return model, tokenizer

def train_on_turkmen_corpus(
    corpus_path: Path,
    output_dir: Path,
    num_epochs: int = 3,
    batch_size: int = 4,
):
    model, tokenizer = prepare_model()

    import json
    with open(corpus_path, "r", encoding="utf-8") as f:
        texts = [json.loads(line)["text"] for line in f if line.strip()]

    def format_text(text):
        return {
            "text": tokenizer.apply_chat_template([
                {"role": "system", "content": "Sen türkmen dilinde gürleýän emeli aň. Türkmen diliniň grammatikasyna we orfografiýasyna doly eýerýärsiň."},
                {"role": "user", "content": text[:100] + "..."},
                {"role": "assistant", "content": text}
            ], tokenize=False)
        }

    dataset = Dataset.from_list([format_text(t) for t in texts])

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=TrainingArguments(
            output_dir=str(output_dir),
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            warmup_steps=10,
            learning_rate=2e-4,
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            logging_steps=10,
            save_strategy="epoch",
            push_to_hub=False,
        ),
    )
    trainer.train()
    model.save_pretrained(str(output_dir / "lora"))
    tokenizer.save_pretrained(str(output_dir / "lora"))
    return model, tokenizer
