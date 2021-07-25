from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

from bot.config import settings


def encrypt(data, public_key) -> bytes:
    cipher = Cipher_PKCS1_v1_5.new(public_key)
    return cipher.encrypt(data.encode())


def decrypt(data, private_key) -> str:
    decipher = Cipher_PKCS1_v1_5.new(private_key)
    return decipher.decrypt(data, None).decode()


def import_rsa_key_bytes(name: str) -> bytes:
    with open(settings.ROOT_DIR + f"/rsa/{name}", "rb") as fp:
        return fp.read()
