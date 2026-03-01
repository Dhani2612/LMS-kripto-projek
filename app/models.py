# app/models.py
from datetime import datetime
from . import db
from .utils.hash_utils import md5_hash, verify_md5
from flask_login import UserMixin  # SUDAH ADA, TINGGAL DIPAKAI!

# ---------------- DOSEN ----------------
class Dosen(UserMixin, db.Model):
    __tablename__ = 'dosen'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nidn = db.Column(db.String(50), unique=True, nullable=False)
    jurusan = db.Column(db.String(50), nullable=False)
    fakultas = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    mahasiswa = db.relationship('Mahasiswa', backref='dosen_wali', lazy=True)
    tugas = db.relationship('Tugas', backref='dosen', lazy=True)
    transkrip = db.relationship('Transkrip', backref='dosen', lazy=True)

    # INI YANG BARU DITAMBAHKAN (WAJIB!)
    role = 'dosen'  # Biar decorator tahu ini dosen

    def set_password(self, password):
        self.password_hash = md5_hash(password)

    def check_password(self, password):
        return verify_md5(password, self.password_hash)

    # Flask-Login butuh ini
    def get_id(self):
        return str(self.id)


# ---------------- MAHASISWA ----------------
class Mahasiswa(UserMixin, db.Model):
    __tablename__ = 'mahasiswa'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nim = db.Column(db.String(50), unique=True, nullable=False)
    jurusan = db.Column(db.String(50), nullable=False)
    fakultas = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    dosen_wali_id = db.Column(db.Integer, db.ForeignKey('dosen.id'), nullable=False)

    tugas = db.relationship('Tugas', backref='mahasiswa', lazy=True)
    transkrip = db.relationship('Transkrip', backref='mahasiswa', lazy=True)

    # INI YANG BARU DITAMBAHKAN (WAJIB!)
    role = 'mahasiswa'  # Biar decorator tahu ini mahasiswa

    def set_password(self, password):
        self.password_hash = md5_hash(password)

    def check_password(self, password):
        return verify_md5(password, self.password_hash)

    # Flask-Login butuh ini
    def get_id(self):
        return str(self.id)


# ---------------- TUGAS ----------------
class Tugas(db.Model):
    __tablename__ = 'tugas'
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.id'), nullable=False)
    judul = db.Column(db.String(200), nullable=False)
    deskripsi_encrypted = db.Column(db.Text, nullable=False)
    file_encrypted = db.Column(db.LargeBinary, nullable=True)
    komentar_encrypted = db.Column(db.Text, nullable=True)


# ---------------- TRANSKRIP ----------------
class Transkrip(db.Model):
    __tablename__ = 'transkrip'
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.id'), nullable=False)
    nama_dosen_wali = db.Column(db.String(100), nullable=False)
    nidn = db.Column(db.String(50), nullable=False)
    jurusan = db.Column(db.String(50), nullable=False)
    fakultas = db.Column(db.String(50), nullable=False)
    nilai_image_encrypted = db.Column(db.LargeBinary, nullable=False)
    tanggal_verifikasi = db.Column(db.DateTime, default=datetime.utcnow)