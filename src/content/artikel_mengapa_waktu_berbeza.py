"""Article: Mengapa Waktu Solat Berbeza Antara Daerah.

Copy this file to add a new article, then register it in content/__init__.py.
"""

ARTICLE = {
    "SLUG": "mengapa-waktu-solat-berbeza-antara-daerah",
    "TITLE": "Mengapa Waktu Solat Berbeza Antara Daerah",
    "DESCRIPTION": (
        "Sebab waktu solat berbeza antara daerah walaupun dalam zon masa yang "
        "sama, dan bagaimana aplikasi ini mengiranya mengikut kaedah JAKIM."
    ),
    "DATE": "2026-10-18",
    "BODY": """
Waktu solat ditentukan oleh kedudukan matahari, bukan oleh jam dinding. Oleh
sebab itu dua tempat dalam zon masa yang sama boleh mempunyai waktu solat yang
berbeza beberapa minit.

## Kedudukan matahari menentukan waktu

Setiap waktu solat berkait dengan sudut matahari pada sesuatu lokasi:

| Waktu | Ditentukan oleh |
|-------|-----------------|
| Subuh | Matahari 18° di bawah ufuk |
| Syuruk | Matahari terbit |
| Zohor | Matahari melintasi meridian |
| Asar | Panjang bayang melebihi panjang objek |
| Maghrib | Matahari terbenam |
| Isyak | Matahari 18° di bawah ufuk |

Semakin jauh ke timur sesuatu lokasi dalam zon masa yang sama, semakin awal
matahari terbit dan terbenam.

## Kaedah pengiraan dalam aplikasi ini

Aplikasi ini menggunakan kaedah JAKIM berdasarkan formula Rinto Anugraha
("Mekanika Benda Langit") dengan keputusan MKI Ke-116 (November 2019):

- Subuh dan Isyak: sudut 18°
- Ihtiyati: Subuh +2 minit, Zohor +2 minit, Asar +3 minit, Maghrib +1 minit,
  Isyak +2 minit

Ihtiyati ialah margin keselamatan supaya waktu yang dipaparkan tidak mendahului
waktu sebenar.
""",
}
