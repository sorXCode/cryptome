from flask import Blueprint, render_template, request
from .models import CompletedTransaction
from pprint import pprint

payment_bp = Blueprint("payment_bp", __name__, url_prefix="/subscriptions")


@payment_bp.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    pprint(request.json)
    transaction = CompletedTransaction.get_transaction_by_code(
        code=body["event"]["data"]["code"])
    
    if transaction:
        transaction.set_webhook_data(body)
        return "saved", 200
    return "Couldn't find transaction matching code", 422


@payment_bp.route("/log", methods=["POST"])
def log_data():
    data = request.json
    print("logging", data)

    transaction = CompletedTransaction(**data)
    transaction.save()
    return "success", 200
