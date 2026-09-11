from flask import Flask

from config import SECRET_KEY

from routes.public import public_bp
from routes.cart import cart_bp
from routes.admin import admin_bp


app = Flask(__name__)

app.secret_key = SECRET_KEY


app.register_blueprint(public_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    app.run(debug=True)