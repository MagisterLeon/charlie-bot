from bot.crypto import encrypt_data, decrypt_data


def test_encryption(public_key, private_key):
    # given
    data = "hello charlie!"

    # when
    result = encrypt_data(data, public_key)

    # then
    assert decrypt_data(result, private_key) == data
