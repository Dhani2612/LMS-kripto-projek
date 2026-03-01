from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def md5_hash(password: str) -> str:
    """
    Menghasilkan hash yang lebih aman menggunakan default werkzeug (pbkdf2:sha256 atau scrypt).
    Nama fungsi dipertahankan agar kompatibel dengan pemanggilan di file models.py.
    """
    return generate_password_hash(password)

def verify_md5(password: str, hashed: str) -> bool:
    """
    Verifikasi password input dengan hash tersimpan.
    Mendukung pengecekan hash lama (MD5) sekaligus hash baru.
    """
    # Fallback untuk MD5 (agar user dengan hash lama tetap bisa login)
    if not hashed.startswith('pbkdf2:sha256') and not hashed.startswith('scrypt'):
        SALT = os.getenv("MD5_SALT", "default_salt")
        import hashlib
        salted = password + SALT
        legacy_md5 = hashlib.md5(salted.encode()).hexdigest()
        return legacy_md5 == hashed

    return check_password_hash(hashed, password)