"""Small, reusable input-validation and helper utilities.

Centralising these here keeps the menu functions in ``inventory.py`` and
``sales.py`` focused on *flow*, while the fiddly bits (parsing a float
safely, generating the next product code, parsing either date format the
user might type) live in one tested place.
"""

from __future__ import annotations

from datetime import date, datetime


def read_float(prompt: str, allow_blank: bool = False) -> float | None:
    """Prompt until the user enters a non-negative number (or blanks out).

    Returns ``None`` only when ``allow_blank`` is True and the user pressed
    Enter with no input - used for "skip this field" flows.
    """
    while True:
        raw = input(prompt).strip()
        if not raw and allow_blank:
            return None
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value < 0:
            print("Value cannot be negative.")
            continue
        return value


def generate_unique_code(existing_codes: list[str], prefix: str, width: int = 3) -> str:
    """Generate the next sequential code for a given prefix.

    e.g. with existing codes ["R001", "R002"] and prefix "R" this returns
    "R003". Non-numeric or foreign-prefix codes are ignored when scanning
    for the highest existing number, so mixed-prefix inventories
    (R001, ADD001, B001, ...) stay independent of each other.
    """
    highest = 0
    for code in existing_codes:
        if not code.upper().startswith(prefix.upper()):
            continue
        suffix = code[len(prefix):]
        if suffix.isdigit():
            highest = max(highest, int(suffix))
    return f"{prefix.upper()}{highest + 1:0{width}d}"


def generate_order_id(existing_order_ids: list[str], today: date | None = None) -> str:
    """Generate the next order ID in the format ``BBO-YY-XXXX``.

    The sequence resets implicitly whenever the two-digit year changes,
    since it only counts existing IDs that already carry the current year.
    """
    today = today or date.today()
    year_suffix = f"{today.year % 100:02d}"
    prefix = f"BBO-{year_suffix}-"

    highest = 0
    for order_id in existing_order_ids:
        if order_id.startswith(prefix) and order_id[len(prefix):].isdigit():
            highest = max(highest, int(order_id[len(prefix):]))
    return f"{prefix}{highest + 1:04d}"


def parse_delivery_date(raw: str, today: date | None = None) -> date | None:
    """Parse a delivery date given as ``DD-MM-YYYY`` or ``YYYY-MM-DD``.

    Returns ``None`` if the text doesn't match either format.
    """
    for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw.strip(), fmt).date()
        except ValueError:
            continue
    return None


def is_weekend(day: date) -> bool:
    """True for Saturday/Sunday - used to apply the weekend delivery surcharge."""
    return day.weekday() >= 5  # Monday=0 ... Sunday=6


def is_valid_name(text: str) -> bool:
    """A "name" field must be non-empty once whitespace is stripped."""
    return bool(text.strip())
