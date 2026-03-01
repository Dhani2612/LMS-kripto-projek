# 🎓 Kripto Sakti LMS (Learning Management System)

Kripto Sakti adalah sebuah purwarupa aplikasi berbasis web bertema *Learning Management System* (LMS) yang dirancang secara khusus untuk mendemonstrasikan integrasi berbagai logaritma keamanan siber dan kriptografi modern ke dalam alur kerja pendidikan digital sehari-hari (seperti pengelolaan tugas mahasiswa dan transkrip akademik).

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![UI](https://img.shields.io/badge/UI/UX-Modern_Blue-0F62FE?style=for-the-badge)

---

## ✨ Fitur Utama (Security & Features)

Aplikasi ini tidak sekadar bertindak sebagai sarana unggah-unduh file biasa, melainkan menyuntikkan keamanan tingkat tinggi di balik layar:

1. **🔒 Hybrid Cryptography (File Tugas)**
   - Saat Mahasiswa mengunggah file tugas (PDF/DOCX), sistem akan mengenkripsinya menggunakan kombinasi **AES-256** (Advanced Encryption Standard) dan dimodifikasi dengan **Caesar Cipher**.
   - Dokumen asli tidak pernah disimpan secara utuh di *server*. Hanya Dosen pembimbing yang berwenang yang dapat mendekripsinya kembali. 
2. **🛡️ Steganography LSB (Verifikasi Transkrip)**
   - Saat Dosen mengunggah transkrip nilai Mahasiswa, sistem akan menyisipkan *"Watermark Digital"* atau metadata verifikasi kejut ke dalam gambar (PNG/JPEG) menggunakan teknik **Least Significant Bit (LSB)**.
   - Hak aslina transkrip dapat diverifikasi tanpa merusak visual gambar secara kasat mata.
3. **🔑 Secure Authentication (Bcrypt)**
   - Kata sandi (password) baik Dosen maupun Mahasiswa dilindungi secara absolut menggunakan skema hashing modern (`pbkdf2:sha256` / `Bcrypt`) dari kerangka kerja *Werkzeug Security*.
4. **🚦 Anti Brute-Force (Rate Limiting)**
   - Endpoint vital seperti gerbang Login dan Registrasi dilindungi dengan pembatasan lalu-lintas (Rate Limiting) untuk mencegah serangan *Brute-Force* maupun spam otomatis oleh bot.
5. **🎨 Professional UI/UX**
   - Mengusung balutan warna modis *Professional LMS White & Modern Blue*, antarmuka menggunakan desain _clean card_ yang responsif berskala besar (`1100px`) dipadukan dengan pustaka ikon rapi dari *FontAwesome 6*.

---

## 🛠️ Arsitektur & Teknologi

* **Backend**: Python 3.x, Flask, Werkzeug
* **Database**: MySQL (PyMySQL) via Flask-SQLAlchemy
* **Frontend**: HTML5, Vanilla CSS3 (Custom Design System CSS), FontAwesome
* **Security & Crypto**: PyCryptodome (AES), Flask-Limiter, LSB Steganography Engine

---

## ⚙️ Panduan Instalasi (Development Mode)

Ikuti langkah-langkah di bawah ini untuk menjalankan Kripto Sakti secara lokal di komputer Anda:

### 1. Kloning Repositori
```bash
git clone https://github.com/Dhani2612/LMS-kripto-projek.git
cd LMS-kripto-projek
```

### 2. Atur Virtual Environment (Opsional tapi Direkomendasikan)
```bash
python -m venv venv
# Untuk Windows:
venv\Scripts\activate
# Untuk macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```
*(Catatan: Anda mungkin perlu membuat file `requirements.txt` atau mendownload modul seperti `Flask`, `Flask-SQLAlchemy`, `PyMySQL`, `PyCryptodome`, dan `Flask-Limiter` secara manual)*

### 4. Konfigurasi Database (MySQL)
- Pastikan server database MySQL Anda (seperti XAMPP / Laragon) sedang menyala.
- Buat database baru bernama `kripto_sakti`.
- Import skema tabel yang telah disediakan di file `database.sql` ke dalam database tersebut.
- Pastikan URI akses database di `app/__init__.py` sesuai dengan *credential* lokal Anda (misal: `mysql+pymysql://root:@localhost/kripto_sakti`).

### 5. Jalankan Server
```bash
python run.py
```
Aplikasi akan tersedia pada antarmuka lokal dengan *auto-reload* HTTPS:
**👉 https://localhost:5000**

---

## 👨‍💻 Hak Cipta & Pengembang

Proyek ini dibangun sebagai dedikasi terhadap integrasi keamanan informasi dalam lingkungan akademik. 
* _Dikembangkan oleh Dhani Kartika Prihantyo (Dhani2612)_
