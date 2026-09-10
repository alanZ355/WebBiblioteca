"""
app.py — Backend de la librería web "Verso".

Qué cambió respecto a la versión original:
1. Los libros ya NO están hardcodeados acá. Viven en data/books.json,
   y este archivo tiene funciones para leerlos y escribirlos.
2. Hay una ruta /admin para agregar libros nuevos llenando un formulario,
   sin tener que tocar código ni el JSON a mano.
3. El carrito de compras se guarda en la sesión de Flask (server-side),
   así que si el usuario refresca la página, el carrito sigue ahí.

Ojo: /admin no tiene login ni contraseña. Es un panel simple pensado
para uso personal/local. Si en algún momento publicás el sitio en internet
para que lo vea cualquiera, conviene agregarle autenticación antes.
"""

import json
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)

# La sesión de Flask necesita una "secret_key" para poder firmar la cookie
# donde se guarda el carrito. Es un valor fijo para desarrollo local;
# si esto se despliega en producción, esta clave debería salir de una
# variable de entorno (por ejemplo os.environ["SECRET_KEY"]) y no
# quedar escrita en el código.
app.secret_key = "cambiar-esta-clave-en-produccion"

# Ruta al archivo donde vivven los libros. Path(__file__).parent apunta
# a la carpeta donde está este mismo app.py, así el programa funciona
# sin importar desde qué directorio lo ejecutes.
BOOKS_FILE = Path(__file__).parent / "data" / "books.json"


# ---------------------------------------------------------------------------
# Funciones para leer y guardar los libros en el archivo JSON
# ---------------------------------------------------------------------------

def load_books():
    """Lee data/books.json y devuelve la lista de libros como diccionarios."""
    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_books(books):
    """Escribe la lista de libros de vuelta en data/books.json.

    indent=2 es solo para que el archivo quede prolijo y legible si lo
    abrís a mano; ensure_ascii=False evita que las tildes/eñes se guarden
    como \\u00e1 en vez de "á".
    """
    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=2, ensure_ascii=False)


def next_book_id(books):
    """Calcula el próximo id disponible (el mayor id actual + 1).

    Si la lista está vacía, arranca en 1.
    """
    if not books:
        return 1
    return max(book["id"] for book in books) + 1


# ---------------------------------------------------------------------------
# Funciones para trabajar con el carrito guardado en la sesión
# ---------------------------------------------------------------------------
# El carrito se guarda en session["cart"] como un diccionario:
#   { "1": 2, "3": 1 }
# donde la clave es el id del libro (como texto, porque las claves de
# session/JSON siempre son strings) y el valor es la cantidad.

def get_cart_dict():
    """Devuelve el carrito guardado en la sesión (o uno vacío si no hay)."""
    return session.get("cart", {})


def cart_to_response(books):
    """Arma la respuesta que el frontend necesita para dibujar el carrito:
    una lista de items (con los datos completos del libro + cantidad)
    y el total a pagar.
    """
    cart = get_cart_dict()
    # Diccionario id -> libro para buscar rápido los datos de cada libro.
    books_by_id = {book["id"]: book for book in books}

    items = []
    total = 0
    for book_id_str, quantity in cart.items():
        book = books_by_id.get(int(book_id_str))
        if not book:
            # Si el libro fue borrado del catálogo pero seguía en el
            # carrito de alguien, lo salteamos en vez de romper la página.
            continue
        items.append({"book": book, "quantity": quantity})
        total += book["price"] * quantity

    return {"items": items, "total": round(total, 2)}


