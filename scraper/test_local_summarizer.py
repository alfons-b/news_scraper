from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# ============================================================
# 1. PATH MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "summarizer"
    / "model_indonesian_summarizer"
)


# ============================================================
# 2. DEVICE
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 70)
print("LOCAL SUMMARIZER TEST")
print("=" * 70)

print(f"Model path : {MODEL_PATH}")
print(f"Device     : {device}")


# ============================================================
# 3. LOAD TOKENIZER
# ============================================================

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

print("Tokenizer berhasil dimuat.")


# ============================================================
# 4. LOAD MODEL
# ============================================================

print("\nLoading model...")

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model.to(device)
model.eval()

print("Model berhasil dimuat.")


# ============================================================
# 5. TEKS UJI
# ============================================================

text = """
Pemerintah Provinsi Nusa Tenggara Timur menggelar rapat
koordinasi pengendalian inflasi daerah di Kabupaten Timor
Tengah Selatan. Kegiatan tersebut dilakukan setelah daerah
tersebut mengalami deflasi pada Agustus 2026. Pemerintah
bersama sejumlah pihak membahas kondisi harga dan pasokan
komoditas pangan serta langkah yang perlu dilakukan untuk
menjaga stabilitas harga.
"""


# ============================================================
# 6. TOKENISASI
# ============================================================

inputs = tokenizer(
    text,
    return_tensors="pt",
    truncation=True,
    max_length=512
)

inputs = {
    key: value.to(device)
    for key, value in inputs.items()
}

print("\n" + "=" * 70)
print("INPUT")
print("=" * 70)

print(f"Jumlah token input : {inputs['input_ids'].shape[1]}")


# ============================================================
# 7. GENERATE SUMMARY
# ============================================================

print("\nGenerating summary...")

with torch.no_grad():

    outputs = model.generate(
        **inputs,

        # Untuk tahap pengujian awal,
        # gunakan generation_config dari model
        max_length=120,
        min_length=30,

        num_beams=5,
        do_sample=False,

        no_repeat_ngram_size=2,

        repetition_penalty=1.0
    )


# ============================================================
# 8. DECODE
# ============================================================

summary = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)


# ============================================================
# 9. HASIL
# ============================================================

print("\n" + "=" * 70)
print("HASIL SUMMARY")
print("=" * 70)

print(summary)

print("\n" + "=" * 70)
print("INFORMASI OUTPUT")
print("=" * 70)

print(f"Jumlah token output : {outputs.shape[1]}")

input_tokens = inputs["input_ids"].shape[1]
output_tokens = outputs.shape[1]

print(
    f"Compression ratio  : "
    f"{output_tokens / input_tokens:.2%}"
)

print("\nModel lokal berhasil digunakan.")