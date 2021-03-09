import os
from flask import Blueprint, render_template, abort
from app import coinbase_client
from json.decoder import JSONDecodeError

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/")
def home():
    checkout = None
    try:
        checkout = coinbase_client.checkout.retrieve(os.environ.get("COINBASE_CHECKOUT_ID"))
    except JSONDecodeError:
        print("cannot decode checkout response")

    if not checkout:
        abort(404, "Invalid checkout")
    return render_template("index.html", checkout=checkout)
