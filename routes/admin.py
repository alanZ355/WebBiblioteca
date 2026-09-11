from flask import Blueprint, redirect, render_template, request, url_for

from services.books import load_books, save_books, next_book_id


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin", methods=["GET"])
def admin_panel():

    books = load_books()

    return render_template(
        "admin.html",
        books=books
    )


@admin_bp.route("/admin/books", methods=["POST"])
def create_book():

    books = load_books()

    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    category = request.form.get("category", "").strip()
    price_raw = request.form.get("price", "").strip()
    book_format = request.form.get("format", "").strip()
    cover = request.form.get("cover", "").strip()
    featured = request.form.get("featured") == "on"

    if not title or not author or not price_raw:
        return redirect(url_for("admin.admin_panel"))

    try:
        price = float(price_raw)
    except ValueError:
        return redirect(url_for("admin.admin_panel"))

    new_book = {
        "id": next_book_id(books),
        "title": title,
        "author": author,
        "category": category or "Sin categoría",
        "price": price,
        "format": book_format or "Tapa blanda",
        "cover": cover,
        "featured": featured,
    }

    books.append(new_book)

    save_books(books)

    return redirect(url_for("admin.admin_panel"))


@admin_bp.route(
    "/admin/books/<int:book_id>/delete",
    methods=["POST"]
)
def delete_book(book_id):

    books = load_books()

    books = [
        book
        for book in books
        if book["id"] != book_id
    ]

    save_books(books)

    return redirect(url_for("admin.admin_panel"))