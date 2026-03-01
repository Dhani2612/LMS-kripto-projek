from PIL import Image

DELIMITER = "@@END@@"

def encode_lsb(input_image_path: str, output_image_path: str, secret_text: str):
    """Sembunyikan teks di gambar menggunakan LSB"""
    image = Image.open(input_image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    encoded = image.copy()
    width, height = image.size

    # Tambahkan delimiter
    secret_text += DELIMITER
    binary_text = ''.join(format(ord(i), '08b') for i in secret_text)
    data_index = 0

    for y in range(height):
        for x in range(width):
            if data_index >= len(binary_text):
                break
            r, g, b = image.getpixel((x, y))
            # Set bit LSB
            r = (r & ~1) | int(binary_text[data_index])
            data_index += 1
            if data_index < len(binary_text):
                g = (g & ~1) | int(binary_text[data_index])
                data_index += 1
            if data_index < len(binary_text):
                b = (b & ~1) | int(binary_text[data_index])
                data_index += 1
            encoded.putpixel((x, y), (r, g, b))
        if data_index >= len(binary_text):
            break

    encoded.save(output_image_path)

def decode_lsb(image_path: str) -> str:
    """Ambil teks yang disembunyikan di gambar menggunakan LSB"""
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    width, height = image.size
    binary_text = ''

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            binary_text += str(r & 1)
            binary_text += str(g & 1)
            binary_text += str(b & 1)

    # Split menjadi 8-bit chunks
    all_bytes = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    decoded_text = ''
    for byte in all_bytes:
        if len(byte) < 8:
            continue
        decoded_text += chr(int(byte, 2))
        if DELIMITER in decoded_text:
            break

    # Hapus delimiter
    return decoded_text.replace(DELIMITER, '')