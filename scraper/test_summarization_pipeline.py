from scraper.summarization.long_article import LongArticleSummarizer
from scraper.summarization.summary_merger_v2 import SummaryMergerV2


ARTICLES = [
    {
        "name": "Sumba Barat Daya Dapat Program Pengembangan Pabrik Bioetanol dari Kementan RI",
        "text": """
Laporan Reporter POS-KUPANG.COM , Petrus Piter

POS-KUPANG.COM, TAMBOLAKA - Kabupaten Sumba Barat Daya , Provinsi Nusa Tenggara Timur  mendapat peluang pengembangan industri bioetanol melalui program berbasis komoditas tebu, singkong dan jagung dari Kementrian Pertanian (Kementan) RI.

Program dari Kementan RI tersebut dibahas dalam Rapat Koordinasi Percepatan Pengembangan Bioetanol yang dihadiri 44 kepala daerah se-Indonesia dari berbagai sentra produksi di Jakarta, Senin, 21 September 2026.

Menteri Pertanian RI Andi Amran Sulaiman mengatakan pengembangan bioetanol akan melibatkan pemerintah, BUMN, swasta dan masyarakat melalui pola kemitraan.

Masyarakat ditargetkan mendapat porsi kemitraan minimal 30 persen sehingga manfaat program dapat dirasakan secara langsung.

Pemerintah menyiapkan pengembangan lahan hingga 2 juta hektare sebagai bagian dari penguatan ketahanan dan kemandirian energi nasional.

Sementara itu,  Bupati Sumba Barat Daya , Ratu Ngadu Bonnu Wulla , S.T dalam pertemuan itu, menyatakan kesiapan daerah untuk mendukung program Kementerian Pertanian itu.

Melansir dari Rilis Kominfo Sumba Barat Daya yang diperoleh POS-KUPANG.COM pada Selasa 22 September 2026 disebutkan, selain rencana pengembangan pabrik bioetanol , Sumba Barat Daya juga mendapat dukungan awal berupa pengembangan jagung seluas 1.000 hektare dan bantuan lima unit traktor.

Program ini diharapkan dapat memperkuat sektor pertanian, meningkatkan produktivitas dan pendapatan petani, membuka lapangan kerja, serta mendorong tumbuhnya industri berbasis komoditas lokal di Kabupaten Sumba Barat Daya .

Karena itu, Bupati  Ratu Wulla meminta masyarakat untuk mensukseskan program tersebut demi meningkatan kesejahteraan hidupnya. (pet)
"""
    },{
        "name": "Arus Wisman Labuan Bajo Selisih Kedatangan dan Keberangkatan 873 Orang",
        "text": """
Laporan Reporter POS-KUPANG.COM , Tari Rahmaniar

POS-KUPANG.COM, LABUAN BAJO - Arus kunjungan wisatawan mancanegara (wisman) melalui Tempat Pemeriksaan Imigrasi (TPI) Udara Labuan Bajo menunjukkan adanya perubahan dalam periode 16 Agustus hingga 20 September 2026.

Berdasarkan data Kantor Imigrasi Kelas II TPI Labuan Bajo mencatat jumlah wisatawan yang meninggalkan Labuan Bajo lebih banyak dibandingkan yang datang.

Kepala Kantor Imigrasi Kelas II TPI Labuan Bajo, Charles Christian Mathaus , mengatakan selama periode tersebut tercatat 6.672 orang datang melalui TPI Udara Labuan Bajo, sementara 7.545 orang tercatat berangkat.

Dengan demikian, terdapat selisih sekitar 873 orang antara jumlah kedatangan dan keberangkatan.

“Kalau kita data, yang keluar memang lebih banyak daripada yang masuk,” ujat Charles, Rabu (23/9/2026).

Menurutnya, kondisi tersebut tidak terlepas dari sejumlah faktor, termasuk situasi bencana yang terjadi di wilayah Flores serta adanya sejumlah objek wisata yang ditutup sehingga memengaruhi aktivitas wisatawan selama berada di wilayah Manggarai.

Charles menilai dampak bencana terhadap pergerakan wisatawan tidak dapat diabaikan.

Namun, ia mengatakan perubahan tersebut belum menunjukkan penurunan yang sangat besar jika hanya dilihat dari selisih jumlah kedatangan dan keberangkatan.

“Kalau dibilang ada dampak, pastilah berdampak. Dampaknya itu kan tidak hanya dilihat dari sisi jumlah yang keluar masuk, tetapi juga dari banyaknya objek wisata yang mungkin tutup dan tidak bisa dikunjungi, baik yang di darat maupun di laut,” ujarnya.

Ia menjelaskan, wisatawan yang meninggalkan Labuan Bajo tidak serta-merta dapat dikaitkan seluruhnya dengan kekhawatiran terhadap bencana.

Sebagian wisatawan bisa saja memang telah menyelesaikan masa kunjungannya.

Karena itu, data perlintasan imigrasi perlu dilihat bersama dengan kondisi pariwisata di lapangan, termasuk akses terhadap destinasi wisata yang terdampak dan penutupan sejumlah objek wisata.

“Tidak bisa dibilang itu tidak ada dampaknya, pasti ada dampaknya. Tapi kalau bisa dibilang, tidak terlalu signifikan,” ungkap Charles.

Perubahan arus tersebut menjadi salah satu indikator yang menunjukkan bahwa kondisi destinasi wisata dan situasi kebencanaan di Flores turut memengaruhi mobilitas wisatawan di Labuan Bajo, meskipun besarnya dampak terhadap sektor pariwisata masih perlu dilihat dari indikator lainnya, seperti tingkat hunian hotel, lama tinggal wisatawan, kunjungan ke destinasi, serta aktivitas perjalanan wisata. (iar)
"""
    }

    # Artikel kedua, ketiga, dst. kita tambahkan setelah ini.
]


def main():
    print("=" * 80)
    print("INITIALIZING SUMMARIZATION PIPELINE")
    print("=" * 80)

    summarizer = LongArticleSummarizer(
        max_tokens=450,
        overlap_paragraphs=2
    )

    merger = SummaryMergerV2(
        similarity_threshold=0.40,
        containment_threshold=0.80
    )

    for article in ARTICLES:
        print("\n")
        print("=" * 80)
        print(f"ARTICLE: {article['name']}")
        print("=" * 80)

        text = article["text"].strip()

        print("\n[1] ARTICLE INFO")
        print(f"Characters : {len(text)}")
        print(f"Words     : {len(text.split())}")

        print("\n[2] CHUNKING + SUMMARIZATION")

        chunk_results = summarizer.summarize_chunks(text)

        print(f"\nTotal chunks: {len(chunk_results)}")

        chunk_summaries = []

        for result in chunk_results:
            print("\n" + "-" * 80)
            print(f"CHUNK {result['chunk_index']}")
            print(f"Tokens : {result['chunk_tokens']}")
            print(f"Summary: {result['summary']}")

            chunk_summaries.append(result["summary"])

        print("\n[3] SUMMARY MERGER V2")

        final_summary = merger.merge(chunk_summaries)

        print("\nFINAL SUMMARY:")
        print(final_summary)

        print("\n[4] SUMMARY STATISTICS")

        original_words = len(text.split())
        summary_words = len(final_summary.split())

        if original_words > 0:
            compression = (
                1 - summary_words / original_words
            ) * 100
        else:
            compression = 0

        print(f"Original words : {original_words}")
        print(f"Summary words  : {summary_words}")
        print(f"Compression     : {compression:.2f}%")

        print("\n" + "=" * 80)


if __name__ == "__main__":
    main()