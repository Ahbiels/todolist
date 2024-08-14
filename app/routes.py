from flask import render_template, Blueprint, request

class RegisterUser:
    ...

routes_bp = Blueprint('routes_bp', __name__, template_folder='templates')

@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    print("test")
    return render_template("login.html")

@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    name = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    print(name, email, password, confirm_password)
    return render_template("register.html")