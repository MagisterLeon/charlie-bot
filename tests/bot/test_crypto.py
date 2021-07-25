from Crypto.PublicKey import RSA

from bot.crypto import encrypt, decrypt


def test_encryption(public_key, private_key):
    # given
    data = "hello charlie!"
    RSA.importKey(private_key)

    # when
    result = encrypt(data, RSA.importKey(public_key))

    # then
    assert decrypt(result, RSA.importKey(private_key)) == data
