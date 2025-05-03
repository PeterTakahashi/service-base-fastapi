from typing import Optional
from app.v1.schemas.base import HasEncodedID

class CharacterImageRead(HasEncodedID):
    image_url: Optional[str] # NOTE: 基本的には空にならないが、画像アップロードに失敗した場合などを考慮してOptionalにしている
