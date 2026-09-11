from flask import session


def get_cart_dict():
    """Obtiene el carrito almacenado en la sesión."""
    return session.get("cart", {})


def cart_to_response(books):
    """Convierte el carrito en una respuesta lista para enviar al frontend."""

    cart = get_cart_dict()

    books_by_id = {
        book["id"]: book
        for book in books
    }

    items = []
    total = 0

    for book_id_str, quantity in cart.items():

        book = books_by_id.get(int(book_id_str))

        if not book:
            continue

        subtotal = book["price"] * quantity
        total += subtotal

        items.append({
            "book": book,
            "quantity": quantity,
            "subtotal": round(subtotal, 2),
        })

    return {
        "items": items,
        "total": round(total, 2),
    }