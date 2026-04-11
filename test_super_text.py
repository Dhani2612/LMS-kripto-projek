import os
from dotenv import load_dotenv
load_dotenv()

from app.utils.super_text import encrypt_text, decrypt_text

def test_super_text():
    # Ambil AES_KEY_B64 dan FERNET_KEY dari .env hanya untuk informasi
    AES_KEY_B64 = os.getenv("AES_KEY_B64")
    FERNET_KEY = os.getenv("FERNET_KEY")
    MD5_SALT = os.getenv("MD5_SALT")
    
    print("AES_KEY_B64:", AES_KEY_B64)
    print("FERNET_KEY:", FERNET_KEY)
    print("MD5_SALT:", MD5_SALT)
    print("====================================")
    
    # Teks uji
    teks_asli = "Halo Mahasiswa SAKTI 123!"
    print("Teks Asli:", teks_asli)

    # Enkripsi
    teks_terenkripsi = encrypt_text(teks_asli)
    print("Teks Terenkripsi:", teks_terenkripsi)

    # Dekripsi
    teks_didekripsi = decrypt_text(teks_terenkripsi)
    print("Teks Didekripsi:", teks_didekripsi)

    # Cek konsistensi
    if teks_asli == teks_didekripsi:
        print("✅ Test berhasil: Teks didekripsi sesuai aslinya")
    else:
        print("❌ Test gagal: Hasil dekripsi tidak sama dengan asli")

if __name__ == "__main__":
    test_super_text()