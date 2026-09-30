import re


class EconomicActivityFilter:

    ECONOMIC_KEYWORDS = [
        # KBLI A: Pertanian, Kehutanan, Perikanan, dan Peternakan
        "petani", "pertanian", "perkebunan", "perikanan", "nelayan",
        "panen", "panen raya", "produksi", "gagal panen", "puso", 
        "hasil panen", "komoditas", "pupuk", "subsidi pupuk", "benih", 
        "bibit", "hama", "cuaca buruk", "kemarau", "kekeringan",
        "peternakan", "ternak", "sapi", "babi", "unggas", "pakan",
        "rumput laut", "jagung", "kopi", "kemiri", "kakao", "mete",

        # KBLI G: Perdagangan, Harga, dan Konsumsi
        "perdagangan", "pedagang", "pasar", "pasar tradisional", "pasar modern",
        "harga", "kenaikan harga", "penurunan harga", "inflasi", "deflasi",
        "distribusi", "pasokan", "permintaan", "stok", "ketersediaan",
        "sembako", "kebutuhan pokok", "bahan pokok", "bapok", "beras", 
        "minyak goreng", "gula", "cabai", "bawang", "daging",
        "daya beli", "operasi pasar", "eceran", "grosir", "stabilitas harga",

        # KBLI C: Industri Pengolahan & UMKM
        "industri", "pabrik", "usaha", "produksi", "pengolahan", 
        "manufaktur", "umkm", "usaha mikro", "usaha kecil", "usaha menengah",
        "kerajinan", "tenun", "ikat", "kreatif", "ekonomi kreatif", 
        "koperasi", "kapasitas produksi", "bahan baku",

        # KBLI I & R: Pariwisata, Akomodasi, dan Makanan Minuman
        "pariwisata", "wisatawan", "turis", "kunjungan wisatawan", "wisata", 
        "destinasi", "hotel", "penginapan", "restoran", "rumah makan",
        "kafe", "okupansi", "tingkat hunian", "event", "festival",

        # KBLI H: Transportasi dan Pergudangan
        "transportasi", "angkutan", "penerbangan", "pelayaran", 
        "penumpang", "pelabuhan", "bandara", "logistik", "rantai pasok", 
        "kargo", "distribusi barang", "tarif", "tiket", "tol laut", 
        "pelayaran perintis", "cuaca ekstrem", "gelombang tinggi",

        # KBLI F: Konstruksi, Real Estat & Infrastruktur
        "konstruksi", "pembangunan", "proyek", "jalan", "jembatan", 
        "infrastruktur", "bendungan", "pengadaan", "tender", 
        "material bangunan", "semen", "properti", "perumahan",

        # KBLI K: Keuangan dan Asuransi
        "bank", "kredit", "pinjaman", "investasi", "perbankan", 
        "kredit macet", "npl", "suku bunga", "kur", "kredit usaha rakyat", 
        "pembiayaan", "modal", "inklusi keuangan", "literasi keuangan", 
        "pma", "penanaman modal asing", "pmdn", "modal dalam negeri",

        # KBLI B, D, E: Pertambangan, Energi, dan Utilitas
        "tambang", "pertambangan", "galian c", "listrik", "elektrifikasi", 
        "energi", "bbm", "bahan bakar minyak", "air bersih", "pdam",

        # Ketenagakerjaan
        "tenaga kerja", "pekerja", "buruh", "lapangan kerja", 
        "pengangguran", "phk", "pemutusan hubungan kerja", "upah", 
        "ump", "umk", "upah minimum", "angkatan kerja", "serapan kerja",

        # Ekonomi Makro, Fiskal & Statistik Pemerintahan
        "pdrb", "pertumbuhan ekonomi", "ekonomi", "pendapatan", 
        "pajak", "retribusi", "pendapatan asli daerah", "pad", 
        "ekspor", "impor", "neraca perdagangan", "kemiskinan", 
        "ketimpangan", "gini ratio", "indeks pembangunan manusia", "ipm", 
        "apbd", "apbn", "dana desa", "subsidi", "resesi"
    ]

    def get_matched_keywords(self, text):
        if not text:
            return []

        normalized_text = text.lower()

        matched = []

        for keyword in self.ECONOMIC_KEYWORDS:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, normalized_text):
                matched.append(keyword)

        return matched

    def is_economic_activity(self, text):
        return len(self.get_matched_keywords(text)) > 0
    