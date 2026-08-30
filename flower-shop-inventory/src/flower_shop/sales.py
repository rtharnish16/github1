"""Sales Management: browsing products, creating orders, and order tracking."""

from __future__ import annotations

from .file_handler import save_orders
from .inventory import find_addon_by_code, find_product_by_code
from .models import Addon, Order, Product
from .validators import generate_order_id, is_valid_name, is_weekend, parse_delivery_date

PICKUP_FEE = 0.0
DELIVERY_FEE = 35.0
SAME_DAY_SURCHARGE = 35.0
WEEKEND_SURCHARGE = 10.0

ORDER_STATUSES = ["Open", "Preparing", "Ready", "Closed", "Cancelled"]


def calculate_delivery_fee(delivery_type: str, same_day: str, delivery_date) -> float:
    """Pure fee calculation, kept separate from I/O so it's easy to unit test.

    Rules (from the project spec): Pickup is free; Delivery is a flat $35;
    same-day delivery adds a further $35; a weekend delivery date adds $10.
    """
    if delivery_type != "Delivery":
        return PICKUP_FEE

    fee = DELIVERY_FEE
    if same_day == "Y":
        fee += SAME_DAY_SURCHARGE
    if delivery_date is not None and is_weekend(delivery_date):
        fee += WEEKEND_SURCHARGE
    return fee


def sales_menu(products: list[Product], addons: list[Addon], orders: list[Order]) -> None:
    """Top-level Sales Management menu (Main Menu option 2)."""
    while True:
        print("\n==== Sales Management ====")
        print("1. Create Order")
        print("2. View Orders")
        print("3. Back to Main Menu")
        choice = input("Enter option: ").strip()

        if choice == "1":
            create_order(products, addons, orders)
        elif choice == "2":
            view_orders(orders)
        elif choice == "3":
            return
        else:
            print("Invalid option. Try again.")


def _print_product_list(products: list[Product]) -> None:
    print("\n--- Product List ---")
    if not products:
        print("(No products available.)")
        return
    print(f"{'Code':<8}{'Name':<25}{'Category':<15}{'Price':<9}{'Status':<12}")
    for p in products:
        print(f"{p.code:<8}{p.name:<25}{p.category:<15}${p.price:<8.2f}{p.status:<12}")


def create_order(products: list[Product], addons: list[Addon], orders: list[Order]) -> None:
    """Create Order flow: browse (filter/sort optional), pick add-on, deliver, confirm."""
    available = [p for p in products if p.is_available]

    while True:
        _print_product_list(available)
        print("\nOptions:")
        print("1. Filter products by category")
        print("2. Sort products by price")
        print("3. Order item")
        print("4. Back to Sales Menu")
        opt = input("Enter option: ").strip()

        if opt == "1":
            category = input("Enter category to filter by: ").strip().lower()
            available = [p for p in available if p.category.lower() == category]
            if not available:
                print("No products found in that category. Showing full list again.")
                available = [p for p in products if p.is_available]
        elif opt == "2":
            available = sorted(available, key=lambda p: p.price)
        elif opt == "3":
            _handle_new_order(available, addons, orders, products)
            return
        elif opt == "4":
            return
        else:
            print("Invalid option. Try again.")


def _handle_new_order(
    available: list[Product], addons: list[Addon], orders: list[Order], all_products: list[Product]
) -> None:
    code = input("Enter product item code: ").strip()
    product = find_product_by_code(available, code)
    if not product or not product.is_available:
        print("Invalid or unavailable product code. Order cancelled.")
        return

    addon = _select_addon(addons)

    while True:
        customer_name = input("Enter customer name: ").strip()
        if is_valid_name(customer_name):
            break
        print("Customer name cannot be empty.")

    while True:
        recipient_name = input("Enter recipient name: ").strip()
        if is_valid_name(recipient_name):
            break
        print("Recipient name cannot be empty.")

    message = input("Enter message for recipient (max 300 chars): ").strip()[:300]

    while True:
        delivery_type_raw = input("Store pickup or Delivery? (S/D): ").strip().upper()
        if delivery_type_raw == "S":
            delivery_type = "Pickup"
            break
        if delivery_type_raw == "D":
            delivery_type = "Delivery"
            break
        print("Invalid choice. Please enter S for pickup or D for delivery.")

    address = ""
    delivery_date_str = ""
    same_day = "N"
    delivery_fee = PICKUP_FEE

    if delivery_type == "Delivery":
        while True:
            address = input("Enter delivery address: ").strip()
            if address:
                break
            print("Delivery address cannot be empty.")

        while True:
            delivery_date_str = input(
                "Enter delivery date (DD-MM-YYYY or YYYY-MM-DD): "
            ).strip()
            parsed_date = parse_delivery_date(delivery_date_str)
            if parsed_date:
                break
            print("Invalid date format. Please try again.")

        while True:
            same_day = input("Same day delivery? (Y/N): ").strip().upper()
            if same_day in ("Y", "N"):
                break
            print("Invalid choice. Please enter Y or N.")

        delivery_fee = calculate_delivery_fee(delivery_type, same_day, parsed_date)

    total = product.price + (addon.price if addon else 0) + delivery_fee

    print("\n---------- Order Summary ----------")
    print(f"Item: {product.name}({product.code})".ljust(28) + f"${product.price:.2f}")
    if addon:
        print(f"Addon: {addon.name}({addon.code})".ljust(28) + f"${addon.price:.2f}")
    else:
        print("Addon: None")
    if delivery_type == "Delivery":
        print(f"Delivery date: {delivery_date_str}")
        print(f"Same day delivery: {'Yes' if same_day == 'Y' else 'No'}")
    print("Delivery charges:".ljust(28) + f"${delivery_fee:.2f}")
    print("Total:".ljust(28) + f"${total:.2f}")

    choice = input(
        "\nEnter 1 to confirm, 2 to edit info, or 0 to cancel: "
    ).strip()

    if choice == "2":
        _handle_new_order(available, addons, orders, all_products)
        return
    if choice != "1":
        print("Order cancelled.")
        return

    order_id = generate_order_id([o.order_id for o in orders])
    order = Order(
        order_id=order_id,
        product_code=product.code,
        product_name=product.name,
        addon_code=addon.code if addon else "",
        addon_name=addon.name if addon else "",
        customer_name=customer_name,
        recipient_name=recipient_name,
        message=message,
        delivery_type=delivery_type,
        address=address,
        delivery_date=delivery_date_str,
        same_day=same_day,
        delivery_fee=delivery_fee,
        total=total,
        status="Open",
    )
    orders.append(order)
    save_orders(orders)
    print(f"Order saved successfully (ID: {order_id})")


