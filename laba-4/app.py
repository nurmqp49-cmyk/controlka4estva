from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from modules.auth import auth_bp
from modules.catalog import catalog_bp
from modules.booking import booking_bp
from modules.payment import payment_bp

app = Flask(__name__)
app.secret_key = "ticketbook-secret-2024"

# Register blueprints
app.register_blueprint(auth_bp,    url_prefix="/auth")
app.register_blueprint(catalog_bp, url_prefix="/catalog")
app.register_blueprint(booking_bp, url_prefix="/booking")
app.register_blueprint(payment_bp, url_prefix="/payment")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
