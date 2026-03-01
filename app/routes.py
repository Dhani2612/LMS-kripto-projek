# app/routes.py
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    session, flash, send_file, current_app, make_response
)
from functools import wraps
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
from datetime import datetime
import json
import os

from . import limiter
from .models import db, Dosen, Mahasiswa, Tugas, Transkrip
from .utils.hash_utils import md5_hash, verify_md5
from .utils.super_text import encrypt_text, decrypt_text
from .utils.fernet_utils import encrypt_file, decrypt_file
from .utils.lsb_utils import encode_lsb, decode_lsb

# Buat folder uploads kalau belum ada
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

main = Blueprint('main', __name__)

# ------------------- DECORATOR -------------------
def login_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get('user_id'):
                flash("Silakan login dahulu.", "error")
                return redirect(url_for('main.login'))
            if role and session.get('role') != role:
                flash("Akses ditolak.", "error")
                return redirect(url_for('main.login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ------------------- ROUTES -------------------

@main.route('/')
def home():
    return redirect(url_for('main.login'))

# ---------- LOGIN & LOGOUT ----------
@main.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        # Cek Dosen
        dosen = Dosen.query.filter_by(nidn=identifier).first()
        if dosen and dosen.check_password(password):
            session['user_id'] = dosen.id
            session['role'] = 'dosen'
            return redirect(url_for('main.dashboard_dosen'))

        # Cek Mahasiswa
        mahasiswa = Mahasiswa.query.filter_by(nim=identifier).first()
        if mahasiswa and mahasiswa.check_password(password):
            session['user_id'] = mahasiswa.id
            session['role'] = 'mahasiswa'
            return redirect(url_for('main.dashboard_mahasiswa'))

        flash('Login gagal, cek NIM/NIDN dan password', 'error')

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('main.login'))

# ---------- REGISTER ----------
@main.route('/register/dosen', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def register_dosen():
    if request.method == 'POST':
        nama = request.form['nama']
        nidn = request.form['nidn']
        jurusan = request.form['jurusan']
        fakultas = request.form['fakultas']
        password = request.form['password']

        dosen = Dosen(nama=nama, nidn=nidn, jurusan=jurusan, fakultas=fakultas)
        dosen.set_password(password)
        db.session.add(dosen)
        db.session.commit()
        flash('Akun Dosen berhasil dibuat', 'success')
        return redirect(url_for('main.login'))

    return render_template('register_dosen.html')

@main.route('/register/mahasiswa', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def register_mahasiswa():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']
        fakultas = request.form['fakultas']
        dosen_wali_id = request.form['dosen_wali_id']
        password = request.form['password']

        mhs = Mahasiswa(nama=nama, nim=nim, jurusan=jurusan,
                        fakultas=fakultas, dosen_wali_id=dosen_wali_id)
        mhs.set_password(password)
        db.session.add(mhs)
        db.session.commit()
        flash('Akun Mahasiswa berhasil dibuat', 'success')
        return redirect(url_for('main.login'))

    dosen_list = Dosen.query.all()
    return render_template('register_mahasiswa.html', dosen_list=dosen_list)

# ---------- DASHBOARD ----------
@main.route('/dashboard/dosen')
@login_required(role='dosen')
def dashboard_dosen():
    dosen_id = session['user_id']
    mahasiswa_list = Mahasiswa.query.filter_by(dosen_wali_id=dosen_id).all()
    
    # Debug: cek apakah data masuk
    print(f"[DEBUG] Dosen ID: {dosen_id} → Mahasiswa: {[m.nama for m in mahasiswa_list]}")
    
    return render_template('dashboard_dosen.html', mahasiswa_list=mahasiswa_list)

@main.route('/dashboard/mahasiswa')
@login_required(role='mahasiswa')
def dashboard_mahasiswa():
    return render_template('dashboard_mahasiswa.html')

# ---------- TUGAS (DOSEN) ----------
@main.route('/dashboard/dosen/buat_tugas', methods=['GET', 'POST'])
@login_required(role='dosen')
def buat_tugas():
    dosen_id = session['user_id']
    mahasiswa_list = Mahasiswa.query.filter_by(dosen_wali_id=dosen_id).all()

    if request.method == 'POST':
        mahasiswa_id = request.form['mahasiswa_id']
        judul = request.form['judul']
        deskripsi = request.form['deskripsi']
        deskripsi_enc = encrypt_text(deskripsi)

        tugas = Tugas(mahasiswa_id=mahasiswa_id, dosen_id=dosen_id,
                      judul=judul, deskripsi_encrypted=deskripsi_enc)
        db.session.add(tugas)
        db.session.commit()
        flash('Tugas berhasil dibuat', 'success')
        return redirect(url_for('main.dashboard_dosen'))

    return render_template('buat_tugas.html', mahasiswa_list=mahasiswa_list)

@main.route('/dashboard/dosen/tugas_masuk')
@login_required(role='dosen')
def tugas_masuk_dosen():
    dosen_id = session['user_id']
    tugas_list = Tugas.query.filter_by(dosen_id=dosen_id).all()

    for t in tugas_list:
        t.komentar = decrypt_text(t.komentar_encrypted) if t.komentar_encrypted else "Belum ada komentar"
        t.status = "Sudah Upload" if t.file_encrypted else "Belum Upload"

    return render_template('tugas_masuk_dosen.html', tugas_list=tugas_list)

@main.route('/dashboard/dosen/tugas/<int:tugas_id>', methods=['GET', 'POST'])
@login_required(role='dosen')
def lihat_tugas_dosen(tugas_id):
    tugas = Tugas.query.get_or_404(tugas_id)
    deskripsi = decrypt_text(tugas.deskripsi_encrypted)
    komentar = decrypt_text(tugas.komentar_encrypted) if tugas.komentar_encrypted else ''

    if request.method == 'POST':
        komentar_baru = request.form.get('komentar', '')
        tugas.komentar_encrypted = encrypt_text(komentar_baru)
        db.session.commit()
        flash('Komentar berhasil disimpan!', 'success')

    return render_template('lihat_tugas_dosen.html', tugas=tugas,
                           deskripsi=deskripsi, komentar=komentar)

@main.route('/dashboard/dosen/download_tugas/<int:tugas_id>')
@login_required(role='dosen')
def download_tugas_dosen(tugas_id):
    tugas = Tugas.query.get_or_404(tugas_id)
    
    if not tugas.file_encrypted:
        flash('Mahasiswa belum mengumpulkan tugas.', 'error')
        return redirect(url_for('main.tugas_masuk_dosen'))

    upload_dir = current_app.config['UPLOAD_FOLDER']
    temp_enc = os.path.join(upload_dir, f"temp_enc_{tugas_id}.enc")
    temp_dec = os.path.join(upload_dir, f"temp_dec_{tugas_id}")

    try:
        # 1. Simpan file terenkripsi sementara
        with open(temp_enc, 'wb') as f:
            f.write(tugas.file_encrypted)

        # 2. Dekripsi — cek apakah berhasil
        if not decrypt_file(temp_enc, temp_dec):
            flash('Gagal mendekripsi file tugas. File mungkin rusak atau kunci salah.', 'error')
            return redirect(url_for('main.tugas_masuk_dosen'))

        # 3. Kirim file asli
        original_filename = f"tugas_{tugas.mahasiswa.nama.replace(' ', '_')}_{tugas.judul}.pdf"
        response = send_file(
            temp_dec,
            as_attachment=True,
            download_name=original_filename
        )

        # 4. Hapus file temp setelah download selesai
        @response.call_on_close
        def cleanup():
            for p in (temp_enc, temp_dec):
                try:
                    if os.path.exists(p):
                        os.remove(p)
                except:
                    pass

        return response

    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
        # Bersihkan file temp kalau error
        for p in (temp_enc, temp_dec):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except:
                pass
        return redirect(url_for('main.tugas_masuk_dosen'))

# ---------- TUGAS (MAHASISWA) ----------
@main.route('/dashboard/mahasiswa/tugas')
@login_required(role='mahasiswa')
def tugas_mahasiswa_list():
    tugas_list = Tugas.query.filter_by(mahasiswa_id=session['user_id']).all()
    return render_template('tugas_mahasiswa.html', tugas_list=tugas_list)

@main.route('/dashboard/mahasiswa/tugas/<int:tugas_id>', methods=['GET', 'POST'])
@login_required(role='mahasiswa')
def submit_tugas_mahasiswa(tugas_id):
    tugas = Tugas.query.get_or_404(tugas_id)
    deskripsi = decrypt_text(tugas.deskripsi_encrypted)
    komentar = decrypt_text(tugas.komentar_encrypted) if tugas.komentar_encrypted else ''

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename:
            orig_path = os.path.join(UPLOAD_FOLDER, f"tugas_{tugas_id}_{file.filename}")
            file.save(orig_path)
            enc_path = orig_path + '.enc'
            encrypt_file(orig_path, enc_path)
            with open(enc_path, 'rb') as f:
                tugas.file_encrypted = f.read()
            db.session.commit()
            flash('Tugas berhasil dikirim!', 'success')
            # Hapus file sementara
            for p in (orig_path, enc_path):
                try: os.remove(p)
                except: pass
            return redirect(url_for('main.dashboard_mahasiswa'))

    return render_template('submit_tugas.html', tugas=tugas,
                           deskripsi=deskripsi, komentar=komentar)

@main.route('/dashboard/mahasiswa/history_tugas')
@login_required(role='mahasiswa')
def history_tugas_mahasiswa():
    tugas_list = Tugas.query.filter_by(mahasiswa_id=session['user_id']).all()
    for t in tugas_list:
        t.komentar = decrypt_text(t.komentar_encrypted) if t.komentar_encrypted else "Belum ada komentar"
        t.status = "Sudah Upload" if t.file_encrypted else "Belum Upload"
    return render_template('history_tugas_mahasiswa.html', tugas_list=tugas_list)

# ---------- TRANSKRIP (DOSEN & MAHASISWA) ----------
ALLOWED_EXT = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@main.route('/dashboard/dosen/transkrip')
@login_required(role='dosen')
def transkrip_dosen():
    mahasiswa_list = Mahasiswa.query.all()
    return render_template('transkrip_dosen.html', mahasiswa_list=mahasiswa_list)

@main.route('/dashboard/dosen/upload_transkrip/<int:mahasiswa_id>', methods=['GET', 'POST'])
@login_required(role='dosen')
def upload_transkrip_dosen(mahasiswa_id):
    mahasiswa = Mahasiswa.query.get_or_404(mahasiswa_id)
    dosen = Dosen.query.get_or_404(session['user_id'])

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '' or not allowed_file(file.filename):
            flash('Pilih file gambar yang valid (PNG/JPG)', 'error')
            return redirect(request.url)

        # Buka gambar
        img = Image.open(file.stream).convert('RGBA')
        verif_data = {
            "nama_dosen_wali": request.form.get('nama_dosen_wali', dosen.nama),
            "nidn": request.form.get('nidn', dosen.nidn),
            "jurusan": request.form.get('jurusan', mahasiswa.jurusan),
            "fakultas": request.form.get('fakultas', mahasiswa.fakultas),
            "tanggal_verifikasi": datetime.utcnow().strftime('%Y-%m-%d')
        }
        message = json.dumps(verif_data, ensure_ascii=False)

        upload_dir = current_app.config['UPLOAD_FOLDER']
        src_path = os.path.join(upload_dir, f"src_{mahasiswa_id}_{int(datetime.utcnow().timestamp())}.png")
        out_path = os.path.join(upload_dir, f"stego_{mahasiswa_id}_{int(datetime.utcnow().timestamp())}.png")

        img.save(src_path, format='PNG')
        encode_lsb(src_path, out_path, message)

        with open(out_path, 'rb') as f:
            image_bytes = f.read()

        transkrip = Transkrip(
            mahasiswa_id=mahasiswa.id,
            dosen_id=dosen.id,
            nama_dosen_wali=verif_data["nama_dosen_wali"],
            nidn=verif_data["nidn"],
            jurusan=verif_data["jurusan"],
            fakultas=verif_data["fakultas"],
            nilai_image_encrypted=image_bytes,
            tanggal_verifikasi=datetime.utcnow()
        )
        db.session.add(transkrip)
        db.session.commit()

        # Cleanup
        for p in (src_path, out_path):
            try: os.remove(p)
            except: pass

        flash('Transkrip berhasil diunggah dan diverifikasi dengan LSB!', 'success')
        return redirect(url_for('main.dashboard_dosen'))

    return render_template('upload_transkrip.html', mahasiswa=mahasiswa, dosen=dosen)

@main.route('/dashboard/mahasiswa/transkrip')
@login_required(role='mahasiswa')
def lihat_transkrip_mahasiswa():
    transkrip_list = Transkrip.query.filter_by(mahasiswa_id=session['user_id']).all()

    for t in transkrip_list:
        if t.nilai_image_encrypted:
            tmp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"tmp_{t.id}.png")
            try:
                with open(tmp_path, 'wb') as f:
                    f.write(t.nilai_image_encrypted)
                decoded = decode_lsb(tmp_path)
                try:
                    t.verif_info = json.loads(decoded)
                except:
                    t.verif_info = {"raw": decoded}
            finally:
                try: os.remove(tmp_path)
                except: pass
        else:
            t.verif_info = None

    return render_template('lihat_transkrip.html', transkrip_list=transkrip_list)

@main.route('/dashboard/mahasiswa/transkrip/serve/<int:transkrip_id>')
@login_required(role='mahasiswa')
def serve_transkrip(transkrip_id):
    t = Transkrip.query.get_or_404(transkrip_id)
    if t.mahasiswa_id != session['user_id']:
        flash('Akses ditolak', 'error')
        return redirect(url_for('main.login'))
    return send_file(BytesIO(t.nilai_image_encrypted), mimetype='image/png',
                     as_attachment=False, download_name=f"transkrip_{t.id}.png")

@main.route('/dashboard/mahasiswa/transkrip/download/<int:transkrip_id>')
@login_required(role='mahasiswa')
def download_transkrip(transkrip_id):
    t = Transkrip.query.get_or_404(transkrip_id)
    if t.mahasiswa_id != session['user_id']:
        flash('Akses ditolak', 'error')
        return redirect(url_for('main.login'))
    return send_file(BytesIO(t.nilai_image_encrypted), mimetype='image/png',
                     as_attachment=True, download_name=f"transkrip_{t.id}.png")