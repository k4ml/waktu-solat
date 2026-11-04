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
    {
        "SLUG": "nota-pembangunan-kiblat",
        "ORDER": 8,
        "TITLE": "Nota Pembangunan — Pencari Arah Kiblat",
        "DESCRIPTION": (
            "Nota teknikal pelaksanaan pencari arah kiblat: formula bearing "
            "bulatan besar, geolokasi, kompas peranti dan perangkap iOS/Android."
        ),
        "BODY": """
Halaman [Pencari Arah Kiblat](/kiblat/) berbeza daripada kalkulator waktu solat:
ia **tidak memerlukan rangkaian sama sekali** selepas dimuatkan. Arah kiblat
ialah fungsi tulen bagi koordinat pengguna, jadi keseluruhan pengiraan berlaku
dalam pelayar. Nota ini merekodkan cara ia dibina, keputusan reka bentuk, dan
perangkap yang ditemui semasa menguji pada iOS dan Android.

## 1. Bearing Kiblat — Formula Bulatan Besar

Kiblat ialah arah **bearing awal** (*initial bearing*) dari satu titik di
permukaan sfera ke Kaabah (21.4225°N, 39.8262°E). Ia dikira dengan formula
bearing bulatan besar:

```
θ = atan2( sin Δλ · cos φ₂ ,
           cos φ₁ · sin φ₂ − sin φ₁ · cos φ₂ · cos Δλ )
```

di mana `φ₁, λ₁` ialah latitud/longitud pengguna, `φ₂, λ₂` koordinat Kaabah, dan
`Δλ = λ₂ − λ₁`. Hasil `atan2` berada dalam julat −π…π, jadi ia perlu dinormalkan
ke 0–360°.

Pelaksanaan sebenar (JavaScript dalam halaman, dan salinan Python dalam
`src/kiblat.py` untuk semakan):

```js
function qiblaBearing(lat, lng) {
  const kaabaLat = 21.4225 * Math.PI / 180;
  const kaabaLng = 39.8262 * Math.PI / 180;
  lat *= Math.PI / 180; lng *= Math.PI / 180;
  const dLng = kaabaLng - lng;
  const y = Math.sin(dLng) * Math.cos(kaabaLat);
  const x = Math.cos(lat) * Math.sin(kaabaLat)
          - Math.sin(lat) * Math.cos(kaabaLat) * Math.cos(dLng);
  return (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
}
```

**Perhatian:** ini bearing *permulaan*, bukan bearing sepanjang laluan rhumb.
Untuk jarak sejauh Malaysia–Makkah (6,000–7,000 km) perbezaannya kecil, tetapi
istilah yang betul tetap penting jika kod ini digunakan semula untuk jarak jauh
atau untuk laluan yang melintasi kutub.

### Bukan "arah matahari terbenam"

Ramai menganggap kiblat dari Malaysia ialah "arah barat". Ia sebenarnya
**barat-barat laut (WNW)**. Bearing 292.5° bermaksud 22.5° ke utara dari barat
tulen. Menghadap tepat ke barat (270°) akan tersasar lebih 20° — cukup untuk
membawa saf jauh dari arah Kaabah pada jarak beberapa meter.

Nilai rujukan yang disahkan dengan fungsi di atas:

| Lokasi | Latitud | Longitud | Bearing kiblat |
|--------|---------|----------|----------------|
| Kuala Lumpur | 3.1390 | 101.6869 | 292.5° |
| Johor Bahru | 1.4927 | 103.7414 | 293.0° |
| George Town | 5.4141 | 100.3288 | 291.6° |
| Ipoh | 4.5975 | 101.0901 | 291.9° |
| Kuantan | 3.8077 | 103.3260 | 292.0° |
| Kota Kinabalu | 5.9804 | 116.0735 | 290.6° |
| Kuching | 1.5533 | 110.3592 | 292.1° |
| Kota Bharu | 6.1254 | 102.2381 | 291.0° |

## 2. Geolokasi

Lokasi diambil melalui `navigator.geolocation.getCurrentPosition()` dengan
`enableHighAccuracy: true`, `timeout: 10000`, dan `maximumAge: 600000` (10
minit). Pilihan `maximumAge` membenarkan kedudukan terakhir yang masih segar
dipulangkan serta-merta, mengurangkan masa menunggu.

Kod ralat dipetakan kepada mesej yang boleh difahami:

| `err.code` | Maksud | Tindakan dalam UI |
|------------|--------|-------------------|
| 1 | Kebenaran ditolak | Minta benarkan akses atau guna koordinat manual |
| 2 | Kedudukan tidak tersedia | Cadang masukkan koordinat |
| 3 | Masa tamat | Cadang cuba semula |

**Cache luar talian:** lokasi terakhir yang sah disimpan dalam `localStorage`
(kunci `kiblat:location`) supaya arah kiblat masih boleh dipaparkan tanpa
rangkaian pada lawatan seterusnya. Lokasi contoh Kuala Lumpur **tidak** disimpan
— jika tidak, UI akan mendakwa pengguna berada di KL sedangkan itu hanya nilai
lalai.

**Fallback tanpa GPS:** pemilih bandar (8 bandar Malaysia) dan medan latitud /
longitud manual. Ini penting untuk desktop, di mana pengguna sering menolak
permintaan lokasi.

**Privasi:** koordinat tidak pernah dihantar ke pelayan. Ia hanya digunakan
dalam fungsi `qiblaBearing()` pada peranti.

## 3. Kompas Peranti

Ini bahagian yang paling banyak perangkapnya kerana setiap pelayar mendedahkan
data yang berbeza.

### iOS Safari

- Gunakan `DeviceOrientationEvent.webkitCompassHeading` — nilai 0–360° mengikut
  arah jam dari utara, sudah dikompensasi untuk orientasi peranti.
- `DeviceOrientationEvent.requestPermission()` **wajib** dipanggil dari gerak
  isyarat pengguna (ketikan butang). Ia tidak boleh dipanggil secara automatik
  semasa muat halaman.
- `webkitCompassAccuracy` memberi ketepatan dalam darjah; nilai negatif bermaksud
  tidak sah. Jika melebihi 15°, UI memaparkan gesaan kalibrasi angka 8.

### Android Chrome

- Utamakan peristiwa `deviceorientationabsolute`, yang membawa `absolute: true`
  dan `alpha` relatif kepada utara sebenar.
- `alpha` adalah **lawan arah jam** dari utara, manakala heading kompas adalah
  mengikut arah jam: `heading = 360 − alpha`.
- Nilai `alpha` adalah relatif kepada rangka peranti, bukan skrin. Apabila skrin
  berputar (landskap), offset orientasi skrin perlu ditambah:

```js
const screenAngle = screen.orientation
  ? screen.orientation.angle
  : (window.orientation || 0);

heading = ((360 - alpha) + screenAngle + 360) % 360;
```

- Jika hanya `deviceorientation` tersedia (bukan mutlak), bacaan itu relatif dan
  boleh terpesong. Halaman ini tetap menerimanya sebagai sandaran, tetapi
  `deviceorientationabsolute` sentiasa diutamakan kerana ia didaftarkan dahulu.

### Memutar carta, bukan jarum

Dua cara untuk memaparkan kompas:

1. Kekalkan carta (N/E/S/W) pegun dan putar jarum kiblat mengikut
   `bearing − heading`.
2. Putar **seluruh carta** mengikut `−heading`, dan letakkan jarum kiblat pada
   `bearing` dalam ruang carta.

Halaman ini menggunakan pendekatan kedua. Kelebihannya: label N/E/S/W sentiasa
menghadap utara sebenar, jadi pengguna boleh membaca arah cardinal secara
terus, dan jarum kiblat hanya perlu dikemas kini apabila bearing berubah.
Penanda `▲` di bahagian atas skrin menunjukkan arah bahagian atas peranti;
apabila jarum KIBLAT bertemu `▲`, pengguna sedang menghadap kiblat.

## 4. Perangkap yang Ditemui

- **`alpha` relatif vs mutlak.** Tanpa `deviceorientationabsolute`, bacaan
  Android bergantung pada orientasi awal dan boleh tersasar berpuluh darjah.
  Sentiasa utamakan peristiwa mutlak.
- **Kebenaran iOS.** Kedua-dua geolokasi dan orientasi memerlukan HTTPS (atau
  `localhost`) dan gerak isyarat pengguna. Tiada cara untuk bertanya secara
  senyap semasa muat halaman.
- **Magnetometer dalam bangunan.** Bacaan kompas sangat lemah berhampiran logam
  dan struktur bangunan. Gesaan kalibrasi angka 8 dipaparkan berdasarkan
  `webkitCompassAccuracy`, tetapi ketidaktepatan Android tidak didedahkan secara
  langsung — sebab itu UI mengesyorkan kalibrasi secara manual.
- **Tiada sensor.** Sesetengah desktop dan peranti lama tiada API orientasi.
  Selepas 1.5 saat tanpa peristiwa, UI beralih kepada mod statik: carta
  berorientasikan utara dengan bacaan darjah, dan arahan "putar sehingga N
  menghadap utara sebenar".
- **Deklinasi magnetik.** Kompas mengukur utara magnetik, bukan utara sebenar.
  Di Malaysia perbezaannya kecil (±0°–1°), jadi ia diabaikan. Di latitud tinggi
  ia tidak boleh diabaikan.
- **Konteks selamat.** Membuka halaman melalui `http://` daripada peranti lain
  dalam LAN akan menyekat kedua-dua API. `localhost` dikecualikan.

## 5. Struktur Fail

| Fail | Peranan |
|------|---------|
| `src/kiblat.py` | Halaman penuh (`PAGE`), `qibla_bearing()` Python, `CITY_PRESETS`, `render_kiblat()` |
| `src/entry.py` | Laluan `if path == "/kiblat"` dan kaedah `serve_kiblat()`; entri `sitemap.xml` |
| `src/template.py` | Pautan menu `Kiblat` pada halaman waktu solat |
| `src/pages.py` | Pautan menu `Kiblat` pada halaman kandungan (`_main_menu`) |
| `README.md` | Baris `/kiblat/` dalam jadual struktur URL |

Halaman menggunakan penanda templat tersendiri (bukan `str.format`) supaya
JavaScript dalaman boleh mengekalkan kurungan kurawal tanpa perlu di-escape —
konvensyen yang sama seperti `src/template.py` dan `src/pages.py`.
`render_kiblat()` akan meningkatkan ralat jika ada penanda yang tidak diganti,
supaya salah taip tidak lulus secara senyap.

Bearing dikira dalam dua tempat: JavaScript (paparan langsung) dan Python
(`qibla_bearing()`). Salinan Python digunakan untuk semakan dan boleh dijalankan
dari terminal:

```bash
python3 -c "import sys; sys.path.insert(0,'src'); import kiblat; \\
print(round(kiblat.qibla_bearing(3.1390, 101.6869), 2))"
```

Keluaran dijangka `292.54`.

## 6. Pengesahan

Semasa pembangunan, halaman disahkan melalui:

- **Semakan sintaks JS:** skrip dalaman diekstrak dan diuji dengan `node --check`.
- **Semakan penanda:** `render_kiblat()` dipanggil secara langsung untuk
  memastikan tiada penanda yang tertinggal.
- **Semakan laluan:** pelayan pembangunan dijalankan dan `curl` memastikan
  `/kiblat/` memulangkan 200 serta `/kiblat` mengalih ke `/kiblat/` (301).
- **Semakan bearing:** nilai bagi 8 bandar dibandingkan secara manual dengan
  jangkaan geometri (semua dalam julat 290°–293° untuk Malaysia).

Yang **tidak** dapat diuji secara automatik ialah perkakasan: bacaan kompas
sebenar hanya boleh disahkan pada peranti fizikal. Ujian pada iOS dan Android
sebenar masih diperlukan sebelum menganggap bahagian kompas itu muktamad.
""",
    },
]
