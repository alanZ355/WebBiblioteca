from flask import Blueprint, render_template, request, redirect, url_for, session


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # Por ahora solamente mostramos qué recibimos.
    # La autenticación real la agregaremos después.
    print("Usuario:", username)
    print("Contraseña:", password)
    session["user_id"] = username
    
    return redirect(url_for("admin.admin_panel"))


@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    session.pop("user_id", None)

    return redirect(url_for("public.home"))