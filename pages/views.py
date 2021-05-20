from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, render_template_string, request, url_for, request,
                   jsonify)
from flask_user import login_required
from subscriptions.utils import subscription_required
import json
import os
from pprint import pprint
page_bp = Blueprint("page_bp", __name__, url_prefix="/pages")


@page_bp.route("/<int:id>")
@login_required
@subscription_required
def get_page(id):
    file_path = f"static/data/page{id}.json"

    if not os.path.exists(file_path):
        return render_template("page.html")

    # supported types are [scalping, intraday and swing]
    json_data = json.load(open(file_path))
    title = list(json_data.keys())[0]
    rows = list(json_data[title])
    intervals = {
        "scalping": "5",
        "intraday": "60",
        "swing": "240",
    }
    headings = list(rows[0].keys())
    for row in rows:
        row["tradingview"] = json.dumps({
            "width": 980,
            "height": 610,
            "symbol": f"BINANCE:{row['market'].replace('/','')}",
            "interval": f"{intervals[row['type']]}",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": False,
            "allow_symbol_change": True,
            "container_id": "tradingview"
        })
    pprint(rows)
    # pprint(rows)
    return render_template("page.html", title=title, rows=rows, headings=headings, json_data=json_data)
