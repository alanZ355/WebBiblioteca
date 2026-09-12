import json
import math

from config import BOOKS_FILE


def load_books():
    """Lee data/books.json y devuelve la lista de libros."""
    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_books(books):
    """Guarda la lista de libros en data/books.json."""
    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            books,
            file,
            indent=2,
            ensure_ascii=False
        )


def next_book_id(books):
    """Devuelve el próximo ID disponible."""

    if not books:
        return 1

    ids = [
        book["id"]
        for book in books
        if isinstance(book.get("id"), int)
    ]

    if not ids:
        return 1

    return max(ids) + 1


def validate_book_data(title, author, price):
    """
    Valida los datos mínimos necesarios para crear un libro.

    Devuelve:
        None si los datos son válidos.
        Un mensaje de error si hay algún problema.
    """

    if not title:
        return "El título es obligatorio."

    if not author:
        return "El autor es obligatorio."

    if price is None:
        return "El precio es obligatorio."
    
    if not math.isfinite(price):
        return "El precio debe ser un número válido."

    if price <= 0:
        return "El precio debe ser mayor a Cero."

    return None


def create_book(
    books,
    title,
    author,
    category,
    price,
    book_format,
    cover,
    featured
):
    """
    Valida y crea un nuevo libro.

    Devuelve:
        (libro, None) si todo está correcto.
        (None, mensaje_error) si hay un problema.
    """

    error = validate_book_data(
        title,
        author,
        price
    )

    if error:
        return None, error

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

    return new_book, None