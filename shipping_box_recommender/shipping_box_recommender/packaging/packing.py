
from itertools import permutations
from .models import Box


def get_orientations(product):
    dimensions = (
        float(product.length),
        float(product.width),
        float(product.height)
    )
    return set(permutations(dimensions))


def overlaps(a, b):
    return (
        a["x"] < b["x"] + b["length"]
        and a["x"] + a["length"] > b["x"]
        and a["y"] < b["y"] + b["width"]
        and a["y"] + a["width"] > b["y"]
        and a["z"] < b["z"] + b["height"]
        and a["z"] + a["height"] > b["z"]
    )


def try_place(product, box, placed_items, current_weight):
    length = float(box.length)
    width = float(box.width)
    height = float(box.height)
    max_weight = float(box.max_weight)

    product_weight = float(product.weight)

    if current_weight + product_weight > max_weight:
        return None

    # Try every possible product rotation
    orientations = sorted(
        get_orientations(product),
        reverse=True
    )

    # Try positions beside and above already placed products
    x_positions = {0}
    y_positions = {0}
    z_positions = {0}

    for item in placed_items:
        x_positions.add(item["x"] + item["length"])
        y_positions.add(item["y"] + item["width"])
        z_positions.add(item["z"] + item["height"])

    for x in sorted(x_positions):
        for y in sorted(y_positions):
            for z in sorted(z_positions):
                for l, w, h in orientations:

                    if x + l > length:
                        continue
                    if y + w > width:
                        continue
                    if z + h > height:
                        continue

                    new_item = {
                        "product": product.name,
                        "length": l,
                        "width": w,
                        "height": h,
                        "weight": product_weight,
                        "x": x,
                        "y": y,
                        "z": z
                    }

                    if not any(
                        overlaps(new_item, old_item)
                        for old_item in placed_items
                    ):
                        return new_item

    return None


def calculate_packing(order):
    order_items = list(order.items.select_related("product"))

    # Expand quantities into individual products
    products = []

    for item in order_items:
        for _ in range(item.quantity):
            product = item.product

            if any(
                value is None
                for value in (
                    product.length,
                    product.width,
                    product.height,
                    product.weight
                )
            ):
                raise ValueError(
                    f"Dimensions or weight missing for {product.name}"
                )

            products.append(product)

    # Place larger products first
    products.sort(
        key=lambda p: (
            float(p.length) * float(p.width) * float(p.height)
        ),
        reverse=True
    )

    available_boxes = list(Box.objects.all().order_by("cost"))

    if not available_boxes:
        raise ValueError("No shipping boxes are available.")

    # First, try to fit the entire order into one box
    for box in available_boxes:
        placed = []
        total_weight = 0
        success = True

        for product in products:
            position = try_place(
                product, box, placed, total_weight
            )

            if position is None:
                success = False
                break

            placed.append(position)
            total_weight += float(product.weight)

        if success:
            return [{
                "box": box,
                "items": placed,
                "total_weight": total_weight
            }]

    # If one box cannot fit everything, use multiple boxes
    packed_boxes = []

    for product in products:
        placed_successfully = False

        # Try to use space in boxes already opened
        for packed_box in packed_boxes:
            position = try_place(
                product,
                packed_box["box"],
                packed_box["items"],
                packed_box["total_weight"]
            )

            if position is not None:
                packed_box["items"].append(position)
                packed_box["total_weight"] += float(product.weight)
                placed_successfully = True
                break

        if placed_successfully:
            continue

        # Open the cheapest box that can hold this product
        for box in available_boxes:
            position = try_place(product, box, [], 0)

            if position is not None:
                packed_boxes.append({
                    "box": box,
                    "items": [position],
                    "total_weight": float(product.weight)
                })
                placed_successfully = True
                break

        if not placed_successfully:
            raise ValueError(
                f"No available box can fit {product.name}."
            )

    return packed_boxes
