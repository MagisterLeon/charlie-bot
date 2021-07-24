from bot.crypto import encrypt, decrypt


def test_encryption(public_key, private_key):
    # given
    data = "hello charlie!"

    # when
    result = encrypt(data, public_key)

    # then
    assert decrypt(result, private_key) == data
