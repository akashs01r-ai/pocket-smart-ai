from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response,
)

from .database import get_conn
from .models import (
    LoginRequest,
    RegisterRequest,
)
from .security import (
    create_access_token,
    get_current_user_id,
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
)


@router.post("/register")
def register(
    payload: RegisterRequest,
):
    with get_conn() as connection:

        existing = connection.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (payload.email,),
        ).fetchone()

        if existing:
            raise HTTPException(
                status_code=409,
                detail=(
                    "An account with this "
                    "email already exists."
                ),
            )

        cursor = connection.execute(
            """
            INSERT INTO users
                (name, email, password_hash)
            VALUES
                (?, ?, ?)
            """,
            (
                payload.name.strip(),
                payload.email,
                hash_password(
                    payload.password
                ),
            ),
        )

        user_id = cursor.lastrowid

    return {
        "message": "Registration successful",

        "user": {
            "id": user_id,
            "name": payload.name,
            "email": payload.email,
        },
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response,
):
    with get_conn() as connection:

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (payload.email,),
        ).fetchone()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    if not verify_password(
        payload.password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    token = create_access_token(
        user["id"]
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 24 * 60,
    )

    return {
        "message": "Login successful",

        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        },
    }


@router.post("/logout")
def logout(
    response: Response,
):
    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out"
    }


@router.get("/me")
def me(
    request: Request,
):
    user_id = get_current_user_id(
        request
    )

    with get_conn() as connection:

        user = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return {
        "user": dict(user)
    }