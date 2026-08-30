# User Guide

## Running the program

From the project root, with the three data files present under `data/`:

```bash
python -m src.flower_shop.main
```

## Main Menu

```
@@@@ Beautiful Blooms @@@@
1. Inventory Management
2. Sales Management
3. Exit
Enter option:
```

## Inventory Management

```
==== Inventory Management ====
1. View / Update Blooms
2. Add New Bloom
3. View / Update Add-ons
4. Add New Add-on
5. Back to Main Menu
```

- **View / Update Blooms** lists every product, then lets you enter an item
  code to update its price and/or status (or `0` to go back).
- **Add New Bloom** asks for a name, an optional code (auto-generated from a
  category prefix if left blank, e.g. `R003`), a price, and a category.
- **View / Update Add-ons** and **Add New Add-on** work the same way for
  add-ons (auto-generated codes look like `ADD004`).

## Sales Management

```
==== Sales Management ====
1. Create Order
2. View Orders
3. Back to Sales Menu
```

### Create Order

1. Browse the product list, optionally filtering by category or sorting by
   price, then choose **Order item**.
2. Enter the product code, then an optional add-on code (or `0` to skip).
3. Enter customer name, recipient name, and a short message.
4. Choose **Store pickup (S)** or **Delivery (D)**. Delivery additionally
   asks for an address, a delivery date, and whether it's same-day.
5. Review the order summary (product + add-on + delivery fee = total), then
   confirm (`1`), edit and re-enter (`2`), or cancel (`0`).

Delivery fees: pickup is free; delivery is a flat $35; same-day delivery adds
$35; a delivery date that falls on a weekend adds a further $10.

### View Orders

- **Edit / Cancel order**: enter an order ID to move it through its allowed
  status transitions (`Open → Preparing/Cancelled`, `Preparing → Ready`,
  `Ready → Preparing/Closed`, `Cancelled → Open`). Closed orders can't be
  changed.
- **Filter orders by status**: lists only the orders in the status you pick.

## Example session

```
--- Product List ---
Code    Name                     Category       Price    Status
R001    Angel Eyes               Romantic       $85.00   Available
...
Enter option: 3
Enter product item code: R001

Available add-ons:
ADD001    Chocolates               $8.00
Enter item code for add-on, or 0 to skip: ADD001
Enter customer name: Tony Lin
Enter recipient name: Linda Foo
Enter message for recipient (max 300 chars): I love you
Store pickup or Delivery? (S/D): D
Enter delivery address: 123 ABC Street
Enter delivery date (DD-MM-YYYY or YYYY-MM-DD): 28-08-2025
Same day delivery? (Y/N): N

---------- Order Summary ----------
Item: Angel Eyes(R001)      $85.00
Addon: Chocolates(ADD001)   $8.00
Delivery date: 28-08-2025
Same day delivery: No
Delivery charges:           $35.00
Total:                      $128.00

Enter 1 to confirm, 2 to edit info, or 0 to cancel: 1
Order saved successfully (ID: BBO-26-0001)
```
