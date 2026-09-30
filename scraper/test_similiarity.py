from scraper.summarization.summary_merger import SummaryMerger

merger = SummaryMerger(similarity_threshold=0.80)

sentence_a = (
    "Kegiatan tersebut dilaksanakan di Kecamatan Riung, "
    "Kabupaten Ngada."
)

sentence_b = (
    "Kegiatan tersebut dilaksanakan pada 23 September 2026 "
    "di Aula Bintang Wisata, Kecamatan Riung, Kabupaten Ngada."
)

similarity = merger.calculate_similarity(
    sentence_a,
    sentence_b
)

print("=" * 70)
print("TEST SIMILARITY")
print("=" * 70)

print("\nSentence A:")
print(sentence_a)

print("\nSentence B:")
print(sentence_b)

print("\nSimilarity:")
print(f"{similarity:.4f}")

print("\nThreshold:")
print(merger.similarity_threshold)

if similarity >= merger.similarity_threshold:
    print("\nHASIL: REDUNDANT")
else:
    print("\nHASIL: TIDAK REDUNDANT")