# Christina Natalia Siregar — Portofolio

Website statis untuk GitHub Pages, dengan desain burgundy dan ivory, tampilan responsif, filter bukti kerja, galeri gambar, dan unduhan PDF terpisah.

## Berkas utama

- `index.html`: profil, pengalaman, dokumentasi, keahlian, pendidikan, dan kontak.
- `assets/style.css`: desain desktop, ponsel, dan aturan cetak.
- `assets/app.js`: navigasi ponsel, filter karya, dan dialog pembesaran gambar.
- `CV-Christina-Natalia-Siregar.pdf`: CV asli yang tersedia untuk diunduh.
- `Portofolio-Christina-Natalia-Siregar.pdf`: portofolio A4, 5 halaman, siap dicetak.

Seluruh gambar pada desain baru berasal dari dokumentasi yang sudah ditampilkan pada website sebelumnya, termasuk penyamaran informasi pada bukti kerja. Tidak ada layanan pihak ketiga, font CDN, atau build framework yang diperlukan.

## Menjalankan secara lokal

Dari direktori repositori:

```bash
python3 -m http.server 8000
```

Buka `http://localhost:8000`. Untuk GitHub Pages, gunakan sumber branch `main`, direktori root.

## Membuat ulang PDF

```bash
python3 -m pip install reportlab Pillow
python3 scripts/build_portfolio.py
```

Skrip membaca gambar di `assets/` dan pengalaman dari `index.html`. Teks profil, deskripsi bukti kerja, serta kredensial diatur di dalam skrip. Setelah mengubah data, periksa kembali website dan PDF. PDF menggunakan DejaVu bila tersedia dan font standar PDF sebagai alternatif.

## Pemeriksaan perubahan desain

- Sintaks JavaScript dan tautan aset lokal.
- Navigasi ponsel pada lebar 390 px, tanpa overflow horizontal.
- Filter seluruh karya dan kategori Tour & Travel.
- Dialog gambar dan penutupan dialog.
- Render visual seluruh 5 halaman PDF serta batas teks halaman.
