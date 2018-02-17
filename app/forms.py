from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import ValidationError
from wtforms.fields import IntegerField, TextAreaField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Length, URL


class URLValidator(URL):
    """
    Redefined WTForms URL class with the ability submit an empty URL field.
    """
    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = _('Invalid URL.')

        if field.data:
            match = super(URL, self).__call__(form, field, message)
            if not self.validate_hostname(match.group('host')):
                raise ValidationError(message)


class EstimationForm(FlaskForm):
    speed = IntegerField(
        label=_('Speed'),
        description=_(
            'Reading speed. Usually this value about 200 words per minute.'
        ),
        default=200,
        validators=[DataRequired()]
    )
    url = URLField(
        label='URL',
        description=_(
            'Paste URL address that should be estimated. Max length is 2083'
            ' characters.'
        ),
        validators=[Length(max=2083), URLValidator()]
    )
    text = TextAreaField(
        label=_('Plain text'),
        description=_(
            'Plain text for reading estimation. Max length is 5000-000'
            ' characters.'
        ),
        validators=[Length(max=500000)]
    )
    recaptcha = RecaptchaField()
