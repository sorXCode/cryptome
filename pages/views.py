from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, render_template_string, request, url_for, request)
from flask_user import login_required
import json, os
from pprint import pprint
page_bp = Blueprint("page_bp", __name__, url_prefix="/pages")

@page_bp.route("/<int:id>")
@login_required
def get_page(id):
    file_path = f"static/data/page{id}.json"

    if not os.path.exists(file_path):
        return render_template("page.html")

    json_data = json.load(open(file_path))
    pprint(json_data)
    title = list(json_data.keys())[0]
    rows = json_data[title]
    headings = rows[0].keys()
    return render_template("page.html", title=title, rows=rows, headings=headings)