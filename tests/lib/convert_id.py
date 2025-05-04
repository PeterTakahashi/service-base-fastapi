from app.lib.convert_id import encode_id, decode_id
from app.core.config import settings


def test_encode_id():
    encoded_id = encode_id(1)
    len(encoded_id) == settings.HASHIDS_MIN_LENGTH


def test_decode_id():
    encoded_id = encode_id(1)
    decoded_id = decode_id(encoded_id)
    assert decoded_id == 1
