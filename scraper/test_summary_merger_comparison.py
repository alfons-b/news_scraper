from scraper.summarization.summary_merger import SummaryMerger
from scraper.summarization.summary_merger_v2 import SummaryMergerV2


CHUNK_SUMMARIES = [
    """
    Project In Flores memberikan pelatihan kepada Kelompok Tani Hutan (KTH),
    pelaku wisata, dan pelaku UMKM di Kecamatan Riung, Kabupaten Ngada, NTT.
    Pelatihan tersebut menjadi bagian dari upaya mendorong pemulihan ekonomi
    masyarakat lokal setelah gempa Flores yang mengguncang wilayah tersebut
    pada Minggu "15/8/2026".
    """,

    """
    Projek In Flores memiliki batas waktu pendampingan hingga 2028, setelah
    itu kita harus bisa mengembangkan diri sendiri, untuk bisa berjalan secara
    mandiri," ujar Dr. Nicolaus. Ia mengatakan, kemandirian tersebut harus
    mulai dipersiapkan sejak sekarang, termasuk dalam pengembangan bisnis dan
    pemasaran produk maupun jasa yang dikelola masyarakat.
    """
]


def count_words(text):
    return len(text.split())


print("=" * 70)
print("PERBANDINGAN SUMMARY MERGER V1 vs V2")
print("=" * 70)


# ============================================================
# V1
# ============================================================

merger_v1 = SummaryMerger(
    similarity_threshold=0.80
)

result_v1 = merger_v1.merge(CHUNK_SUMMARIES)


# ============================================================
# V2
# ============================================================

merger_v2 = SummaryMergerV2(
    similarity_threshold=0.40,
    containment_threshold=0.80
)

result_v2 = merger_v2.merge(CHUNK_SUMMARIES)


# ============================================================
# OUTPUT V1
# ============================================================

print("\n")
print("=" * 70)
print("HASIL V1")
print("=" * 70)

print(result_v1)

print("\nJumlah kata V1:")
print(count_words(result_v1))


# ============================================================
# OUTPUT V2
# ============================================================

print("\n")
print("=" * 70)
print("HASIL V2")
print("=" * 70)

print(result_v2)

print("\nJumlah kata V2:")
print(count_words(result_v2))


# ============================================================
# PERBANDINGAN
# ============================================================

print("\n")
print("=" * 70)
print("PERBANDINGAN")
print("=" * 70)

v1_words = count_words(result_v1)
v2_words = count_words(result_v2)

print(f"Jumlah kata V1 : {v1_words}")
print(f"Jumlah kata V2 : {v2_words}")

print("\nSelisih kata:")
print(v1_words - v2_words)