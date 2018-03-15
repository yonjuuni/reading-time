from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import IntegerField, TextAreaField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Length, URL


class EstimationForm(FlaskForm):
    speed = IntegerField(
        label=_('Speed'),
        description=_(
            'Reading speed. Usually this value is about 200 words per minute.'
        ),
        default=200,
        validators=[DataRequired()]
    )
    url = URLField(
        label='URL',
        description=_(
            'Paste the URL of the website that should be estimated. Max length'
            ' is 2083 characters.'
        ),
        validators=[Length(max=2083), URL()]
    )
    text = TextAreaField(
        label=_('Plain text'),
        description=_(
            'Plain text for reading estimation. Max length is 500 000'
            ' characters.'
        ),
        validators=[Length(max=500000)]
    )
    recaptcha = RecaptchaField()
