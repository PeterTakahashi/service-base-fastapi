from app.lib.convert_id import encode_id, decode_id

def test_encode_id():
    print(encode_id(1))

def test_decode_id():
    encoded_id = encode_id(1)
    decoded_id = decode_id(encoded_id)
    assert decoded_id == 1
