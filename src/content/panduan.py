"""Guide pages (Panduan) — served at /panduan/<slug>/.

This is the long-form reference content that used to live in the app's
"Peringatan & Kaedah Pengiraan" modal. Each entry becomes a real page:

- ``SLUG``        URL segment, e.g. /panduan/ihtiyati/
- ``TITLE``       page heading and <title> prefix
- ``DESCRIPTION`` meta description (SEO)
- ``BODY``        Markdown
- ``ORDER``       position in the /panduan/ index
"""

PANDUAN = [
    {
        "SLUG": "penafian",
        "ORDER": 1,
        "TITLE": "Penafian Penting",
        "DESCRIPTION": (
            "Aplikasi ini adalah untuk panduan umum sahaja. Waktu solat boleh "
            "berbeza satu hingga dua minit daripada waktu rasmi pihak berkuasa."
        ),
        "BODY": """
**Aplikasi ini adalah untuk panduan umum sahaja.** Waktu solat yang dipaparkan
mungkin berbeza satu hingga dua minit daripada waktu rasmi yang diterbitkan
oleh pihak berkuasa.

> Untuk waktu yang lebih tepat dan sah secara rasmi, sila rujuk sumber rasmi
> berikut sebelum beramal.

- [e-Solat JAKIM](https://www.e-solat.gov.my) — www.e-solat.gov.my
- Majlis Agama Islam negeri masing-masing
- Taqwim Solat yang diterbitkan setiap tahun
""",
    },
    {
        "SLUG": "zon-dan-titik-rujukan",
        "ORDER": 2,
        "TITLE": "Zon Waktu & Titik Rujukan JAKIM",
        "DESCRIPTION": (
            "Bagaimana JAKIM membahagikan Malaysia kepada zon waktu solat, dan "
            "sebab aplikasi ini memaparkan dua lajur: barat dan timur."
        ),
        "BODY": """
Malaysia dibahagikan kepada **59 zon waktu solat** oleh JAKIM. Setiap zon
merangkumi beberapa daerah yang berbeza jarak dari garisan bujur.

Prinsip utama: JAKIM menggunakan **titik paling barat dalam setiap zon** sebagai
titik rujukan. Ini kerana titik barat menerima cahaya fajar paling lewat dan
matahari terbenam paling awal — bermakna waktu Subuh paling lewat dan waktu
Maghrib paling awal bagi seluruh zon. Ini memastikan seluruh penduduk zon
tersebut **selamat untuk berimsak** secara serentak.

Sebab itulah aplikasi ini memaparkan **dua lajur**:

- **Barat (◀)** — waktu rasmi zon, berdasarkan sempadan barat. Inilah yang
  JAKIM gunakan.
- **Timur (▶)** — waktu di sempadan timur zon. Subuh lebih awal, Maghrib lebih
  lewat berbanding kolum Barat.

Perbezaan boleh mencecah **5–15 minit** bagi zon yang luas seperti di Sabah,
Sarawak dan Pahang dalaman.
""",
    },
    {
        "SLUG": "ihtiyati",
        "ORDER": 3,
        "TITLE": "Ihtiyati — Margin Berjaga-jaga",
        "DESCRIPTION": (
            "Nilai ihtiyati yang ditambah pada setiap waktu solat dalam aplikasi "
            "ini, dan sebab ia diperlukan."
        ),
        "BODY": """
**Ihtiyati** (الاحتياط) bermaksud langkah berjaga-jaga. Dalam pengiraan waktu
solat, nilai astronomik tulen ditambah sedikit minit tambahan sebelum dibulatkan
ke minit penuh. Tujuannya untuk memastikan setiap waktu sudah pasti masuk
sebelum diisytiharkan.

| Waktu Solat | Kaedah | Sebab | Ihtiyati |
|-------------|--------|-------|----------|
| **Imsak** | Subuh − 10 min | Sempadan akhir makan sahur | −10 min |
| **Subuh** | raw + ihtiyati, bulat ke bawah | Sudut 18° sudah lebih konservatif | +2 min |
| **Syuruk** | raw, bulat ke bawah | Tamat waktu solat Subuh | +0 min |
| **Zohor** | raw + ihtiyati, bulat ke bawah | Pastikan matahari sudah jelas condong | +2 min |
| **Asar** | raw + ihtiyati, bulat ke bawah | Sempadan bayang-bayang lebih selamat | +3 min |
| **Maghrib** | raw + ihtiyati, bulat ke bawah | Pastikan matahari sudah terbenam penuh | +1 min |
| **Isyak** | raw + ihtiyati, bulat ke bawah | Syafaq benar-benar hilang | +2 min |

Nilai ihtiyati ini disahkan melalui perbandingan dengan data JAKIM untuk zon
JHR02 dan WLY01 pada 18 Mac 2026, menggunakan sudut Subuh **18°** yang berkuat
kuasa sejak 2019 berikutan keputusan MKI Ke-116.
""",
    },
    {
        "SLUG": "kaedah-pengiraan",
        "ORDER": 4,
        "TITLE": "Kaedah Pengiraan Astronomik",
        "DESCRIPTION": (
            "Formula dan sudut matahari yang digunakan untuk mengira waktu solat "
            "mengikut kaedah JAKIM dan formula Rinto Anugraha."
        ),
        "BODY": """
Aplikasi ini menggunakan formula dari buku **Rinto Anugraha — "Mekanika Benda
Langit"** (Universiti Gadjah Mada, Indonesia), yang menjadi rujukan utama
pengiraan waktu solat di Malaysia dan Indonesia.

Langkah-langkah pengiraan:

- **Julian Day (JD)** — tarikh ditukar kepada nombor Julian untuk memudahkan
  pengiraan astronomi.
- **Deklinasi Matahari (δ)** — sudut antara garisan khatulistiwa Bumi dan
  kedudukan matahari. Berubah sepanjang tahun (±23.4°). Formula siri
  trigonometri tiga sebutan digunakan.
- **Persamaan Masa (ET)** — perbezaan antara waktu matahari sebenar dan jam
  biasa, disebabkan orbit Bumi berbentuk elips dan paksi condong. Boleh ±16
  minit. Formula tujuh sebutan digunakan.
- **Waktu Transit (Zohor)** — matahari di puncak meridian tempatan:
  `TT = 12 + zon_masa − (bujur÷15) − (ET÷60)`
- **Sudut Waktu (Hour Angle)** — sudut matahari dari meridian pada ketinggian
  tertentu, dikira dengan formula:
  `cos H = (sin alt − sin lat · sin δ) / (cos lat · cos δ)`

Ketinggian matahari yang digunakan:

```
Subuh / Fajr    -> -18° (di bawah ufuk) - keputusan MKI Ke-116, Nov 2019
Syuruk / Maghrib -> -0.833° - 0.0347√h  (h = ketinggian tempat, meter)
Asar (Syafii)   -> arctan(1 / (1 + tan|lat-δ|))
Isyak           -> -18° (di bawah ufuk) - standard JAKIM
```

Fajr/Isyak menggunakan ketinggian negatif kerana matahari masih di bawah ufuk.
Kedua-duanya ialah **sudut senja astronomi** yang menentukan gelap-terang langit.
Sudut Subuh 18° adalah **lebih lewat** daripada 20° (lebih cerah, lebih selamat
untuk imsak), menghasilkan waktu Subuh ~8 minit lebih lewat.
""",
    },
    {
        "SLUG": "isu-teknikal",
        "ORDER": 5,
        "TITLE": "Isu & Penemuan Teknikal",
        "DESCRIPTION": (
            "Nota teknikal semasa membangunkan aplikasi ini: ralat formula, "
            "perubahan sudut Subuh, ihtiyati, mazhab Asar dan pembetulan "
            "ketinggian tempat."
        ),
        "BODY": """
Semasa membangunkan aplikasi ini, beberapa isu menarik ditemui:

- **Ralat formula asal:** Formula deklinasi Anugraha menggunakan T dalam
  radian, di mana argumen `sinD(57.297 × T)` menukar radian ke darjah secara
  tersirat. Menggunakan T dalam darjah secara salah menghasilkan Subuh 12–15
  minit terlalu awal.
- **Sudut Subuh 18°, bukan 20°:** Pada November 2019, Muzakarah MKI Ke-116
  memutuskan sudut Subuh Malaysia bertukar dari 20° kepada **18°** berikutan
  kajian setahun oleh JAKIM, UM, UniSZA dan UiTM. Perubahan ini menambah ~8
  minit kepada waktu Subuh. Perbezaan tepat 8 minit antara dua sudut ini
  mengesahkan penemuan tersebut secara matematik. Rujukan:
  [Bayan Linnas Khas, Jabatan Mufti WP (6 Dis 2019)](https://muftiwp.gov.my/ms/artikel/bayan-linnas/3858-).
- **Ihtiyati Subuh hanya +2 minit:** Dengan sudut 18° yang sudah lebih
  selamat/lewat, ihtiyati yang diperlukan hanyalah 2 minit (bukan 10 minit
  seperti jika menggunakan 20°). Kesimpulan asal +10 minit adalah gabungan
  ralat sudut + ihtiyati yang tersalah dikira sebagai ihtiyati semata-mata.
- **Koordinat zon bukan titik tengah:** Menggunakan koordinat tengah bandar
  (seperti Johor Bahru) memberi waktu yang berbeza daripada JAKIM. Titik
  rujukan JAKIM ialah sempadan barat zon, bukan pusat penduduk.
- **Asar berbeza mazhab:** Mazhab Syafii (digunakan di Malaysia) mengira Asar
  apabila bayang-bayang sesuatu objek sama panjang dengan objek _ditambah_
  bayang-bayang tengah hari. Mazhab Hanafi menggunakan dua kali panjang — ini
  boleh menjadikan Asar 30–60 minit lebih lewat.
- **Pembetulan ketinggian tempat:** Kawasan tinggi seperti Cameron Highlands
  (±1500m) dan Gunung Kinabalu (±3000m) mempunyai Syuruk lebih awal dan
  Maghrib lebih lewat kerana ufuk efektif lebih rendah. Formula: tambah
  `0.0347√h` darjah kepada sudut ufuk.
""",
    },
    {
        "SLUG": "tarikh-hijri",
        "ORDER": 6,
        "TITLE": "Tarikh Hijri",
        "DESCRIPTION": (
            "Kenapa tarikh Hijri dalam aplikasi ini boleh berbeza 1–2 hari "
            "daripada takwim rasmi Malaysia."
        ),
        "BODY": """
Tarikh Hijri dipaparkan menggunakan **algoritma tabular** berdasarkan Julian
Day, yang menganggap bulan bermula secara tetap 29.5 hari. Kaedah ini boleh
berbeza **1–2 hari** daripada takwim rukyah (cerapan anak bulan) yang digunakan
secara rasmi di Malaysia.

Untuk tarikh Hijri rasmi Malaysia, sila rujuk [JAKIM](https://www.islam.gov.my)
atau Majlis Agama negeri.
""",
    },
    {
        "SLUG": "kakas-pembangunan",
        "ORDER": 7,
        "TITLE": "Skrip Pembangunan (Dev Tools)",
        "DESCRIPTION": (
            "Skrip interaktif yang digunakan untuk mengesahkan pengiraan waktu "
            "solat berbanding data JAKIM."
        ),
        "BODY": """
Semasa membangunkan aplikasi ini, beberapa skrip interaktif digunakan untuk
mengesahkan pengiraan berbanding data JAKIM:

- **Tab 1 — Perbandingan JAKIM:** Masukkan waktu JAKIM untuk mana-mana zon dan
  tarikh, bandingkan dengan hasil pengiraan tempatan secara langsung.
- **Tab 2 — Probe Koordinat:** Imbas julat latitud/longitud untuk mencari titik
  yang menghasilkan waktu sasaran — cara titik rujukan barat setiap zon
  disahkan.
- **Tab 3 — Probe Ihtiyati:** Cari kombinasi ihtiyati yang paling hampir dengan
  data JAKIM secara automatik.
- **Tab 4 — Fetch JAKIM API:** Ambil data langsung dari API e-Solat JAKIM untuk
  dijadikan rujukan. Termasuk skrip Node.js untuk elak sekatan CORS.
- **Tab 5 — Kod Sumber:** Semua skrip Node.js asal yang dijalankan dalam
  terminal semasa sesi pembangunan, dengan ulasan terperinci.

[Buka Dev Tools](/dev-tools)
""",
    },
]
