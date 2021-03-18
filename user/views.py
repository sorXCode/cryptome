import os
from flask import Blueprint, render_template, abort, redirect, request, flash, abort, url_for, current_app

from app import coinbase_client
from json.decoder import JSONDecodeError
from flask_login import login_manager, logout_user, login_required, current_user
from flask_user.forms import LoginForm
from is_safe_url import is_safe_url
from flask_login import login_user
from .models import User

user = Blueprint("user", __name__)


@user.route('/login', methods=['GET', 'POST'])
def custom_login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if request.method=="POST" and form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class

        user_manager = current_app.user_manager
        if user_manager.USER_ENABLE_USERNAME:
            # Find user by username
            user = user_manager.db_manager.find_user_by_username(form.username.data)

            # Find user by email address (username field)
            if not user and user_manager.USER_ENABLE_EMAIL:
                user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(form.username.data)

        else:
            # Find user by email address (email field)
            user, user_email = user_manager.db_manager.get_user_and_user_email_by_email(form.email.data)

        
        if user and user_manager.verify_password(form.password.data, user.password):
            pass
        else:
            return abort(400)

        if not user.can_be_logged_in():
            flash("Please log out of other device")
            return render_template('flask_user/login.html', login_form=form, form=form)

        login_user(user)                        # Successful authentication
        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next, ["*"]):
            return redirect(url_for('.index'))

        return redirect(next or url_for('.index'))
    return render_template('flask_user/login.html', login_form=form, form=form)
    
# @user.route("/onboard")
# def onboard():
#     referral = request.args.get("referral")
#     return render_template("onboard.html", referral=referral)

@user.route("/")
def index():
    checkout = None
    try:
        checkout = coinbase_client.checkout.retrieve(os.environ.get("COINBASE_CHECKOUT_ID"))
    except JSONDecodeError:
        print("cannot decode checkout response")

    if not checkout:
        abort(404, "Invalid checkout")
    return render_template("index.html", checkout=checkout)