from datetime import datetime, timedelta, timezone

import base64
import hashlib
import hmac
import os

import jwt

from fastapi import HTTPException, Request

from .config import get_settings


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    """

    rounds = 310_000

    salt = os.urandom(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        rounds,
    )

    salt_encoded = base64.b64encode(
        salt
    ).decode("ascii")

    digest_encoded = base64.b64encode(
        digest
    ).decode("ascii")

    return (
        f"pbkdf2_sha256$"
        f"{rounds}$"
        f"{salt_encoded}$"
        f"{digest_encoded}"
    )


def verify_password(
    password: str,
    stored_password: str,
) -> bool:
    try:
        scheme, rounds, salt_b64, digest_b64 = (
            stored_password.split("$")
        )

        if scheme != "pbkdf2_sha256":
            return False

        salt = base64.b64decode(
            salt_b64
        )

        expected_digest = base64.b64decode(
            digest_b64
        )

        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(rounds),
        )

        return hmac.compare_digest(
            actual_digest,
            expected_digest,
        )

    except (
        ValueError,
        TypeError,
        base64.binascii.Error,
    ):
        return False


def create_access_token(
    user_id: int,
) -> str:
    settings = get_settings()

    expiration = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.jwt_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_token(token: str) -> int:
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        return int(payload["sub"])

    except (
        jwt.InvalidTokenError,
        KeyError,
        ValueError,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token.",
        )


def get_current_user_id(
    request: Request,
) -> int:
    token = request.cookies.get(
        "access_token"
    )

    if not token:
        authorization = request.headers.get(
            "Authorization",
            "",
        )

        if authorization.lower().startswith(
            "bearer "
        ):
            token = authorization[7:].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
        )

    return decode_token(token)