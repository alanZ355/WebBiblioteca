from pathlib import Path


from werkzeug.utils import secure_filename

from config import (
    UPLOAD_FOLDER,
    ALLOWED_IMAGE_EXTENSIONS
)

def allowed_image(filename):
    """Devuelve True si la extensión de la imagen está permitida."""

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_IMAGE_EXTENSIONS

def save_book_image(image, book_id, image_type):
    """
    Guarda la portada de un libro.

    Devuelve:
        La ruta relativa de la imagen si se guardó correctamente.
        None si no se recibió una imagen válida.
    """

    if not image or not image.filename:
        return None

    if not allowed_image(image.filename):
        return None

    extension = Path(image.filename).suffix.lower()

    filename = f"book_{book_id}_{image_type}{extension}"

    filename = secure_filename(filename)

    UPLOAD_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    image.save(UPLOAD_FOLDER / filename)

    return f"images/books/{filename}"