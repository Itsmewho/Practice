from flask import Flask
from flask_cors import CORS
from flask import send_from_directory
from routes.register.register_route import register_bp
from routes.auth.auth_routes import auth_bp
from routes.login.login_route import login_bp

app = Flask(__name__)
CORS(app)


# All routes.
app.register_blueprint(register_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(login_bp)


# Favicon fun
@app.route("/favicon.svg")
def favicon():
    return send_from_directory("static", "favicon.svg", mimetype="image/svg+xml")


#  Main route
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml">
        <title>Backend server</title>
      </head>
      <body>
        <h1>Flask is running!</h1>
      </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
