from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, render_template_string, request, url_for, request)


page_bp = Blueprint("page_bp", __name__, url_prefix="/pages")

@page_bp.route("/<int:id>")
def get_page(id):
    return render_template("page.html")