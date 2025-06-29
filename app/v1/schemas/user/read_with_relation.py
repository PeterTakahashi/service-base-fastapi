from pydantic import Field
from app.v1.schemas.user_wallet import UserWalletRead
from app.v1.schemas.user.read import UserRead

from app.v1.schemas.common.address.read import AddressRead


class UserWithRelationRead(UserRead):
    user_wallet: UserWalletRead = Field(
        description="The user_wallet associated with the user.",
    )
    address: AddressRead | None = Field(
        None, description="Address associated with the user."
    )
