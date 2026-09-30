import re
from pathlib import Path

from transformers import AutoTokenizer

from scraper.summarization.chunker import TextChunker


# ============================================================
# 1. LOAD TOKENIZER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "summarizer"
    / "model_indonesian_summarizer"
)

print("=" * 70)
print("TEST TEXT CHUNKER")
print("=" * 70)

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

print("Tokenizer berhasil dimuat.")


# ============================================================
# 2. MEMBUAT DATA TEST
# ============================================================

def create_test_article():
    """
    Membuat artikel sintetis dengan paragraf yang memiliki
    ID unik sehingga overlap antar-chunk dapat diverifikasi.
    """

    paragraphs = []

    base_text = (
        "Pemerintah daerah melakukan pemantauan terhadap kondisi "
        "ekonomi wilayah dan perkembangan aktivitas masyarakat. "
        "Informasi tersebut digunakan untuk melihat perubahan "
        "kegiatan ekonomi serta kondisi sektor yang berkaitan "
        "dengan produksi, perdagangan, konsumsi, dan distribusi."
    )

    for i in range(1, 21):
        paragraph = (
            f"PARAGRAF_{i:02d}. "
            f"{base_text} "
            f"Data pada paragraf ini merupakan bagian ke-{i} "
            f"dari rangkaian informasi ekonomi yang sedang dianalisis."
        )

        paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)


ARTICLE_TEXT = create_test_article()


# ============================================================
# 3. FUNGSI UNTUK MENGAMBIL ID PARAGRAF
# ============================================================

def get_paragraph_ids(text):
    """
    Mengambil ID seperti PARAGRAF_01, PARAGRAF_02, dst.
    """

    return re.findall(
        r"PARAGRAF_\d+",
        text
    )


# ============================================================
# 4. INISIALISASI CHUNKER
# ============================================================

chunker = TextChunker(
    tokenizer=tokenizer,
    max_tokens=450,
    overlap_paragraphs=2
)


# ============================================================
# 5. HITUNG TOTAL TOKEN
# ============================================================

total_tokens = chunker.count_tokens(
    ARTICLE_TEXT
)

original_paragraph_ids = get_paragraph_ids(
    ARTICLE_TEXT
)

print("\nDATA ARTIKEL TEST")
print("-" * 70)
print(f"Jumlah paragraf : {len(original_paragraph_ids)}")
print(f"Jumlah token    : {total_tokens}")


# ============================================================
# 6. BUAT CHUNKS
# ============================================================

chunks = chunker.create_chunks(
    ARTICLE_TEXT
)

print("\nHASIL CHUNKING")
print("-" * 70)
print(f"Jumlah chunks   : {len(chunks)}")


for index, chunk in enumerate(chunks, start=1):

    token_count = chunker.count_tokens(chunk)
    paragraph_ids = get_paragraph_ids(chunk)

    print(f"\nChunk {index}")
    print(f"  Token      : {token_count}")
    print(f"  Paragraf   : {len(paragraph_ids)}")
    print(f"  ID         : {paragraph_ids}")


# ============================================================
# 7. TEST 1 — SEMUA CHUNK ≤ 450 TOKEN
# ============================================================

print("\n")
print("=" * 70)
print("TEST 1 — BATAS MAKSIMAL TOKEN")
print("=" * 70)

token_limit_passed = True

for index, chunk in enumerate(chunks, start=1):

    token_count = chunker.count_tokens(chunk)

    if token_count > 450:
        print(
            f"❌ Chunk {index} melebihi batas: "
            f"{token_count} token"
        )
        token_limit_passed = False

    else:
        print(
            f"✅ Chunk {index}: "
            f"{token_count} token"
        )


# ============================================================
# 8. TEST 2 — CEK OVERLAP 2 PARAGRAF
# ============================================================

print("\n")
print("=" * 70)
print("TEST 2 — OVERLAP 2 PARAGRAF")
print("=" * 70)

overlap_passed = True

for i in range(len(chunks) - 1):

    current_ids = get_paragraph_ids(
        chunks[i]
    )

    next_ids = get_paragraph_ids(
        chunks[i + 1]
    )

    overlap = [
        paragraph_id
        for paragraph_id in current_ids
        if paragraph_id in next_ids
    ]

    expected_overlap = current_ids[-2:]

    print(
        f"\nChunk {i + 1} → Chunk {i + 2}"
    )

    print(
        f"  Akhir chunk sebelumnya : "
        f"{expected_overlap}"
    )

    print(
        f"  Overlap aktual         : "
        f"{overlap}"
    )

    if overlap != expected_overlap:
        print("  ❌ OVERLAP TIDAK SESUAI")
        overlap_passed = False

    else:
        print("  ✅ Overlap sesuai")


# ============================================================
# 9. TEST 3 — TIDAK ADA PARAGRAF YANG HILANG
# ============================================================

print("\n")
print("=" * 70)
print("TEST 3 — TIDAK ADA PARAGRAF HILANG")
print("=" * 70)

all_chunk_paragraph_ids = []

for chunk in chunks:

    paragraph_ids = get_paragraph_ids(
        chunk
    )

    all_chunk_paragraph_ids.extend(
        paragraph_ids
    )

unique_chunk_paragraph_ids = set(
    all_chunk_paragraph_ids
)

original_paragraph_id_set = set(
    original_paragraph_ids
)

missing_paragraphs = (
    original_paragraph_id_set
    - unique_chunk_paragraph_ids
)

if not missing_paragraphs:

    print(
        "✅ Semua paragraf asli muncul "
        "minimal satu kali."
    )

    paragraph_completeness_passed = True

else:

    print(
        "❌ Ada paragraf yang hilang:"
    )

    print(
        sorted(missing_paragraphs)
    )

    paragraph_completeness_passed = False


# ============================================================
# 10. TEST 4 — CEK URUTAN PARAGRAF
# ============================================================

print("\n")
print("=" * 70)
print("TEST 4 — URUTAN PARAGRAF")
print("=" * 70)

order_passed = True

expected_numbers = list(
    range(1, 21)
)

found_numbers = sorted(
    set(
        int(
            paragraph_id.split("_")[1]
        )
        for paragraph_id in unique_chunk_paragraph_ids
    )
)

if found_numbers == expected_numbers:

    print(
        "✅ Semua paragraf PARAGRAF_01 "
        "sampai PARAGRAF_20 ditemukan."
    )

else:

    print(
        "❌ Urutan/kumpulan paragraf tidak sesuai."
    )

    print(
        f"Expected: {expected_numbers}"
    )

    print(
        f"Found   : {found_numbers}"
    )

    order_passed = False


# ============================================================
# 11. HASIL AKHIR
# ============================================================

print("\n")
print("=" * 70)
print("HASIL AKHIR TEST CHUNKER")
print("=" * 70)

print(
    f"Test batas token       : "
    f"{'PASS' if token_limit_passed else 'FAIL'}"
)

print(
    f"Test overlap            : "
    f"{'PASS' if overlap_passed else 'FAIL'}"
)

print(
    f"Test paragraf lengkap   : "
    f"{'PASS' if paragraph_completeness_passed else 'FAIL'}"
)

print(
    f"Test urutan paragraf    : "
    f"{'PASS' if order_passed else 'FAIL'}"
)


all_passed = (
    token_limit_passed
    and overlap_passed
    and paragraph_completeness_passed
    and order_passed
)


print("\n" + "=" * 70)

if all_passed:

    print("✅ SEMUA TEST CHUNKER BERHASIL")

else:

    print("❌ ADA TEST CHUNKER YANG GAGAL")

print("=" * 70)