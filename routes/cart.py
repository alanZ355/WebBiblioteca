from flask import Blueprint, jsonify, request, session

from services.books import load_books
from services.cart import get_cart_dict, cart_to_response


cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/api/cart", methods=["GET"])
def get_cart():

    books = load_books()

    return jsonify(
        cart_to_response(books)
    )


@cart_bp.route("/api/cart/add", methods=["POST"])
def add_to_cart():

    data = request.get_json(silent=True) or {}

    book_id = data.get("id")

    books = load_books()

    valid_ids = {
        book["id"]
        for book in books
    }

    if book_id not in valid_ids:
        return jsonify({
            "error": "Libro no encontrado"
        }), 404

    cart = get_cart_dict()

    key = str(book_id)

    cart[key] = cart.get(key, 0) + 1

    session["cart"] = cart

    return jsonify(
        cart_to_response(books)
    )


@cart_bp.route("/api/cart/remove", methods=["POST"])
def remove_from_cart():

    data = request.get_json(silent=True) or {}

    book_id = data.get("id")

    cart = get_cart_dict()

    key = str(book_id)

    if key in cart:

        cart[key] -= 1

        if cart[key] <= 0:
            del cart[key]

    session["cart"] = cart

    books = load_books()

    return jsonify(
        cart_to_response(books)
    )