from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from config import ADMIN_USERNAME, ADMIN_PASSWORD_HASH


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # Comprobamos que el usuario y la contraseña sean correctos.
    if (
        username == ADMIN_USERNAME
        and ADMIN_PASSWORD_HASH
        and check_password_hash(
            ADMIN_PASSWORD_HASH,
            password
        )
    ):
        # Guardamos el usuario en la sesión.
        session["user_id"] = username
        return redirect(url_for("admin.admin_panel"))
    
    # Si las credenciales son incorrectas,
    # volvemos al login mostrando un mensaje.
    return render_template(
        "login.html",
        error="Usuario o contraseña incorrectos."
    )


@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    session.pop("user_id", None)

    return redirect(url_for("public.home"))