# ---------------------------------------------------------------------------
# Rutas públicas del sitio
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Página principal: muestra el catálogo y el carrito ya cargado
    (por si el usuario ya tenía cosas agregadas de antes).
    """
    books = load_books()
    cart = cart_to_response(books)
    return render_template("index.html", books=books, cart=cart)


@app.route("/api/books")
def api_books():
    """Devuelve el catálogo completo en JSON (útil si en el futuro se
    quiere consumir desde otro frontend, una app móvil, etc.)."""
    return jsonify(load_books())


# ---------------------------------------------------------------------------
# API del carrito (todo lo que el JS del frontend llama con fetch)
# ---------------------------------------------------------------------------

@app.route("/api/cart", methods=["GET"])
def get_cart():
    """Devuelve el estado actual del carrito guardado en la sesión."""
    books = load_books()
    return jsonify(cart_to_response(books))


@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    """Suma 1 unidad de un libro al carrito.

    Espera un JSON del tipo {"id": 3} en el body del POST.
    """
    data = request.get_json(silent=True) or {}
    book_id = data.get("id")

    books = load_books()
    valid_ids = {book["id"] for book in books}
    if book_id not in valid_ids:
        # Si mandan un id que no existe, devolvemos error 400 en vez de
        # guardar basura en el carrito.
        return jsonify({"error": "Libro no encontrado"}), 400

    cart = get_cart_dict()
    key = str(book_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    # session.modified asegura que Flask guarde el cambio en la cookie,
    # necesario porque modificamos un diccionario "in place" antes de
    # reasignarlo (con la línea de arriba ya alcanza, pero lo dejamos
    # explícito para que quede claro por qué existe este patrón).
    session.modified = True

    return jsonify(cart_to_response(books))


@app.route("/api/cart/remove", methods=["POST"])
def remove_from_cart():
    """Resta 1 unidad de un libro del carrito (y lo saca del todo si
    llega a 0). Espera un JSON del tipo {"id": 3}.
    """
    data = request.get_json(silent=True) or {}
    book_id = data.get("id")
    key = str(book_id)

    cart = get_cart_dict()
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]
        session["cart"] = cart
        session.modified = True

    books = load_books()
    return jsonify(cart_to_response(books))


# ---------------------------------------------------------------------------
# Panel de administración: agregar libros sin tocar código
# ---------------------------------------------------------------------------

@app.route("/admin", methods=["GET"])
def admin_panel():
    """Muestra el panel admin: la lista de libros actuales + el
    formulario para cargar uno nuevo.
    """
    books = load_books()
    return render_template("admin.html", books=books)


@app.route("/admin/books", methods=["POST"])
def admin_add_book():
    """Recibe el formulario del panel admin y agrega un libro nuevo
    al archivo data/books.json.
    """
    books = load_books()

    # request.form son los datos que vienen del <form> en admin.html.
    # .strip() saca espacios de más al principio/final de lo que escriba
    # el usuario.
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    category = request.form.get("category", "").strip()
    price_raw = request.form.get("price", "").strip()
    book_format = request.form.get("format", "").strip()
    cover = request.form.get("cover", "").strip()
    featured = request.form.get("featured") == "on"  # checkbox tildado o no

    # Validación básica: si falta algo importante, volvemos al admin
    # sin guardar nada. (Para un formulario más prolijo se podría mostrar
    # un mensaje de error, pero esto ya evita libros "rotos".)
    if not title or not author or not price_raw:
        return redirect(url_for("admin_panel"))

    try:
        price = float(price_raw)
    except ValueError:
        return redirect(url_for("admin_panel"))

    new_book = {
        "id": next_book_id(books),
        "title": title,
        "author": author,
        "category": category or "Sin categoría",
        "price": price,
        "format": book_format or "Tapa blanda",
        "cover": cover or "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=600&q=85",
        "featured": featured,
    }

    books.append(new_book)
    save_books(books)

    return redirect(url_for("admin_panel"))


@app.route("/admin/books/<int:book_id>/delete", methods=["POST"])
def admin_delete_book(book_id):
    """Elimina un libro del catálogo por su id, desde el panel admin."""
    books = load_books()
    books = [book for book in books if book["id"] != book_id]
    save_books(books)
    return redirect(url_for("admin_panel"))


if __name__ == "__main__":
    # debug=True es cómodo para programar (recarga sola y muestra errores
    # detallados), pero NUNCA debe usarse así si el sitio queda accesible
    # desde internet: expone información sensible del servidor.
    app.run(debug=True)
