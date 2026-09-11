import json

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

    return max(book["id"] for book in books) + 1