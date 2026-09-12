from flask import Flask

from config import SECRET_KEY

from routes.public import public_bp
from routes.cart import cart_bp
from routes.admin import admin_bp
from routes.auth import auth_bp

app = Flask(__name__)

app.secret_key = SECRET_KEY


app.register_blueprint(public_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)