def _select_addon(addons: list[Addon]) -> Addon | None:
    available_addons = [a for a in addons if a.is_available]
    if not available_addons:
        return None

    print("\nAvailable add-ons:")
    for a in available_addons:
        print(f"{a.code:<10}{a.name:<25}${a.price:.2f}")

    while True:
        code = input("Enter item code for add-on, or 0 to skip: ").strip()
        if code == "0" or not code:
            return None

        addon = find_addon_by_code(available_addons, code)
        if addon:
            return addon

        print("Invalid add-on code. Please try again.")


def view_orders(orders: list[Order]) -> None:
    """Sales Management option 2: edit/cancel orders or filter by status."""
    while True:
        print("\n--- View Orders ---")
        print("1. Edit / Cancel order")
        print("2. Filter orders by status")
        print("3. Back to Sales Menu")
        choice = input("Enter option: ").strip()

        if choice == "1":
            modify_order(orders)
        elif choice == "2":
            _filter_orders_by_status(orders)
        elif choice == "3":
            return
        else:
            print("Invalid option. Try again.")


def _filter_orders_by_status(orders: list[Order]) -> None:
    print("\nFilter by status:")
    for i, status in enumerate(ORDER_STATUSES, start=1):
        print(f"{i}. {status}")
    print(f"{len(ORDER_STATUSES) + 1}. Back")

    choice = input("Select option: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(ORDER_STATUSES)):
        return

    status = ORDER_STATUSES[int(choice) - 1]
    matching = [o for o in orders if o.status == status]

    print(f"\n--- Orders with status: {status} ---")
    if not matching:
        print("(No orders with this status.)")
        return
    for o in matching:
        addon_label = o.addon_name or "None"
        print(
            f"{o.order_id}  {o.product_name}  {addon_label}  "
            f"${o.total:.2f}  {o.status}  {o.delivery_date}"
        )


def modify_order(orders: list[Order]) -> None:
    """Edit/cancel a single order, enforcing valid status transitions:

    Open      -> Preparing / Cancelled
    Cancelled -> Open (reopen)
    Preparing -> Ready
    Ready     -> Preparing / Closed
    Closed    -> no further changes
    """
    order_id = input("Enter Order ID or 0 to go back: ").strip()
    if order_id == "0":
        return

    order = next((o for o in orders if o.order_id == order_id), None)
    if not order:
        print("Invalid ID.")
        return

    print(f"Current Status: {order.status}")

    if order.status == "Open":
        choice = input("Enter new status (Preparing/Cancelled): ").strip().title()
        if choice in ("Preparing", "Cancelled"):
            order.status = choice
        else:
            print("Invalid choice. No changes made.")
            return
    elif order.status == "Cancelled":
        choice = input("Set back to Open? (Y/N): ").strip().upper()
        if choice == "Y":
            order.status = "Open"
        else:
            print("No changes made.")
            return
    elif order.status == "Preparing":
        order.status = "Ready"
    elif order.status == "Ready":
        choice = input("Enter new status (Preparing/Closed): ").strip().title()
        if choice in ("Preparing", "Closed"):
            order.status = choice
        else:
            print("Invalid choice. No changes made.")
            return
    elif order.status == "Closed":
        print("This order is closed and cannot be modified.")
        return

    save_orders(orders)
    print("Order updated successfully.")
