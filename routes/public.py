from flask import Blueprint, jsonify, render_template

from services.books import load_books
from services.cart import cart_to_response


public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():

    books = load_books()
    cart = cart_to_response(books)

    return render_template(
        "index.html",
        books=books,
        cart=cart
    )


@public_bp.route("/api/books")
def api_books():

    return jsonify(load_books())