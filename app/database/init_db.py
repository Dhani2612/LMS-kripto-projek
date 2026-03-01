from app import create_app, db
from app.models import Dosen, Mahasiswa, Tugas, Transkrip

app = create_app()

with app.app_context():
    # Buat semua tabel jika belum ada
    db.create_all()
    print("✅ Database berhasil diinisialisasi")