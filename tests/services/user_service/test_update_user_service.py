import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from app.v1.schemas.user import UserUpdate
from app.models.user import User
from fastapi_users import exceptions
from app.lib.error_code import ErrorCode
from tests.common.check_api_exception_info import check_api_exception_info
from fastapi import status


@pytest.mark.asyncio
async def test_update_with_address_success(user_service, fake_address, user):
    user_manager_mock = AsyncMock()
    user_manager_mock.update.return_value = user

    # -- 3) request をモック化
    request_mock = MagicMock(spec=Request)

    # -- 4) user_update, user をテストデータとして用意
    user_update = UserUpdate(
        email="updated@example.com", password=None, address=fake_address
    )
    # -- 5) いよいよメソッドを実行
    updated_user_read = await user_service.update_me(
        request=request_mock,
        user_manager=user_manager_mock,
        user_update=user_update,
        user=user,
    )

    # -- 6) 結果のアサーション
    assert updated_user_read.address == fake_address
    user_manager_mock.update.assert_awaited_once_with(
        user_update, user, safe=True, request=request_mock
    )


@pytest.mark.asyncio
async def test_update_me_already_exists(user_service):
    """
    すでに同じ email のユーザーがいるなどで fastapi-users が UserAlreadyExists 例外を投げる想定をテスト
    """
    user_manager_mock = AsyncMock()
    # .update(...) が例外を吐くように設定
    user_manager_mock.update.side_effect = exceptions.UserAlreadyExists()

    with pytest.raises(Exception) as exc_info:
        await user_service.update_me(
            request=MagicMock(spec=Request),
            user_manager=user_manager_mock,
            user_update=UserUpdate(email="duplicate@example.com"),
            user=User(
                id="123e4567-e89b-12d3-a456-426614174000",
                email="old@example.com",
                hashed_password="old_hashed_pwd",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            ),
        )

    check_api_exception_info(
        exc_info,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail_code=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        pointer="email",
    )


@pytest.mark.asyncio
async def test_update_me_password_invalid(user_service):
    """
    不正なパスワードのときに fastapi-users が InvalidPasswordException を投げる場合のテスト。
    """

    # -- 2) user_manager をモック化
    user_manager_mock = AsyncMock()
    # .update(...) が不正パスワード例外を投げるように設定
    user_manager_mock.update.side_effect = exceptions.InvalidPasswordException(
        reason="Password must contain at least one digit"
    )

    # -- 3) request をモック化
    request_mock = MagicMock(spec=Request)

    # -- 4) UserUpdate と 既存ユーザーを準備
    user_update = UserUpdate(email=None, password="invalidpass")
    existing_user = User(
        id="123e4567-e89b-12d3-a456-426614174000",
        email="old@example.com",
        hashed_password="old_hashed_pwd",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )

    # -- 5) 例外発生を確認
    with pytest.raises(Exception) as exc_info:
        await user_service.update_me(
            request=request_mock,
            user_manager=user_manager_mock,
            user_update=user_update,
            user=existing_user,
        )

    check_api_exception_info(
        exc_info,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail_code=ErrorCode.UPDATE_USER_INVALID_PASSWORD,
        detail_detail="Password must contain at least one digit",
        pointer="password",
    )

    # -- 7) user_manager.update が正しく呼ばれたことも確認
    user_manager_mock.update.assert_awaited_once_with(
        user_update, existing_user, safe=True, request=request_mock
    )
