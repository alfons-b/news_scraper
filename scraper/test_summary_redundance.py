from scraper.summarization.summary_merger import SummaryMerger


SUMMARY_INPUTS = [
    """
    Project In Flores memberikan pelatihan kepada Kelompok Tani Hutan (KTH),
    pelaku wisata, dan pelaku UMKM di Kecamatan Riung, Kabupaten Ngada, NTT.
    Pelatihan tersebut menjadi bagian dari upaya mendorong pemulihan ekonomi
    masyarakat lokal setelah gempa Flores pada 15 Agustus 2026.
    """,

    """
    Project In Flores memberikan pelatihan kepada pelaku wisata dan pelaku UMKM
    di Kecamatan Riung, Kabupaten Ngada, NTT.
    Pelatihan tersebut bertujuan mendorong pemulihan ekonomi masyarakat lokal
    setelah gempa Flores.
    Projek In Flores memiliki batas waktu pendampingan hingga 2028.
    Masyarakat diharapkan mampu mengembangkan bisnis dan pemasaran produk maupun
    jasa secara mandiri setelah masa pendampingan berakhir.
    """
]


def count_words(text):
    return len(text.split())


print("=" * 70)
print("TEST SUMMARY MERGER - REDUNDANCY")
print("=" * 70)

merger = SummaryMerger(similarity_threshold=0.80)

print("\n")
print("=" * 70)
print("SUMMARY INPUT")
print("=" * 70)

for index, summary in enumerate(SUMMARY_INPUTS, start=1):
    print(f"\nSUMMARY {index}:")
    print(summary.strip())

print("\n")
print("=" * 70)
print("MERGING")
print("=" * 70)

merged_summary = merger.merge(SUMMARY_INPUTS)

print("\n")
print("=" * 70)
print("MERGED SUMMARY")
print("=" * 70)
print(merged_summary)

input_word_count = sum(
    count_words(summary)
    for summary in SUMMARY_INPUTS
)

output_word_count = count_words(merged_summary)

print("\n")
print("=" * 70)
print("INFORMASI")
print("=" * 70)

print(f"Jumlah summary input : {len(SUMMARY_INPUTS)}")
print(f"Total kata input     : {input_word_count}")
print(f"Total kata output    : {output_word_count}")

if input_word_count > 0:
    reduction = (
        (input_word_count - output_word_count)
        / input_word_count
    ) * 100
else:
    reduction = 0

print(f"Pengurangan kata     : {reduction:.2f}%")

print("\n")
print("=" * 70)
print("TEST SELESAI")
print("=" * 70)