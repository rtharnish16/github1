# Design Notes

## Purpose

Beautiful Blooms is a console application that automates the day-to-day
operations of a small flower shop: tracking product/add-on inventory and
running the customer order workflow from selection to delivery.

## Main components

| Module | Responsibility |
|---|---|
| `models.py` | Plain data classes: `Product`, `Addon`, `Order` |
| `file_handler.py` | Load/save each model to its plain-text file |
| `validators.py` | Input parsing/validation, code + order ID generation, date/weekend helpers |
| `inventory.py` | Inventory Management menu: view/update/add blooms and add-ons |
| `sales.py` | Sales Management menu: browse products, create orders, track order status |
| `main.py` | Program entry point and top-level menu loop |

## Data flow

1. On startup, `main.py` loads all products, add-ons, and orders from the
   `data/` text files into memory (as lists of dataclass instances).
2. Every menu action mutates those in-memory lists directly, then calls the
   matching `save_*` function so the change is written back to disk before
   the next prompt is shown. There's no separate "save" step for the user —
   every confirmed action persists immediately.
3. On exit, no extra shutdown step is needed: every mutation was already
   flushed to disk when it happened.

## Key design decisions

- **Plain text over a database.** Three human-readable, comma-separated
  files are enough for this scale, keep the project dependency-free, and
  are easy to inspect/edit directly while testing.
- **Free-text fields are escaped, not rejected.** A customer name or
  delivery message containing a comma has its commas swapped for
  semicolons before being written, rather than being rejected outright —
  simpler than a full CSV/quoting implementation while still keeping the
  file format unambiguous to re-parse.
- **Fee calculation is a pure function.** `calculate_delivery_fee()` in
  `sales.py` takes plain values in and returns a number — no `input()`
  calls — so the pricing rules (flat delivery fee, same-day surcharge,
  weekend surcharge) can be unit tested directly instead of only through
  a scripted terminal session.
- **Order status transitions are explicit.** `modify_order()` only allows
  the transitions described in the project spec (e.g. a `Closed` order can
  never be changed), instead of letting any status be set directly.
