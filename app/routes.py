import json

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)

from .config import get_settings
from .database import get_conn
from .models import (
    HomeRequest,
    JewelryRequest,
    PartyRequest,
)
from .recommendations import (
    generate_home,
    generate_jewelry,
    generate_party,
)
from .security import get_current_user_id


router = APIRouter(
    prefix="/api",
    tags=["planners"],
)


def save_recommendation(
    user_id: int,
    planner: str,
    budget: float,
    request_data: dict,
    response_data: dict,
) -> int:

    with get_conn() as connection:

        cursor = connection.execute(
            """
            INSERT INTO recommendations
                (
                    user_id,
                    planner,
                    budget,
                    request_json,
                    response_json
                )
            VALUES
                (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                planner,
                budget,
                json.dumps(
                    request_data
                ),
                json.dumps(
                    response_data
                ),
            ),
        )

        return cursor.lastrowid


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "PocketSmart AI",
    }


@router.post("/generate-home")
def home(
    payload: HomeRequest,
    request: Request,
):

    user_id = get_current_user_id(
        request
    )

    data = payload.model_dump()

    result = generate_home(
        data
    )

    history_id = save_recommendation(
        user_id=user_id,
        planner="home",
        budget=payload.budget,
        request_data=data,
        response_data=result,
    )

    result["history_id"] = history_id

    return result


@router.post("/generate-party")
def party(
    payload: PartyRequest,
    request: Request,
):

    user_id = get_current_user_id(
        request
    )

    data = payload.model_dump()

    result = generate_party(
        data
    )

    history_id = save_recommendation(
        user_id=user_id,
        planner="party",
        budget=payload.budget,
        request_data=data,
        response_data=result,
    )

    result["history_id"] = history_id

    return result


@router.post("/generate-jewelry")
async def jewelry(
    request: Request,
    budget: float = Form(default=0),
    occasion: str = Form(default="Wedding"),
    style: str = Form(default="Elegant"),
    outfit_notes: str = Form(default=""),
    outfit_image: UploadFile | None = File(
        default=None
    ),
):

    user_id = get_current_user_id(
        request
    )

    if budget <= 0:
        raise HTTPException(
            status_code=422,
            detail=(
                "Budget must be greater than zero."
            ),
        )

    settings = get_settings()

    image_bytes = None
    mime_type = None

    if (
        outfit_image
        and outfit_image.filename
    ):

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPEG, PNG, or WEBP "
                    "images are supported."
                ),
            )

        image_bytes = (
            await outfit_image.read()
        )

        max_bytes = (
            settings.max_upload_mb
            * 1024
            * 1024
        )

        if len(image_bytes) > max_bytes:
            raise HTTPException(
                status_code=413,
                detail="Image is too large.",
            )

        mime_type = (
            outfit_image.content_type
        )

    data = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        outfit_notes=outfit_notes,
    ).model_dump()

    result = generate_jewelry(
        data,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )

    history_id = save_recommendation(
        user_id=user_id,
        planner="jewelry",
        budget=budget,
        request_data=data,
        response_data=result,
    )

    result["history_id"] = history_id

    return result


@router.get("/history")
def history(
    request: Request,
):

    user_id = get_current_user_id(
        request
    )

    with get_conn() as connection:

        rows = connection.execute(
            """
            SELECT
                id,
                planner,
                budget,
                created_at
            FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 100
            """,
            (user_id,),
        ).fetchall()

    return {
        "items": [
            dict(row)
            for row in rows
        ]
    }


@router.get(
    "/history/{recommendation_id}"
)
def history_detail(
    recommendation_id: int,
    request: Request,
):

    user_id = get_current_user_id(
        request
    )

    with get_conn() as connection:

        row = connection.execute(
            """
            SELECT *
            FROM recommendations
            WHERE id = ?
              AND user_id = ?
            """,
            (
                recommendation_id,
                user_id,
            ),
        ).fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found.",
        )

    item = dict(row)

    item["request"] = json.loads(
        item.pop("request_json")
    )

    item["response"] = json.loads(
        item.pop("response_json")
    )

    return item


@router.delete(
    "/history/{recommendation_id}"
)
def delete_history(
    recommendation_id: int,
    request: Request,
):

    user_id = get_current_user_id(
        request
    )

    with get_conn() as connection:

        cursor = connection.execute(
            """
            DELETE FROM recommendations
            WHERE id = ?
              AND user_id = ?
            """,
            (
                recommendation_id,
                user_id,
            ),
        )

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found.",
        )

    return {
        "message": "History item deleted."
    }
