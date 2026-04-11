# app/utils/aes_utils.py
from Crypto.Cipher import AES
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Ambil AES key dari .env (base64 url-safe)
AES_KEY_B64 = os.getenv("AES_KEY_B64")
if not AES_KEY_B64:
    raise ValueError("AES_KEY_B64 tidak ditemukan di .env!")

try:
    AES_KEY = base64.urlsafe_b64decode(AES_KEY_B64)
    if len(AES_KEY) < 32:
        AES_KEY = AES_KEY.ljust(32, b'\0')   # padding kalau kurang
    AES_KEY = AES_KEY[:32]  # pastikan tepat 32 byte (AES-256)
except Exception as e:
    raise ValueError(f"Gagal decode AES_KEY_B64: {e}")

# === PKCS7 Padding & Unpadding ===
def pad(data: bytes) -> bytes:
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len]) * pad_len

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("Padding tidak valid")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Padding rusak")
    return data[:-pad_len]

# === AES-256 ECB Enkripsi & Dekripsi ===
def aes_encrypt(plain_text: str) -> str:
    raw = plain_text.encode("utf-8")
    padded = pad(raw)
    cipher = AES.new(AES_KEY, AES.MODE_ECB)        # HANYA 2 PARAMETER!
    encrypted = cipher.encrypt(padded)
    return base64.urlsafe_b64encode(encrypted).decode("utf-8")

def aes_decrypt(cipher_text: str) -> str:
    try:
        encrypted = base64.urlsafe_b64decode(cipher_text)
        cipher = AES.new(AES_KEY, AES.MODE_ECB)    # HANYA 2 PARAMETER!
        decrypted_padded = cipher.decrypt(encrypted)
        return unpad(decrypted_padded).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Gagal dekripsi teks: {e} (mungkin data rusak atau kunci salah)")