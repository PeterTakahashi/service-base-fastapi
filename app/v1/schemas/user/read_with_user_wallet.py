from pydantic import Field
from app.v1.schemas.user_wallet import UserWalletRead
from app.v1.schemas.user.read import UserRead


class UserWithUserWalletRead(UserRead):
    user_wallet: UserWalletRead = Field(
        description="The user_wallet associated with the user.",
    )
