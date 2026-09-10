from flask import Flask, jsonify, render_template

app = Flask(__name__)

BOOKS = [
	{
		"id": 1,
		"title": "La sombra del viento",
		"author": "Carlos Ruiz Zafón",
		"category": "Novela",
		"price": 18.90,
		"format": "Tapa blanda",
		"cover": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=600&q=85",
		"featured": True,
	},
	{
		"id": 2,
		"title": "Hábitos atómicos",
		"author": "James Clear",
		"category": "Crecimiento",
		"price": 21.50,
		"format": "Tapa dura",
		"cover": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=600&q=85",
		"featured": True,
	},
	{
		"id": 3,
		"title": "El infinito en un junco",
		"author": "Irene Vallejo",
		"category": "Historia",
		"price": 24.00,
		"format": "Tapa blanda",
		"cover": "https://images.unsplash.com/photo-1511108690759-009324a90311?auto=format&fit=crop&w=600&q=85",
		"featured": True,
	},
	{
		"id": 4,
		"title": "Breves respuestas a las grandes preguntas",
		"author": "Stephen Hawking",
		"category": "Ciencia",
		"price": 16.75,
		"format": "Tapa blanda",
		"cover": "https://images.unsplash.com/photo-1532012197267-da84d127e765?auto=format&fit=crop&w=600&q=85",
		"featured": False,
	},
	{
		"id": 5,
		"title": "El camino del artista",
		"author": "Julia Cameron",
		"category": "Crecimiento",
		"price": 19.95,
		"format": "Tapa blanda",
		"cover": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=600&q=85",
		"featured": False,
	},
	{
		"id": 6,
		"title": "Cien años de soledad",
		"author": "Gabriel García Márquez",
		"category": "Clásicos",
		"price": 17.80,
		"format": "Edición especial",
		"cover": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?auto=format&fit=crop&w=600&q=85",
		"featured": False,
	},
]


@app.route("/")
def home():
	return render_template("index.html", books=BOOKS)


@app.route("/api/books")
def books():
	return jsonify(BOOKS)


if __name__ == "__main__":
	app.run(debug=True)
