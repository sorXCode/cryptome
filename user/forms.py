from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+

from wtforms import BooleanField, HiddenField, PasswordField, SubmitField, StringField, FileField
from wtforms import validators, ValidationError
from flask_wtf.file import FileAllowed
import re

class EditUserProfileForm(FlaskForm):
    """Edit user profile form."""

    profile_picture = FileField(u'Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg',], 'Images only!')])
    first_name = StringField('First name', validators=[validators.DataRequired()])
    last_name = StringField('Last name', validators=[validators.DataRequired()])

    submit = SubmitField('Update')

    def validate_profile_picture(form, field):
        if field.data:
            field.data.filename = re.sub(r'[^a-z0-9_.-]', '_', field.data.filename)