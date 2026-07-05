from app.repositories import user_repository


def test_repository():
    assert user_repository is not None
