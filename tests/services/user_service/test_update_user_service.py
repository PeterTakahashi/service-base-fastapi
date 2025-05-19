import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from app.v1.services.user_service import UserService
from app.v1.schemas.user import UserUpdate
from app.models.user import User
from app.v1.repositories.user_repository import UserRepository
from fastapi_users import exceptions
from fastapi_users.router.common import ErrorCode


@pytest.mark.asyncio
async def test_update_me_success():
    # -- 1) UserRepository自体が必要ならモック (純粋に使わないなら None でもOK)
    repo_mock = MagicMock(spec=UserRepository)
    user_service = UserService(repo_mock)

    # -- 2) user_manager は fastapi-users の BaseUserManager をモック化して
    #        .update(...) が呼ばれたら更新済ユーザーを返すようにする
    user_manager_mock = AsyncMock()
    user_manager_mock.update.return_value = User(
        id="123e4567-e89b-12d3-a456-426614174000",
        email="updated@example.com",
        hashed_password="hashed_pwd",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )

    # -- 3) request をモック化
    request_mock = MagicMock(spec=Request)

    # -- 4) user_update, user をテストデータとして用意
    user_update = UserUpdate(email="updated@example.com", password=None)
    existing_user = User(
        id="123e4567-e89b-12d3-a456-426614174000",
        email="old@example.com",
        hashed_password="old_hashed_pwd",
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )

    # -- 5) いよいよメソッドを実行
    updated_user_read = await user_service.update_me(
        request=request_mock,
        user_manager=user_manager_mock,
        user_update=user_update,
        user=existing_user,  # current_active_user 相当
    )

    # -- 6) 結果のアサーション
    assert updated_user_read.email == "updated@example.com"
    assert updated_user_read.is_verified is True
    user_manager_mock.update.assert_awaited_once_with(
        user_update, existing_user, safe=True, request=request_mock
    )


@pytest.mark.asyncio
async def test_update_me_already_exists():
    """
    すでに同じ email のユーザーがいるなどで fastapi-users が UserAlreadyExists 例外を投げる想定をテスト
    """
    user_service = UserService(MagicMock(spec=UserRepository))
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

    # fastapi-users 内部では UserAlreadyExists が起きると
    # user_service 側は HTTPException(400) を投げるようにしている
    # のでそれを確認
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS


@pytest.mark.asyncio
async def test_update_me_password_invalid():
    """
    不正なパスワードのときに fastapi-users が InvalidPasswordException を投げる場合のテスト。
    """
    # -- 1) UserService インスタンス作成 (UserRepository はモック)
    repo_mock = MagicMock(spec=UserRepository)
    user_service = UserService(repo_mock)

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

    # -- 6) 発生した例外をアサート
    # user_service 側では InvalidPasswordException を受け取ると
    # HTTPException(400, detail={ code: ErrorCode.UPDATE_USER_INVALID_PASSWORD, reason: "..." }) を投げる。
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail["code"] == ErrorCode.UPDATE_USER_INVALID_PASSWORD
    assert "must contain at least one digit" in exc_info.value.detail["reason"]

    # -- 7) user_manager.update が正しく呼ばれたことも確認
    user_manager_mock.update.assert_awaited_once_with(
        user_update, existing_user, safe=True, request=request_mock
    )
