from flask import Blueprint, render_template, request
from .models import CompletedTransaction
from pprint import pprint
from subscriptions.models import Subscription

payment_bp = Blueprint("payment_bp", __name__, url_prefix="/payment")


@payment_bp.route("/webhook", methods=["POST"])
def webhook():
    def create_subscription():
        Subscription.create_monthly_subscription(user_id=user_id,code=code)
        pass

    body = request.json
    pprint(request.json)

    code = body["event"]["data"]["code"]
    transaction = CompletedTransaction.get_transaction_by_code(
        code=code)
    
    if not transaction:
        return "Couldn't find transaction matching code", 422
    
    user_id = transaction.user_id

    create_subscription()

    transaction.set_webhook_data(body)
    return "saved", 200


@payment_bp.route("/log", methods=["POST"])
def log_data():
    data = request.json
    print("logging", data)

    transaction = CompletedTransaction(**data)
    transaction.save()
    return "success", 200
