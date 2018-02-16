import re
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import ValidationError
from wtforms.fields import IntegerField, TextAreaField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Length

REGEXP = re.compile(
    r'^[a-z]+://(?P<host>[^/:]+)(?P<port>:[0-9]+)?(?P<path>/.*)?$'
)


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
        validators=[Length(max=2083)]
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

    def validate_url(self, field):
        if field.data:
            if not REGEXP.search(field.data):
                raise ValidationError(
                    _('Invalid URL.')
                )
