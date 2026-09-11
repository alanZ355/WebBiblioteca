from pathlib import Path

BASE_DIR = Path(__file__).parent

BOOKS_FILE = BASE_DIR / "data" / "books.json"

SECRET_KEY = "cambiar-esta-clave-en-produccion"