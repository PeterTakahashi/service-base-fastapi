from hashids import Hashids  # type: ignore[import]
from app.core.config import settings

hashids = Hashids(min_length=settings.HASHIDS_MIN_LENGTH, salt=settings.HASHIDS_SALT)


def encode_id(id: int) -> str:
    """
    Encode an integer ID to a hashid string.
    """
    return hashids.encode(id)


def decode_id(hashid: str) -> int:
    """
    Decode a hashid string to an integer ID.
    """
    decoded = hashids.decode(hashid)
    if not decoded:
        raise ValueError(f"Invalid hashid: {hashid}")
    return decoded[0]
