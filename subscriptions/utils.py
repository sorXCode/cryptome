from functools import wraps
from flask_user import current_user
from flask import redirect, url_for, flash

def subscription_required(func, *args, **kwargs):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and current_user.has_active_subscription():
            return func(*args, **kwargs)
        flash("Subscription required to view page, subscribe below")
        return redirect(url_for("user.index"), 301)
    return decorated_view