from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    category: str
    name: str
    provider: str
    price: float
    description: str
    url: str


CATALOG = [

    # -------------------------
    # HOME
    # -------------------------

    Item(
        "home",
        "Minimal Pendant Light",
        "IKEA",
        2499,
        "Warm modern pendant light for living or dining areas.",
        "https://www.ikea.com/",
    ),

    Item(
        "home",
        "Compact Ceiling Fan",
        "Amazon",
        3299,
        "Energy-efficient ceiling fan for bedrooms and living rooms.",
        "https://www.amazon.in/",
    ),

    Item(
        "home",
        "Oak-look Side Table",
        "IKEA",
        3999,
        "Compact side table with a warm wood appearance.",
        "https://www.ikea.com/",
    ),

    Item(
        "home",
        "Ergonomic Study Chair",
        "Amazon",
        5499,
        "Supportive chair suitable for a home office or study area.",
        "https://www.amazon.in/",
    ),

    Item(
        "home",
        "Modern Wall Art Set",
        "Amazon",
        1799,
        "Three-piece decorative wall art set.",
        "https://www.amazon.in/",
    ),

    Item(
        "home",
        "4-Seater Dining Table",
        "IKEA",
        12999,
        "Space-conscious dining table for apartments.",
        "https://www.ikea.com/",
    ),

    # -------------------------
    # PARTY
    # -------------------------

    Item(
        "party",
        "Vegetarian Catering Package",
        "Zomato",
        450,
        "Indicative per-person catering package.",
        "https://www.zomato.com/",
    ),

    Item(
        "party",
        "Party Food Delivery Package",
        "Swiggy",
        400,
        "Indicative per-person food package.",
        "https://www.swiggy.com/",
    ),

    Item(
        "party",
        "Birthday Decoration Package",
        "Local Vendor",
        4500,
        "Indicative balloon, backdrop and table decoration package.",
        "#",
    ),

    Item(
        "party",
        "Budget Event Venue",
        "OYO",
        7000,
        "Indicative small-event venue budget.",
        "https://www.oyorooms.com/",
    ),

    Item(
        "party",
        "Premium Event Venue",
        "OYO",
        14000,
        "Indicative larger event venue budget.",
        "https://www.oyorooms.com/",
    ),

    # -------------------------
    # JEWELRY
    # -------------------------

    Item(
        "jewelry",
        "Pearl Drop Earrings",
        "Amazon",
        1299,
        "Classic pearl-style earrings for elegant occasions.",
        "https://www.amazon.in/",
    ),

    Item(
        "jewelry",
        "Minimal Gold-tone Necklace",
        "Flipkart",
        1799,
        "Delicate necklace suitable for formal and festive styling.",
        "https://www.flipkart.com/",
    ),

    Item(
        "jewelry",
        "Kundan-inspired Set",
        "Amazon",
        3499,
        "Statement set suited to festive and wedding styling.",
        "https://www.amazon.in/",
    ),

    Item(
        "jewelry",
        "Silver-tone Bracelet",
        "Flipkart",
        999,
        "Simple bracelet for understated looks.",
        "https://www.flipkart.com/",
    ),
]


def get_catalog(
    category: str,
) -> list[Item]:
    return [
        item
        for item in CATALOG
        if item.category == category
    ]