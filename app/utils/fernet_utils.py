# app/utils/fernet_utils.py
from cryptography.fernet import Fernet, InvalidToken
import os
from dotenv import load_dotenv

load_dotenv()

# Pastikan FERNET_KEY ada di .env!
FERNET_KEY = os.getenv('FERNET_KEY')
if not FERNET_KEY:
    raise ValueError("FERNET_KEY tidak ditemukan di .env! Buat dulu dengan: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'")

fernet = Fernet(FERNET_KEY.encode())

def encrypt_file(input_path: str, output_path: str) -> bool:
    """Enkripsi file, return True jika berhasil"""
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(output_path, 'wb') as f:
            f.write(encrypted)
        return True
    except Exception as e:
        print(f"[ENCRYPT ERROR] {e}")
        return False


def decrypt_file(input_path: str, output_path: str) -> bool:
    """Dekripsi file, return True jika berhasil"""
    try:
        if not os.path.exists(input_path):
            print(f"[DECRYPT ERROR] File tidak ditemukan: {input_path}")
            return False

        with open(input_path, 'rb') as f:
            data = f.read()

        if not data:
            print("[DECRYPT ERROR] File kosong!")
            return False

        decrypted = fernet.decrypt(data)  # ← akan raise InvalidToken jika salah kunci
        with open(output_path, 'wb') as f:
            f.write(decrypted)
        return True

    except InvalidToken:
        print("[DECRYPT ERROR] File bukan hasil enkripsi Fernet atau kunci salah!")
        return False
    except Exception as e:
        print(f"[DECRYPT ERROR] {e}")
        return False


def get_fernet_key():
    """Opsional: buat fungsi ini kalau mau dipakai di tempat lain"""
    return FERNET_KEY.encode()