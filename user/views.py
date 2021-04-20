import os
from json.decoder import JSONDecodeError

from app import coinbase_client
from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, render_template_string, request, url_for, request)
from flask_login import (current_user, login_manager, login_required,
                         login_user, logout_user)
from flask_user.forms import LoginForm
from is_safe_url import is_safe_url
from flask_user import UserManager
from .models import User, UserInvitation
from rewards.models import Reward
from functools import wraps

user = Blueprint("user", __name__)


def user_can_login(func, *args, **kwargs):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method == "POST":
            user = User.get_user_by_email_or_username(request.form["username"])
            
            if user and user.can_be_logged_in():
                return func(*args, **kwargs)
            
            elif user and not user.can_be_logged_in():
                flash("Please log out of other device")
                return redirect(url_for('user.login'), 301)

        return func(*args, **kwargs)
    return decorated_view


class CustomUserManager(UserManager):

    @user_can_login
    def login_view(self):
        return super().login_view()


@user.route("/")
@login_required
def index():
    if not current_user.has_active_subscription():
        current_user.activate_reward_for_user_if_any()

    checkout = None
    try:
        checkout = coinbase_client.checkout.retrieve(
            os.environ.get("COINBASE_CHECKOUT_ID"))
    except JSONDecodeError:
        print("cannot decode checkout response")

    if not checkout:
        abort(404, "Invalid checkout")
    return render_template("index.html", checkout=checkout)


@user.route("/profile")
@login_required
def profile():
    referrals = UserInvitation.get_invited_users_for_user_id(current_user.id)
    unused_rewards = Reward.user_unused_reward(current_user.id, all=True)
    return render_template("profile.html", referrals=referrals, rewards=unused_rewards)


{'links': [('/user/resend-email-confirmation',
            'user.resend_email_confirmation'),
           ('/user/edit_user_profile', 'user.edit_user_profile'),
           ('/user/change-password', 'user.change_password'),
           ('/user/change-username', 'user.change_username'),
           ('/user/forgot-password', 'user.forgot_password'),
           ('/user/manage-emails', 'user.manage_emails'),
           ('/user/invite', 'user.invite_user'),
           ('/register', 'user.register'),
           ('/site-map', 'site_map'),
           ('/signin', 'user.login'),
           ('/logout', 'user.logout'),
           ('/login', 'user.custom_login'),
           ('/', 'user.index')]}
