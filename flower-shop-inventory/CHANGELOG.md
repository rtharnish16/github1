# Changelog

## [1.0.1]

### Changed
- Sales flow now retries on invalid input instead of silently defaulting:
  pickup/delivery choice, delivery address, same-day choice, and add-on
  code all re-prompt with an error message until a valid value is given.

## [1.0.0] - Initial Release

### Added
- Inventory management for blooms and add-ons (view, update, add)
- Sales workflow: browse/filter/sort products, create orders, add-ons
- Delivery fee calculator (flat rate, same-day surcharge, weekend surcharge)
- Order tracking with status transitions (Open, Preparing, Ready, Closed, Cancelled)
- Auto-generated product, add-on, and order IDs
- Plain-text file persistence (`products.txt`, `addons.txt`, `orders.txt`)
- Input validation across all menus
- Automated test suite (pytest) for validators, file handling, and business logic
