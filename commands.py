
import click
from datetime import datetime
from werkzeug.security import generate_password_hash
from user.models import User
from rewards.models import Reward
from flask import Blueprint
from app import user_manager

command_bp = Blueprint('admin', __name__)


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@command_bp.cli.command('adduser')
@click.option('--username', prompt="Enter Username", required=True,)
@click.option('--email', prompt="Enter Email", required=True,)
@click.option('--password', prompt="Enter Password For User", hide_input=True,
              confirmation_prompt=True)
@click.option('--last_name', prompt="Enter Last Name", required=True,)
@click.option('--first_name', prompt="Enter First Name", required=True,)
def add_user(username, email, password, first_name, last_name):
    try:
        password = user_manager.password_manager.hash_password(password)
        user = User(active=True,
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name)
        user.email_confirmed_at = datetime.now()
        user.save()

        click.echo("User Created")
    except Exception as e:
        click.echo(f"User Creation Failed\n{e}")


@command_bp.cli.command('deleteuser')
@click.option('--identity', prompt="Enter user's email or username")
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to delete this user?')
def delete_user(identity):
    user = User.get_user_by_email_or_username(identity)
    if user:
        user.delete()
        click.echo("User Deleted")
    else:
        click.echo("User Not Found")


@command_bp.cli.command('rewarduser')
@click.option('--identity', prompt="Enter user's email or username")
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to reward this user?')
def reward_user(identity):
    user = User.get_user_by_email_or_username(identity)
    if user:
        reward = Reward(user_id=user.id, completed=3,
                        created_at=datetime.now())
        reward.save()
        click.echo("User Rewarded!")
    else:
        click.echo("User Not Found")


@command_bp.cli.command('rewardall')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to reward all users?')
def reward_user():
    users = User.all()
    for user in users:
        reward = Reward(user_id=user.id, completed=3,
                        created_at=datetime.now())
        reward.save()
        click.echo(f"{user.email} Rewarded!")

    click.echo(f"All Users Rewarded!")


@command_bp.cli.command('deletereward')
@click.option('--identity', prompt="Enter user's email or username")
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to reward this user?')
def reward_user(identity):
    user = User.get_user_by_email_or_username(identity)
    if user:
        reward = Reward.user_unused_reward(user.id)
        if reward:
            reward.delete()
            click.echo("Reward Delete!")
        else:
            click.echo("User has no unused reward")
    else:
        click.echo("User Not Found")


@command_bp.cli.command('mailall')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to mail all users?')
@click.option('--subject', prompt="Enter the mail subject")
@click.option('--body', prompt="Enter the mail body (html allowed)")
def reward_user(subject, body):
    template_file = "flask_user/emails/mail_users"
    users = User.all()
    count = 0
    for user in users:
        response = user_manager.email_manager._render_and_send_email(user.email, user, template_file, subject=subject, body=body)
        count += 1
        click.echo(f"Sent {count} of {len(users)}...")
        
    click.echo(f"All ({len(users)}) Users mailed!")
