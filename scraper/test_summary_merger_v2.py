from scraper.summarization.summary_merger_v2 import SummaryMergerV2


merger = SummaryMergerV2(
    similarity_threshold=0.40,
    containment_threshold=0.80
)


TEST_CASES = [
    {
        "name": "Kasus 1 - Kalimat sama persis",
        "summaries": [
            """
            Pemerintah daerah melakukan pelatihan kepada pelaku UMKM.
            Pemerintah berharap kegiatan tersebut meningkatkan kapasitas usaha.
            """,
            """
            Pemerintah daerah melakukan pelatihan kepada pelaku UMKM.
            """
        ]
    },

    {
        "name": "Kasus 2 - Kalimat pendek merupakan bagian dari kalimat panjang",
        "summaries": [
            """
            Kegiatan tersebut dilaksanakan di Kecamatan Riung,
            Kabupaten Ngada.
            """,
            """
            Kegiatan tersebut dilaksanakan pada 23 September 2026
            di Aula Bintang Wisata, Kecamatan Riung, Kabupaten Ngada.
            """
        ]
    },

    {
        "name": "Kasus 3 - Informasi berbeda",
        "summaries": [
            """
            Pemerintah daerah memberikan pelatihan kepada pelaku UMKM.
            """,
            """
            Kegiatan tersebut juga melibatkan kelompok tani hutan.
            """
        ]
    }
]


print("=" * 70)
print("TEST SUMMARY MERGER V2")
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