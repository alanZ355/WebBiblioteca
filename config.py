import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

BOOKS_FILE = BASE_DIR / "data" / "books.json"

SECRET_KEY = os.environ.get("SECRET_KEY")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")

ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")