from app.models.user import User


async def test_where_repository(user_repository, user):
    found_users = await user_repository.where(email=user.email, id=user.id)
    assert len(found_users) == 1
    assert found_users[0].id == user.id


async def test_where_repository_no_results(user_repository, faker):
    not_found_users = await user_repository.where(email=faker.email())
    assert not_found_users == []


async def test_where_repository_limit(user_repository, users):
    found_users = await user_repository.where(limit=2)
    assert len(found_users) == 2
    assert all(user.id in [u.id for u in users] for user in found_users)


async def test_where_repository_offset(user_repository, users):
    found_users = await user_repository.where(offset=5)
    assert len(found_users) == 5
    assert all(user.id in [u.id for u in users] for user in found_users)


async def test_where_repository_offset_and_limit(user_repository, users):
    found_users = await user_repository.where(limit=3, offset=2)
    assert len(found_users) == 3
    assert all(user.id in [u.id for u in users] for user in found_users)


async def test_where_repository_sorted(user_repository, users):
    found_users = await user_repository.where(sorted_by="email", sorted_order="asc")
    assert len(found_users) == 10
    assert found_users == sorted(found_users, key=lambda u: u.email)


async def test_where_repository_sorted_desc(user_repository, users):
    found_users = await user_repository.where(sorted_by="email", sorted_order="desc")
    assert len(found_users) == 10
    assert found_users == sorted(found_users, key=lambda u: u.email, reverse=True)


async def test_where_repository_joinedload(user_repository, users, wallets):
    found_users = await user_repository.where(joinedload_models=[User.wallet], limit=10)
    assert len(found_users) == 10
    for user in found_users:
        assert user.wallet is not None
        assert user.wallet.user_id == user.id


async def test_where_repository_lazyload(user_repository, users, wallets):
    found_users = await user_repository.where(lazyload_models=[User.wallet], limit=10)
    assert len(found_users) == 10
    for user in found_users:
        assert user.wallet is not None
        assert user.wallet.user_id == user.id
        assert user.wallet.balance is not None  # Ensure lazy loading worked


async def test_where_repository_attribute_error(user_repository):
    try:
        await user_repository.where(non_existent_column="value")
    except AttributeError as e:
        assert str(e) == "type object 'User' has no attribute 'non_existent_column'"
