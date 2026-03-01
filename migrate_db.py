import sqlite3
import pymysql
import os
from datetime import datetime

# 1. Hubungkan ke MySQL dan buat DB
mysql_conn = pymysql.connect(host='localhost', user='root', password='')
cursor = mysql_conn.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS kripto_sakti;')
cursor.execute('USE kripto_sakti;')

# 2. Buat tabel di MySQL (sesuai struktur models.py Flask)
cursor.execute('''
CREATE TABLE IF NOT EXISTS dosen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    nidn VARCHAR(50) NOT NULL UNIQUE,
    jurusan VARCHAR(50) NOT NULL,
    fakultas VARCHAR(50) NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS mahasiswa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    nim VARCHAR(50) NOT NULL UNIQUE,
    jurusan VARCHAR(50) NOT NULL,
    fakultas VARCHAR(50) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    dosen_wali_id INT NOT NULL,
    FOREIGN KEY (dosen_wali_id) REFERENCES dosen(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tugas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mahasiswa_id INT NOT NULL,
    dosen_id INT NOT NULL,
    judul VARCHAR(200) NOT NULL,
    deskripsi_encrypted TEXT NOT NULL,
    file_encrypted LONGBLOB,
    komentar_encrypted TEXT,
    FOREIGN KEY (mahasiswa_id) REFERENCES mahasiswa(id),
    FOREIGN KEY (dosen_id) REFERENCES dosen(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transkrip (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mahasiswa_id INT NOT NULL,
    dosen_id INT NOT NULL,
    nama_dosen_wali LONGTEXT NOT NULL,
    nidn LONGTEXT NOT NULL,
    jurusan LONGTEXT NOT NULL,
    fakultas LONGTEXT NOT NULL,
    nilai_image_encrypted LONGBLOB NOT NULL,
    tanggal_verifikasi DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mahasiswa_id) REFERENCES mahasiswa(id),
    FOREIGN KEY (dosen_id) REFERENCES dosen(id)
);
''')

# 3. Ambil data dari SQLite
sqlite_path = os.path.join('instance', 'sakti.db')
if not os.path.exists(sqlite_path):
    print("Database SQLite tidak ditemukan di " + sqlite_path)
    exit()

sqlite_conn = sqlite3.connect(sqlite_path)
sqlite_cursor = sqlite_conn.cursor()

# Migrate Dosen
sqlite_cursor.execute("SELECT id, nama, nidn, jurusan, fakultas, password_hash FROM dosen")
dosen_data = sqlite_cursor.fetchall()
for d in dosen_data:
    try:
        cursor.execute("INSERT INTO dosen (id, nama, nidn, jurusan, fakultas, password_hash) VALUES (%s, %s, %s, %s, %s, %s)", d)
    except Exception as e:
        print(f"Skip Dosen {d[0]}: {e}")

# Migrate Mahasiswa
sqlite_cursor.execute("SELECT id, nama, nim, jurusan, fakultas, password_hash, dosen_wali_id FROM mahasiswa")
mhs_data = sqlite_cursor.fetchall()
for m in mhs_data:
    try:
        cursor.execute("INSERT INTO mahasiswa (id, nama, nim, jurusan, fakultas, password_hash, dosen_wali_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", m)
    except Exception as e:
        print(f"Skip Mahasiswa {m[0]}: {e}")

# Migrate Tugas
sqlite_cursor.execute("SELECT id, mahasiswa_id, dosen_id, judul, deskripsi_encrypted, file_encrypted, komentar_encrypted FROM tugas")
tugas_data = sqlite_cursor.fetchall()
for t in tugas_data:
    try:
        cursor.execute("INSERT INTO tugas (id, mahasiswa_id, dosen_id, judul, deskripsi_encrypted, file_encrypted, komentar_encrypted) VALUES (%s, %s, %s, %s, %s, %s, %s)", t)
    except Exception as e:
        print(f"Skip Tugas {t[0]}: {e}")

# Migrate Transkrip
sqlite_cursor.execute("SELECT id, mahasiswa_id, dosen_id, nama_dosen_wali, nidn, jurusan, fakultas, nilai_image_encrypted, tanggal_verifikasi FROM transkrip")
transkrip_data = sqlite_cursor.fetchall()
for tr in transkrip_data:
    try:
        cursor.execute("INSERT INTO transkrip (id, mahasiswa_id, dosen_id, nama_dosen_wali, nidn, jurusan, fakultas, nilai_image_encrypted, tanggal_verifikasi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", tr)
    except Exception as e:
        print(f"Skip Transkrip {tr[0]}: {e}")

mysql_conn.commit()
cursor.close()
mysql_conn.close()
sqlite_cursor.close()
sqlite_conn.close()

print("✅ Migrasi data dari SQLite ke MySQL selesai!")
