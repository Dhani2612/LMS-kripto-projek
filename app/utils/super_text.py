# app/utils/super_text.py
from .caesar import caesar_encrypt, caesar_decrypt
from .aes_utils import aes_encrypt, aes_decrypt

def encrypt_text(plain_text: str) -> str:
    """
    Super Enkripsi: Caesar Cipher → AES-256 ECB
    """
    if not plain_text:
        return ""
    caesar = caesar_encrypt(plain_text)
    return aes_encrypt(caesar)

def decrypt_text(cipher_text: str) -> str:
    """
    Super Dekripsi: AES-256 ECB → Caesar Cipher
    """
    if not cipher_text:
        return ""
    aes_decrypted = aes_decrypt(cipher_text)
    return caesar_decrypt(aes_decrypted)