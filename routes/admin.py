from flask import Blueprint, redirect, render_template, request, url_for, session

from services.books import load_books, save_books, create_book
from services.images import save_book_image

admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
def check_admin_auth():
    if "user_id" not in session:
        return redirect(url_for("public.home"))


@admin_bp.route("/admin", methods=["GET"])
def admin_panel():

    books = load_books()

    return render_template(
        "admin.html",
        books=books
    )


@admin_bp.route("/admin/books", methods=["POST"])
def create_book_route():

    books = load_books()

    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    category = request.form.get("category", "").strip()
    price_raw = request.form.get("price", "").strip()
    book_format = request.form.get("format", "").strip()
    cover = request.files.get("cover")
    back_cover = request.files.get("back_cover")
    featured = request.form.get("featured") == "on"
    description = request.form.get("description", "").strip()

    if not title or not author or not price_raw:
        return redirect(url_for("admin.admin_panel"))

    try:
        price = float(price_raw)
    except ValueError:
        return redirect(url_for("admin.admin_panel"))

    new_book, error = create_book(
        books,
        title,
        author,
        category,
        price,
        book_format,
        None,
        featured,
        description
    )
    if error:
        return redirect(url_for("admin.admin_panel"))
    
    cover_path = save_book_image(
        cover,
        new_book["id"],
        "cover"
    )
    
    new_book["cover"] = cover_path

    back_cover_path = save_book_image(
    back_cover,
    new_book["id"],
    "back_cover"
)

    new_book["back_cover"] = back_cover_path

    books.append(new_book)

    save_books(books)

    return redirect(url_for("admin.admin_panel"))


@admin_bp.route(
    "/admin/books/<int:book_id>/delete",
    methods=["POST"]
)
def delete_book_route(book_id):

    books = load_books()

    books = [
        book
        for book in books
        if book["id"] != book_id
    ]

    save_books(books)

    return redirect(url_for("admin.admin_panel"))