from flask import render_template, Blueprint, request, flash, url_for, redirect, session, make_response
from passlib.hash import sha256_crypt
from conn import cursor, conn, Error

class RegisterUser:
    def __init__(self, username, email, password) -> None:
        self._username = username
        self.__email = email
        self.__password = sha256_crypt.hash(password) if password is not None else None
    
    def save_user(self):
        try:
            validate_email = "SELECT * FROM users WHERE email = %s"
            cursor.execute(validate_email, (self.__email,))
            results = cursor.fetchall()
        except Error as err:
            print(err)
            # criar uma página de error depois
        if not results:
            try:
                query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s);"
                values = (self._username, self.__email, self.__password)
                cursor.execute(query, values)
                conn.commit()
                return True
            except Error as err:
                print(err)
                # criar uma página de error depois
        else:
            flash("This email already exist")
        
class AuthenticateUser:
    def __init__(self, email, password):
        self.__email = email
        self.__password = password
        self.__userData = None
    
    def verifyIfUserExist(self):
        try:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (self.__email,))
            results = cursor.fetchall()
            print(results)
        except Error as err:
            print(err)
            # criar uma página de error depois
        if results:
            print(results)
            results_data = [
                {
                    "id": id, 
                    "name": name,
                    "email": email,
                    "password": password
                }
                for id, name, email, password in results
            ]
            self.__userData = results_data
            return self.__verifyPassword()
        else:
            flash("User do not exist1")
            
            
    def __verifyPassword(self):
        password_encrypted = self.__userData[0]["password"]
        verify_encrypted_password = sha256_crypt.verify(self.__password, password_encrypted)
        print(verify_encrypted_password)
        if verify_encrypted_password:
            response = make_response("dados")
            response.set_cookie('auth_user', 'user123')
            session.permanent = True
            session["authenticate"] = True
            session["id"] = self.__userData[0]["id"]
            session["name"] = self.__userData[0]["name"]
            return True
        else:
            flash("User do not exist")

routes_bp = Blueprint('routes_bp', __name__, template_folder='templates')

@routes_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        authenticate_user = AuthenticateUser(email, password)
        authenticate_user.verifyIfUserExist()
        if session["authenticate"]:
            return redirect(url_for("routes_bp.home"))
    
    return render_template("login.html")


@routes_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.form:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password == confirm_password:
            register_user = RegisterUser(username, email, password)
            if register_user.save_user():
                return redirect(url_for("routes_bp.login"))
        else:
            flash("The passwords are not the same")
            
    return render_template("register.html")

@routes_bp.route("/")
def index():
    return redirect(url_for("routes_bp.login"))

@routes_bp.route("/home", methods=['GET'])
def home():
    print(session)
    if session:
        return render_template("home.html")
    else:
        flash("You are not authenticated")
        return redirect(url_for("routes_bp.login"))