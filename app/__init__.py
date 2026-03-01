# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager   # TAMBAHKAN INI
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load .env
load_dotenv()

# Inisialisasi database, migrate, dan login manager
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()          # BARU DITAMBAHKAN
limiter = Limiter(key_func=get_remote_address) # RATE LIMITER

login_manager.login_view = 'main.login'          # Arahkan ke halaman login
login_manager.login_message = 'Silakan login terlebih dahulu.'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)

    # Konfigurasi
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devsecret123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'mysql+pymysql://root:@localhost/kripto_sakti')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

    # Pastikan folder upload ada
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inisialisasi extension
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)          # AKTIFKAN LOGIN MANAGER
    limiter.init_app(app)                # AKTIFKAN RATE LIMITER

    # USER LOADER — WAJIB ADA AGAR current_user JALAN!
    from .models import Dosen, Mahasiswa

    @login_manager.user_loader
    def load_user(user_id):
        # Cek dulu di Dosen, kalau tidak ketemu cek di Mahasiswa
        user = Dosen.query.get(int(user_id))
        if user:
            return user
        return Mahasiswa.query.get(int(user_id))

    # Register blueprint
    from .routes import main
    app.register_blueprint(main)

    return app