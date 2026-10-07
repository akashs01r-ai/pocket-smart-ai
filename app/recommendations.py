from typing import Any

from .ai import gemini_service
from .catalog import get_catalog


def _budget_items(
    items,
    budget: float,
    count: int = 5,
):
    return sorted(
        items,
        key=lambda item: item.price,
    )[:count]


def _item_dict(
    item,
    score: float = 0.85,
):
    return {
        "name": item.name,
        "provider": item.provider,
        "price": item.price,
        "description": item.description,
        "url": item.url,
        "match_score": round(
            score,
            2,
        ),
    }


def _usable_ai_result(
    result: Any,
    require_allocation: bool = False,
) -> bool:
    if not isinstance(result, dict):
        return False

    recommendations = result.get(
        "recommendations"
    )

    required_item_fields = {
        "name",
        "provider",
        "price",
        "description",
        "url",
    }

    if (
        not isinstance(recommendations, list)
        or not recommendations
        or any(
            not isinstance(item, dict)
            or not required_item_fields.issubset(item)
            for item in recommendations
        )
    ):
        return False

    if require_allocation:
        allocation = result.get("allocation")

        required_allocation_fields = {
            "category",
            "amount",
        }

        if (
            not isinstance(allocation, list)
            or not allocation
            or any(
                not isinstance(item, dict)
                or not required_allocation_fields.issubset(item)
                for item in allocation
            )
        ):
            return False

    return True


def local_home(
    data: dict[str, Any],
) -> dict[str, Any]:

    budget = data["budget"]

    items = _budget_items(
        get_catalog("home"),
        budget,
    )

    selected = [
        item
        for item in items
        if item.price <= budget
    ]

    if not selected:
        selected = items[:3]

    return {
        "planner": "home",

        "title": "Home Interior Budget Plan",

        "summary": (
            f"Starter recommendations for a "
            f"{data['style']} style within "
            f"₹{budget:,.0f}."
        ),

        "budget": budget,

        "allocation": [
            {
                "category": "Lighting",
                "amount": round(
                    budget * 0.18,
                    2,
                ),
            },
            {
                "category": "Furniture",
                "amount": round(
                    budget * 0.42,
                    2,
                ),
            },
            {
                "category": "Decor",
                "amount": round(
                    budget * 0.20,
                    2,
                ),
            },
            {
                "category": "Contingency",
                "amount": round(
                    budget * 0.20,
                    2,
                ),
            },
        ],

        "recommendations": [
            _item_dict(item)
            for item in selected
        ],

        "source_mode": "local_catalog",
    }


def local_party(
    data: dict[str, Any],
) -> dict[str, Any]:

    budget = data["budget"]

    guests = data["guests"]

    food_budget = budget * 0.50

    decoration_budget = budget * 0.20

    venue_budget = budget * 0.20

    contingency = budget * 0.10

    food_per_person = (
        food_budget / guests
    )

    party_items = get_catalog(
        "party"
    )

    suitable = [
        _item_dict(item)
        for item in party_items
    ]

    return {
        "planner": "party",

        "title": (
            f"{data['event_type']} "
            f"Party Budget Plan"
        ),

        "summary": (
            f"Indicative allocation for "
            f"{guests} guests in "
            f"{data['city']}."
        ),

        "budget": budget,

        "allocation": [
            {
                "category": "Food & Catering",
                "amount": round(
                    food_budget,
                    2,
                ),
            },
            {
                "category": "Decoration",
                "amount": round(
                    decoration_budget,
                    2,
                ),
            },
            {
                "category": "Venue",
                "amount": round(
                    venue_budget,
                    2,
                ),
            },
            {
                "category": "Contingency",
                "amount": round(
                    contingency,
                    2,
                ),
            },
        ],

        "per_guest_food_budget": round(
            food_per_person,
            2,
        ),

        "recommendations": suitable[:5],

        "source_mode": "local_catalog",
    }


def local_jewelry(
    data: dict[str, Any],
    image_analyzed: bool = False,
) -> dict[str, Any]:

    budget = data["budget"]

    items = _budget_items(
        get_catalog("jewelry"),
        budget,
    )

    selected = [
        item
        for item in items
        if item.price <= budget
    ]

    if not selected:
        selected = items[:3]

    return {
        "planner": "jewelry",

        "title": "Occasion Jewelry Recommendations",

        "summary": (
            f"Jewelry ideas for a "
            f"{data['occasion']} occasion "
            f"with an {data['style']} preference."
        ),

        "budget": budget,

        "image_analyzed": image_analyzed,

        "recommendations": [
            _item_dict(item)
            for item in selected
        ],

        "style_notes": [
            "Keep the jewelry silhouette proportional to the outfit neckline.",

            "Use one statement piece and keep the remaining pieces simpler.",

            "Treat marketplace prices as indicative until verified on the provider site.",
        ],

        "source_mode": "local_catalog",
    }


def generate_home(
    data: dict[str, Any],
) -> dict[str, Any]:

    prompt = f"""
You are PocketSmart AI's Home Interior Planner.

Create a practical budget-aware home interior recommendation.

User data:
{data}

Return a JSON object.

Required keys:

planner
title
summary
budget
allocation
recommendations
source_mode

recommendations must contain:

name
provider
price
description
url
match_score

Do not claim live marketplace inventory.
Do not invent that you accessed a retailer's private API.
Treat prices as indicative.
"""

    result = gemini_service.generate_json(
        prompt
    )

    if _usable_ai_result(
        result,
        require_allocation=True,
    ):
        return result

    return local_home(data)


def generate_party(
    data: dict[str, Any],
) -> dict[str, Any]:

    prompt = f"""
You are PocketSmart AI's Party Planner.

Create a practical party budget plan.

User data:
{data}

Return JSON with:

planner
title
summary
budget
allocation
per_guest_food_budget
recommendations
source_mode

Recommendations must contain:

name
provider
price
description
url
match_score

Do not claim live inventory or live prices.
"""

    result = gemini_service.generate_json(
        prompt
    )

    if _usable_ai_result(
        result,
        require_allocation=True,
    ):
        return result

    return local_party(data)


def generate_jewelry(
    data: dict[str, Any],
    image_bytes: bytes | None = None,
    mime_type: str | None = None,
) -> dict[str, Any]:

    prompt = f"""
You are PocketSmart AI's Jewelry Planner.

Recommend jewelry based on:

{data}

If an outfit image is supplied, analyze only
broad visual styling cues such as:

- colors
- patterns
- neckline
- silhouette
- general style

Do not identify the person.
Do not infer sensitive personal characteristics.

Return JSON with:

planner
title
summary
budget
image_analyzed
recommendations
style_notes
source_mode

Recommendations must contain:

name
provider
price
description
url
match_score

Do not claim live prices or inventory.
"""

    result = gemini_service.generate_json(
        prompt,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )

    if _usable_ai_result(result):
        return result

    return local_jewelry(
        data,
        image_analyzed=bool(image_bytes),
    )
