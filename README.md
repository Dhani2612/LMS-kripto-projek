# Kripto Sakti — Secure Learning Management System

Kripto Sakti adalah sebuah purwarupa aplikasi berbasis web bertema **Learning Management System (LMS)** yang dirancang secara khusus untuk mendemonstrasikan integrasi berbagai algoritma keamanan siber dan kriptografi modern ke dalam alur kerja pendidikan digital sehari-hari (seperti pengelolaan tugas mahasiswa dan transkrip akademik).

## Fitur Utama (Security & Features)

Aplikasi ini tidak sekadar bertindak sebagai sarana unggah-unduh file biasa, melainkan menyuntikkan keamanan tingkat tinggi di balik layar:

### 1. Hybrid Cryptography (File Tugas)
Saat Mahasiswa mengunggah file tugas (PDF/DOCX), sistem akan mengenkripsinya menggunakan kombinasi **AES-256** (Advanced Encryption Standard) dan dimodifikasi dengan **Caesar Cipher**. Dokumen asli tidak pernah disimpan secara utuh di server. Hanya Dosen pembimbing yang berwenang yang dapat mendekripsinya kembali.

### 2. Steganography LSB (Verifikasi Transkrip)
Saat Dosen mengunggah transkrip nilai Mahasiswa, sistem akan menyisipkan "Watermark Digital" atau metadata verifikasi ke dalam gambar (PNG/JPEG) menggunakan teknik **Least Significant Bit (LSB)**. Keaslian transkrip dapat diverifikasi tanpa merusak visual gambar secara kasat mata.

### 3. Secure Authentication (Werkzeug Scrypt)
Kata sandi (password) baik Dosen maupun Mahasiswa dilindungi menggunakan skema hashing modern (`scrypt`) dari kerangka kerja **Werkzeug Security**. Sistem juga mendukung backward compatibility dengan hash MD5 lama.

### 4. Anti Brute-Force (Rate Limiting)
Endpoint vital seperti gerbang Login dan Registrasi dilindungi dengan pembatasan lalu-lintas (**Rate Limiting**) menggunakan Flask-Limiter untuk mencegah serangan Brute-Force maupun spam otomatis.

### 5. Professional UI/UX
Antarmuka menggunakan desain clean card yang responsif berskala besar (1100px) dipadukan dengan pustaka ikon rapi dari **FontAwesome 6**, dengan balutan warna Professional LMS White & Modern Blue.

## Arsitektur & Teknologi

| Komponen | Teknologi |
|---|---|
| **Backend** | Python 3.x, Flask, Werkzeug |
| **Database** | MySQL (PyMySQL) via Flask-SQLAlchemy |
| **Frontend** | HTML5, Vanilla CSS3, FontAwesome 6 |
| **Security** | PyCryptodome (AES), Werkzeug (scrypt), Flask-Limiter, LSB Steganography |
| **HTTPS** | mkcert (self-signed certificate untuk development) |

## Panduan Instalasi (Development Mode)

### 1. Kloning Repositori
```bash
git clone https://github.com/Dhani2612/LMS-kripto-projek.git
cd LMS-kripto-projek
```

### 2. Atur Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependensi
```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login Flask-WTF Flask-Limiter PyMySQL PyCryptodome Pillow python-dotenv pyOpenSSL bcrypt waitress
```

### 4. Konfigurasi Environment
Buat file `.env` di root proyek:
```env
AES_KEY_B64=<your_base64_aes_key>
FERNET_KEY=<your_fernet_key>
MD5_SALT=saktisalt123
SECRET_KEY=devsecret123
DATABASE_URI=mysql+pymysql://root@localhost/kripto_sakti
```

### 5. Konfigurasi Database (MySQL)
1. Pastikan server MySQL (XAMPP/Laragon) sedang menyala.
2. Buat database baru: `kripto_sakti`
3. Import skema tabel dari file `database.sql`, **atau** jalankan migrasi:
```bash
python migrate_db.py
```

### 6. Generate Sertifikat HTTPS (Opsional)
```bash
mkcert.exe localhost 127.0.0.1
```
Pastikan file `localhost+1.pem` dan `localhost+1-key.pem` ada di root proyek.

### 7. Jalankan Server
```bash
python run.py
```
Aplikasi akan tersedia di: **https://localhost:5000**

## Struktur Proyek
```
kripto_sakti/
├── app/
│   ├── __init__.py          # App factory & konfigurasi
│   ├── models.py            # Model database (Dosen, Mahasiswa, Tugas, Transkrip)
│   ├── routes.py            # Semua route & logic
│   ├── database/
│   │   └── init_db.py       # Inisialisasi database
│   ├── static/              # CSS & asset statis
│   ├── templates/           # HTML templates (Jinja2)
│   ├── uploads/             # Folder upload sementara
│   └── utils/
│       ├── hash_utils.py    # Hashing password (Werkzeug scrypt + MD5 fallback)
│       ├── super_text.py    # Enkripsi teks (AES + Caesar)
│       ├── fernet_utils.py  # Enkripsi file (Fernet)
│       └── lsb_utils.py     # Steganografi LSB
├── instance/                # Database lokal (SQLite fallback)
├── database.sql             # Skema MySQL
├── migrate_db.py            # Script migrasi SQLite -> MySQL
├── run.py                   # Entry point aplikasi
├── test_super_text.py       # Unit test enkripsi
└── .env                     # Konfigurasi environment (tidak di-commit)
```

## Catatan Penting
- File `.env` **tidak di-commit** ke repository. Anda harus membuatnya sendiri.
- Sertifikat SSL (`*.pem`) **tidak di-commit**. Generate sendiri menggunakan `mkcert`.
- Untuk production, gunakan WSGI server seperti **Waitress** atau **Gunicorn**.

---

Dikembangkan oleh **Dhani Kartika Prihantyo** ([@Dhani2612](https://github.com/Dhani2612))
