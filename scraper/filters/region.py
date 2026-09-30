import re


class NTTRegionFilter:

    NTT_KEYWORDS = [
        # Nama Provinsi & Julukan
        "ntt",
        "nusa tenggara timur",
        "flobamora",

        # Kota/Kabupaten (Lengkap dengan singkatan umum di media/berita)
        "kupang",
        "kota kupang",
        "kabupaten kupang",
        "timor tengah selatan", "tts",
        "timor tengah utara", "ttu",
        "belu",
        "malaka",
        "rote ndao",
        "sabu raijua",
        "sumba timur",
        "sumba tengah",
        "sumba barat",
        "sumba barat daya", "sbd",
        "manggarai",
        "manggarai barat", "mabar",
        "manggarai timur", "matim",
        "ngada",
        "nagekeo",
        "ende",
        "sikka",
        "flores timur", "flotim",
        "lembata",
        "alor",

        # Ibukota Kabupaten (Sering menjadi dateline/lokasi spesifik di berita)
        "oelamasi",     # Kab. Kupang
        "soe",          # TTS
        "kefamenanu",   # TTU
        "kefa",         # Singkatan Kefamenanu
        "atambua",      # Belu
        "betun",        # Malaka
        "ba'a", "baa",  # Rote Ndao
        "seba",         # Sabu Raijua
        "waingapu",     # Sumba Timur
        "waibakul",     # Sumba Tengah
        "waikabubak",   # Sumba Barat
        "tambolaka",    # Sumba Barat Daya
        "ruteng",       # Manggarai
        "labuan bajo",  # Manggarai Barat
        "borong",       # Manggarai Timur
        "bajawa",       # Ngada
        "mbay",         # Nagekeo
        "maumere",      # Sikka
        "larantuka",    # Flores Timur
        "lewoleba",     # Lembata
        "kalabahi",     # Alor

        # Pulau-pulau (Besar dan Kecil yang dikenal)
        "pulau timor", "timor",
        "pulau flores", "flores",
        "pulau sumba", "sumba",
        "pulau rote", "rote",
        "pulau sabu", "sabu",
        "pulau alor", "alor",
        "pulau lembata",
        "pulau komodo",
        "pulau padar",
        "pulau rinca",
        "pulau semau",
        "pulau pantar",
        "pulau adonara",
        "pulau solor",
        "pulau palue",
        "pulau babi",
        "pulau ndana",
        "pulau messah",
        "pulau kepa",

        # Kawasan Wisata, Landmark, & Desa Adat Ikonik
        "taman nasional komodo", "tnk",
        "kelimutu",
        "danau kelimutu",
        "wae rebo",
        "kampung bena", "desa bena",
        "kampung tarung",
        "nihiwatu",
        "pantai lasiana",
        "pantai nembrala", "nembrala",
        "fatumnasi",
        "gua batu cermin",
        "bukit wairinding",
        "air terjun tanggedu",
        "teluk gurita",
        "pos lintas batas negara", "plbn motaain", "plbn wini", "plbn motamasin",

        # Gunung Ikonik/Aktif (Sering masuk berita kebencanaan/geografis)
        "gunung mutis",
        "gunung lewotobi", "lewotobi laki-laki", "lewotobi perempuan",
        "gunung ile lewotolok", "ile lewotolok",
        "gunung inerie",
        "gunung egon",
        "gunung rokatenda",
        "gunung ile boleng"
    ]
    def is_ntt_related(self, text):
        if not text:
            return False

        normalized_text = text.lower()

        for keyword in self.NTT_KEYWORDS:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, normalized_text):
                return True

        return False