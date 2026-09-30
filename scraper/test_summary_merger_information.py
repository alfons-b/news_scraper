from scraper.summarization.summary_merger import SummaryMerger


SUMMARY_INPUTS = [
    """
    Pemerintah daerah melakukan pelatihan kepada pelaku UMKM untuk mendorong
    pemulihan ekonomi masyarakat setelah gempa.
    Kegiatan tersebut dilaksanakan di Kecamatan Riung, Kabupaten Ngada.
    """,

    """
    Pemerintah daerah melakukan pelatihan kepada pelaku UMKM untuk mendorong
    pemulihan ekonomi masyarakat setelah gempa.
    Kegiatan tersebut dilaksanakan pada 23 September 2026 di Aula Bintang Wisata,
    Kecamatan Riung, Kabupaten Ngada, dan melibatkan Forum Konservasi Mbou Riung
    Ngada serta BKSDA NTT.
    """
]


def count_words(text):
    return len(text.split())


print("=" * 70)
print("TEST SUMMARY MERGER - INFORMATION PRESERVATION")
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

reduction = (
    (input_word_count - output_word_count)
    / input_word_count
) * 100

print("\n")
print("=" * 70)
print("INFORMASI")
print("=" * 70)

print(f"Jumlah summary input : {len(SUMMARY_INPUTS)}")
print(f"Total kata input     : {input_word_count}")
print(f"Total kata output    : {output_word_count}")
print(f"Pengurangan kata     : {reduction:.2f}%")

print("\n")
print("=" * 70)
print("INFORMASI PENTING YANG DIHARAPKAN")
print("=" * 70)

expected_information = [
    "23 September 2026",
    "Aula Bintang Wisata",
    "Kecamatan Riung",
    "Kabupaten Ngada",
    "Forum Konservasi Mbou Riung Ngada",
    "BKSDA NTT",
]

for information in expected_information:
    if information.lower() in merged_summary.lower():
        print(f"[ADA]     {information}")
    else:
        print(f"[HILANG]  {information}")

print("\n")
print("=" * 70)
print("TEST SELESAI")
print("=" * 70)