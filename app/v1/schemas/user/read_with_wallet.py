from pydantic import Field
from app.v1.schemas.wallet import WalletRead
from app.v1.schemas.user.read import UserRead


class UserWithWalletRead(UserRead):
    wallet: WalletRead = Field(
        description="The wallet associated with the user.",
    )
