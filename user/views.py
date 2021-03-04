from flask import Blueprint, render_template

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/")
def home():
    return render_template("index.html")