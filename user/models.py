from flask_user import UserMixin
from app import db
from datetime import datetime
from app import login_manager
from flask_user import PasswordManager
from flask import current_app
from uuid import uuid4
from rewards.models import Reward
from subscriptions.models import Subscription, SourceEnum


def get_random_id():
    return uuid4().hex


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100, collation='NOCASE'),
                         nullable=False, unique=True)
    email = db.Column(db.String(collation='NOCASE'),
                      nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'),
                           nullable=True, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'),
                          nullable=True, server_default='')
    subscription = db.relationship(
        "Subscription", backref="user", lazy="dynamic")
    is_logged_in = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    refferal_code = db.Column(db.String, default=get_random_id)

    def has_active_subscription(self):
        return Subscription.has_active_subscription(self.id)

    def can_be_logged_in(self):
        if not self.is_logged_in:
            return True
        return False

    def update_logout(self):
        self.is_logged_in = False
        self.save()

    def update_last_login(self):
        if self.is_logged_in:
            return None
        self.last_login = datetime.now()
        self.is_logged_in = True
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def activate_reward_for_user_if_any(self):
        print("Trying to activate")
        reward = Reward.user_unused_reward(self.id)
        print("reward=>", reward)

        if reward:
            Subscription.create_monthly_subscription(user_id=self.id, source=SourceEnum.rewards)
            reward.mark_as_used()
        return bool(reward)
        
    @classmethod
    def get_user_by_email_or_username(cls, user_info):
        return cls.query.filter_by(email=user_info).first() or cls.query.filter_by(username=user_info).first()


@login_manager.user_loader
def _load_user(token):
    # return None
    user = User.get_user_by_token(token)
    user.update_last_login()
    return user


class UserInvitation(db.Model):
    __tablename__ = 'auth_invite'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), server_default=db.func.now())
    # token used for registration page to identify user registering
    token = db.Column(db.String(100), nullable=False, server_default='')
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    

    def __repr__(self):
        return '<auth.UserInvitation(email="{}",on="{}")>'.format(
            self.email, self.created_on)


