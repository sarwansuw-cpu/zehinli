# Zehinli EA - Qwen2.5-7B Fine-tuning
# Turkmen dilinde doklad, referat, konspekt we prezentasiya

import subprocess
import sys
import os
import json

def pip_install(*packages):
    cmd = [sys.executable, '-m', 'pip', 'install', '-q']
    cmd.extend(packages)
    subprocess.check_call(cmd)

def run_cmd(*args):
    subprocess.check_call(args)

# 1. Gerekli kitaplanalary gurnamak
pip_install('--upgrade', 'pip')
pip_install('unsloth[colab-new]', 'bitsandbytes')
pip_install('transformers', 'datasets', 'accelerate', 'sentencepiece', 'protobuf', 'trl')

# 2. Repony klonlamak we korpusy yuklemek
from datasets import Dataset

if os.path.exists('/content/zehinli'):
    run_cmd('git', '-C', '/content/zehinli', 'pull')
else:
    run_cmd('git', 'clone', 'https://github.com/sarwansuw-cpu/zehinli.git')

corpus_path = '/content/zehinli/data/processed/corpus.jsonl'
texts = []
with open(corpus_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            texts.append(json.loads(line)['text'])
print(f'Jemi tekstler: {len(texts)}')

# 3. Unsloth bilen modeli yuklemek
import torch
from unsloth import FastLanguageModel

MAX_SEQ_LENGTH = 2048
MODEL_NAME = 'Qwen/Qwen2.5-7B-Instruct'

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=None,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj'],
    use_rslora=True,
)
print(f'Model yuklendi. Parametrler: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}')

# 4. Okuw ucin maglumatlary tayyarlamak
def format_conversation(text):
    mid = len(text) // 2
    user_part = text[:mid].strip()
    assistant_part = text[mid:].strip()
    if len(assistant_part) < 20:
        assistant_part = text
        user_part = f'Bu tema barada maglumat ber: {text[:50]}...'
    return tokenizer.apply_chat_template([
        {'role': 'system', 'content': 'Sen turkmen dilinde gurleyan emeli an. Turkmen dilinin grammatikasyna we orfografiyasyna doly eyerayarsin.'},
        {'role': 'user', 'content': user_part[:500]},
        {'role': 'assistant', 'content': assistant_part[:500]},
    ], tokenize=False)

formatted = [format_conversation(t) for t in texts]
dataset = Dataset.from_list([{'text': f} for f in formatted])
print(f'Okuw toplumy: {len(dataset)} mysal')

# 5. Fine-tuning baslatmak
from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field='text',
    max_seq_length=MAX_SEQ_LENGTH,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        optim='adamw_8bit',
        weight_decay=0.01,
        lr_scheduler_type='linear',
        seed=42,
        output_dir='zehinli_output',
        report_to='none',
    ),
)
print('Okuw baslayar...')
trainer.train()
print('OKUW TAMAM!')

# 6. Modeli yatda saklamak
from google.colab import drive
drive.mount('/content/drive')
save_path = '/content/drive/MyDrive/zehinli-model-v1'
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
print(f'Model yazdy: {save_path}')

# 7. Test - modelin isleysini barlamak
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name='/content/drive/MyDrive/zehinli-model-v1',
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)

def test_generate(prompt):
    messages = [
        {'role': 'system', 'content': 'Sen turkmen dilinde gurleyan emeli an.'},
        {'role': 'user', 'content': prompt},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors='pt').to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split('assistant')[-1].strip()

print(test_generate('Turkmenistanyn paytagty barada maglumat ber'))
