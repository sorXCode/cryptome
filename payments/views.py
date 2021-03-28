from flask import Blueprint, render_template, request
from .models import Transaction
from pprint import pprint
from subscriptions.models import Subscription

payment_bp = Blueprint("payment_bp", __name__, url_prefix="/payments")


@payment_bp.route("/webhook", methods=["POST"])
def webhook():
    """
    Complete payment flow by verifying the code from webhook data and the Transactions model
    """
    def create_subscription():
        Subscription.create_monthly_subscription(user_id=user_id, code=code)
        pass

    body = request.json
    pprint(request.json)

    code = body["event"]["data"]["code"]
    transaction = Transaction.get_transaction_by_code(
        code=code)

    if not transaction:
        return "Couldn't find transaction matching code", 422

    user_id = transaction.user_id

    create_subscription()

    transaction.set_webhook_data(body)
    return "saved", 200


@payment_bp.route("/log", methods=["POST"])
def log_data():
    try:
        data = request.json
        print("logging data => ")
        pprint(data)

        if not isinstance(data, dict):
            raise ValueError('No valid data found')

        transaction = Transaction(**data)
        transaction.save()
        return "success", 200
    except:
        return "failed", 400
