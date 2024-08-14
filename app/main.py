from flask import Flask
from routes import routes_bp
import os

def creatApp():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.urandom(12)
    app.folder_static = "static"
    return app

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    app = creatApp()
    app.register_blueprint(routes_bp)
    app.run(debug=True, host=host, port=port)