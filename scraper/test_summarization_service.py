from scraper.summarization.service import SummarizationService


# ============================================================
# ARTIKEL UJI
# ============================================================

ARTICLE_TEXT = """
Pemerintah Provinsi Nusa Tenggara Timur (NTT) gelar rapat
koordinasi pengendalian Inflasi Daerah di Kabupaten Timor
Tengah Selatan, setelah sejak Agustus 2026 dilaporkan mengalami
deflasi.

Rapat koordinasi mendaraskan tema "Sinergi TPID dalam menjaga
keseimbangan supply-demand komoditi pangan pasca deflasi".

Kondisi inflasi di Kabupaten Timor Tengah Selatan secara tahunan
tercatat sebesar 1,53 persen year on year (yoy) dengan indeks
harga konsumen sebesar 109,86.

Sedangkan inflasi bulanan untuk Agustus 2026 mengalami deflasi
mendalam sebesar -1,26 persen dan inflasi year to date sebesar
0,84 persen.

Pemerintah daerah membahas kondisi harga dan pasokan komoditas
pangan serta langkah yang perlu dilakukan untuk menjaga
stabilitas harga dan daya beli masyarakat.
"""


# ============================================================
# TEST
# ============================================================

print("=" * 70)
print("TEST SUMMARIZATION SERVICE")
print("=" * 70)

print("\nMembuat SummarizationService...")

summarizer = SummarizationService()


print("\nService berhasil dibuat.")


# ============================================================
# GENERATE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("GENERATING SUMMARY")
print("=" * 70)

summary = summarizer.summarize(ARTICLE_TEXT)


# ============================================================
# HASIL
# ============================================================

print("\n" + "=" * 70)
print("HASIL SUMMARY")
print("=" * 70)

print(summary)

print("\n" + "=" * 70)
print("TEST SELESAI")
print("=" * 70)