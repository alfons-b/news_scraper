from scraper.summarization.long_article import LongArticleSummarizer


ARTICLE_TEXT = """
Laporan Reporter POS-KUPANG.COM , Charles Abar

POS-KUPANG.COM, BAJAWA - Project In Flores berkolaborasi dengan Forum Konservasi Mbou Riung Ngada memberikan pelatihan kepada Kelompok Tani Hutan (KTH), pelaku wisata, dan pelaku UMKM di Kecamatan Riung, Kabupaten Ngada, Nusa Tenggara Timur (NTT).

Pelatihan tersebut menjadi bagian dari upaya mendorong pemulihan ekonomi masyarakat lokal setelah gempa Flores yang mengguncang wilayah tersebut pada Minggu (15/8/2026).

Kegiatan ini merupakan kolaborasi antara Forum Konservasi Mbou Riung Ngada, Projek In Flores, dan Balai Konservasi Sumber Daya Alam (BKSDA) NTT.

Pelatihan tidak hanya menyasar kelompok tani hutan, tetapi juga melibatkan pelaku wisata dan UMKM yang menjadi bagian dari ekosistem pariwisata di Kecamatan Riung.

Projek In Flores yang memiliki fokus pada konservasi Mbou Riung dan spesies lainnya juga menggandeng Lembaga Nusa Bunga Mandiri untuk memberikan pendampingan, mulai dari pengembangan kapasitas hingga pemasaran dan pengelolaan ekosistem wisata berbasis masyarakat lokal di kawasan wisata Riung.

Ketua Forum Konservasi Mbou Riung, Dr. Nicolaus Noywuli, saat mengunjungi peserta di Aula Bintang Wisata Riung, Rabu (23/9), mengatakan pendampingan dan pelatihan tersebut merupakan salah satu upaya untuk mendorong kebangkitan masyarakat lokal, khususnya pelaku wisata dan UMKM.

Menurut dia, Projek In Flores yang selama ini memberikan perhatian terhadap pengembangan ekosistem konservasi Mbou Riung terus mendorong masyarakat agar bangkit dan menjalankan perannya masing-masing sehingga aktivitas ekonomi masyarakat dapat kembali tumbuh.

Ia juga meminta para peserta memanfaatkan kesempatan mengikuti pelatihan tersebut dengan baik sehingga ke depan kelompok tani hutan, pelaku wisata, dan pelaku UMKM dapat berkembang secara mandiri.

“Kita memanfaatkan pendampingan dan pelatihan ini. Betul-betul kita manfaatkan mulai dari proses, input output, agar ini bisa memberikan kita keterampilan memadai dalam mengelola ekosistem pariwisata dan memberi dampak ekonomis bagi masyarakat,” ujar Dr. Nicolaus.

Ia menjelaskan, Projek In Flores memiliki batas waktu pendampingan hingga 2028. Karena itu, masyarakat diharapkan mampu memanfaatkan masa pendampingan tersebut untuk membangun kapasitas dan mengembangkan usaha secara mandiri.

“Projek ini akan sampai 2028, setelah itu kita harus bisa mengembangkan diri sendiri,” katanya.

Ia menekankan, kemandirian tersebut harus mulai dipersiapkan sejak sekarang, termasuk dalam pengembangan bisnis dan pemasaran produk maupun jasa yang dikelola masyarakat.

“Tahun 2029 kita harus bisa, kita harus punya modal, untuk bisa berjalan secara mandiri,” ujarnya.
"""


print("=" * 70)
print("TEST LONG ARTICLE SUMMARIZER")
print("=" * 70)


# ============================================================
# 1. INITIALIZE
# ============================================================

summarizer = LongArticleSummarizer(
    max_tokens=450,
    overlap_paragraphs=2
)


# ============================================================
# 2. PROCESS ARTICLE
# ============================================================

results = summarizer.summarize_chunks(
    ARTICLE_TEXT
)


# ============================================================
# 3. DISPLAY RESULT
# ============================================================

print("\n")
print("=" * 70)
print("HASIL SUMMARIZATION PER CHUNK")
print("=" * 70)


for result in results:

    print("\n" + "-" * 70)

    print(
        f"CHUNK {result['chunk_index']}"
    )

    print(
        f"Token: {result['chunk_tokens']}"
    )

    print("\nSUMMARY:")

    print(
        result["summary"]
    )


# ============================================================
# 4. SUMMARY INFORMATION
# ============================================================

print("\n")
print("=" * 70)
print("INFORMASI")
print("=" * 70)

print(
    f"Jumlah chunk: {len(results)}"
)

for result in results:

    summary = result["summary"]

    print(
        f"Chunk {result['chunk_index']}: "
        f"{len(summary.split())} kata summary"
    )


print("\n")
print("=" * 70)
print("TEST SELESAI")
print("=" * 70)