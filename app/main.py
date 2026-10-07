from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .auth import router as auth_router
from .config import get_settings
from .database import init_db
from .routes import router as api_router


BASE_DIR = Path(
    __file__
).resolve().parent.parent

settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "AI-powered budget and "
        "recommendation assistant."
    ),
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            BASE_DIR / "static"
        )
    ),
    name="static",
)


templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)


app.include_router(
    auth_router
)

app.include_router(
    api_router
)


@app.on_event("startup")
def startup():
    init_db()


@app.get(
    "/",
    include_in_schema=False,
)
def index(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": settings.app_name,
        },
    )


@app.get(
    "/planner/{planner}",
    include_in_schema=False,
)
def planner_page(
    request: Request,
    planner: str,
):

    allowed = {
        "home",
        "party",
        "jewelry",
    }

    if planner not in allowed:
        raise HTTPException(
            status_code=404,
            detail="Planner not found.",
        )

    return templates.TemplateResponse(
        request=request,
        name=f"{planner}.html",
        context={
            "title": (
                f"{planner.title()} Planner"
            ),
        },
    )


@app.get(
    "/login",
    include_in_schema=False,
)
def login_page(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "title": "Login",
        },
    )


@app.get(
    "/register",
    include_in_schema=False,
)
def register_page(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "title": "Register",
        },
    )


@app.get(
    "/dashboard",
    include_in_schema=False,
)
def dashboard(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "Dashboard",
        },
    )


@app.get(
    "/history",
    include_in_schema=False,
)
def history_page(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "title": "History",
        },
    )
