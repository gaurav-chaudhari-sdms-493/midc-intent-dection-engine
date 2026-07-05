from app.core.jwt import (
    create_access_token,
    decode_token,
)


def test_access_token():

    token = create_access_token(
        subject="123",
        role="INVESTOR",
    )

    payload = decode_token(token)

    assert payload["sub"] == "123"
    assert payload["role"] == "INVESTOR"
