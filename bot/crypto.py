from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5


def encrypt_data(data, public_key) -> bytes:
    cipher = Cipher_PKCS1_v1_5.new(public_key)
    return cipher.encrypt(data.encode())


def decrypt_data(data, private_key) -> str:
    decipher = Cipher_PKCS1_v1_5.new(private_key)
    return decipher.decrypt(data, None).decode()
