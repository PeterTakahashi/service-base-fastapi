import pytest


@pytest.mark.asyncio
async def test_where_exact(user_repository, user):
    """email__exact -> 完全一致"""
    found_users = await user_repository.where(email__exact=user.email)
    assert len(found_users) == 1
    assert found_users[0].id == user.id


@pytest.mark.asyncio
async def test_where_iexact(user_repository, user):
    """email__iexact -> 大文字小文字を区別しない完全一致"""
    found_users = await user_repository.where(email__iexact=user.email.upper())
    assert len(found_users) == 1
    assert found_users[0].id == user.id


@pytest.mark.asyncio
async def test_where_contains(user_repository, user):
    """email__contains -> 部分一致（大文字小文字区別あり）"""
    # user.email の一部分を抽出
    substring = user.email[:3]
    found_users = await user_repository.where(email__contains=substring)
    # 大文字小文字区別があるので、もし substring を大文字化すればヒットしない可能性がある
    assert any(u.id == user.id for u in found_users)


@pytest.mark.asyncio
async def test_where_icontains(user_repository, user):
    """email__icontains -> 部分一致（大文字小文字区別なし）"""
    substring = user.email[:3].upper()
    found_users = await user_repository.where(email__icontains=substring)
    assert any(u.id == user.id for u in found_users)


@pytest.mark.asyncio
async def test_where_in(user_repository, user, faker):
    """email__in -> in 演算子"""
    fake_email = faker.email()
    found_users = await user_repository.where(email__in=[user.email, fake_email])
    # user.email は存在するので1人ヒットするはず
    assert len(found_users) == 1
    assert found_users[0].id == user.id


@pytest.mark.asyncio
async def test_where_startswith(user_repository, user):
    """email__startswith -> 前方一致（大文字小文字区別あり）"""
    prefix = user.email.split("@")[0][:3]  # 例: メールユーザー名の先頭3文字
    found_users = await user_repository.where(email__startswith=prefix)
    assert any(u.id == user.id for u in found_users)


@pytest.mark.asyncio
async def test_where_istartswith(user_repository, user):
    """email__istartswith -> 前方一致（大文字小文字区別なし）"""
    prefix = user.email.split("@")[0][:3].upper()  # 大文字にして検索
    found_users = await user_repository.where(email__istartswith=prefix)
    assert any(u.id == user.id for u in found_users)


@pytest.mark.asyncio
async def test_where_endswith(user_repository, user):
    """email__endswith -> 後方一致（大文字小文字区別あり）"""
    suffix = user.email.split("@")[-1]  # ドメイン部分
    found_users = await user_repository.where(email__endswith=suffix)
    assert any(u.id == user.id for u in found_users)


@pytest.mark.asyncio
async def test_where_iendswith(user_repository, user):
    """email__iendswith -> 後方一致（大文字小文字区別なし）"""
    suffix = user.email.split("@")[-1].upper()
    found_users = await user_repository.where(email__iendswith=suffix)
    assert any(u.id == user.id for u in found_users)
