from flask import render_template, Blueprint, request, flash
from passlib.hash import sha256_crypt
from conn import cursor, conn, Error

class RegisterUser:
    def __init__(self, username, email, password) -> None:
        self._username = username
        self.__email = email
        self.__password = sha256_crypt.hash(password)
    
    def save_user(self):
        validate_email = "SELECT * FROM users WHERE email = %s"
        cursor.execute(validate_email, (self.__email,))
        results = cursor.fetchall()
        if not results:
            try:
                query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s);"
                values = (self._username, self.__email, self.__password)
                cursor.execute(query, values)
                conn.commit()
            except Error as err:
                print(err)
                flash("This email already existe")
        else:
            flash("This email already existe")
        
        

routes_bp = Blueprint('routes_bp', __name__, template_folder='templates')

@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    
    if password == confirm_password and password != None:
        register_user = RegisterUser(username, email, password)
        register_user.save_user()
    else:
        flash("As senhas nao sao iguais")
        
    return render_template("register.html")