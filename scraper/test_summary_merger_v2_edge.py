from scraper.summarization.summary_merger_v2 import SummaryMergerV2


merger = SummaryMergerV2(
    similarity_threshold=0.40,
    containment_threshold=0.80
)


TEST_CASES = [
    {
        "name": "Kasus 1 - Informasi tambahan",
        "summaries": [
            """
            Pemerintah memberikan bantuan kepada petani.
            """,
            """
            Pemerintah memberikan bantuan kepada petani,
            tetapi bantuan tersebut belum diterima seluruh kelompok tani.
            """
        ]
    },

    {
        "name": "Kasus 2 - Informasi tambahan ekonomi",
        "summaries": [
            """
            Harga komoditas meningkat.
            """,
            """
            Harga komoditas meningkat, tetapi produksi petani menurun.
            """
        ]
    },

    {
        "name": "Kasus 3 - Informasi lokasi tambahan",
        "summaries": [
            """
            Aktivitas ekonomi masyarakat meningkat.
            """,
            """
            Aktivitas ekonomi masyarakat meningkat di Kabupaten Ngada
            setelah adanya peningkatan kunjungan wisatawan.
            """
        ]
    },

    {
        "name": "Kasus 4 - Informasi benar-benar berbeda",
        "summaries": [
            """
            Produksi pertanian mengalami peningkatan.
            """,
            """
            Jumlah kunjungan wisatawan mengalami penurunan.
            """
        ]
    }
]


print("=" * 70)
print("TEST SUMMARY MERGER V2 - EDGE CASE")
print("=" * 70)


for test_case in TEST_CASES:

    print("\n")
    print("=" * 70)
    print(test_case["name"])
    print("=" * 70)

    summaries = test_case["summaries"]

    print("\nINPUT:")

    for index, summary in enumerate(
        summaries,
        start=1
    ):
        print(f"\nSUMMARY {index}:")
        print(summary.strip())

    result = merger.merge(summaries)

    print("\nOUTPUT:")
    print(result)


print("\n")
print("=" * 70)
print("TEST SELESAI")
print("=" * 70)