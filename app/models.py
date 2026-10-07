from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class RegisterRequest(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=80,
    )

    email: str = Field(
        min_length=5,
        max_length=160,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("email")
    @classmethod
    def normalize_email(
        cls,
        value: str,
    ) -> str:
        return value.strip().lower()


class LoginRequest(BaseModel):
    email: str

    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(
        cls,
        value: str,
    ) -> str:
        return value.strip().lower()


class HomeRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    style: str = Field(
        default="Modern",
        max_length=80,
    )

    rooms: list[str] = Field(
        min_length=1,
    )

    quantities: dict[str, int] = Field(
        default_factory=dict,
    )


class PartyRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    guests: int = Field(
        gt=0,
        le=10_000,
    )

    event_type: str = Field(
        default="Birthday",
        max_length=80,
    )

    venue_preference: str = Field(
        default="Flexible",
        max_length=120,
    )

    city: str = Field(
        default="Chennai",
        max_length=100,
    )


class JewelryRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000,
    )

    occasion: str = Field(
        default="Wedding",
        max_length=80,
    )

    style: str = Field(
        default="Elegant",
        max_length=100,
    )

    outfit_notes: str = Field(
        default="",
        max_length=500,
    )