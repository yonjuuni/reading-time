from math import ceil

import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from flask import (
    Blueprint, current_app, flash, redirect, render_template,
    request, send_from_directory, url_for
)
from flask_babel import lazy_gettext as _
from inscriptis import get_text

from app.forms import EstimationForm

app_bp = Blueprint('app', __name__)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36'
                  '(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}


@app_bp.route('/')
def home():
    return render_template(
        'app/home.html'
    )


@app_bp.route('/evaluation/', methods=['GET', 'POST'])
def evaluation_form():
    form = EstimationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.text.data:
                text = form.text.data.strip()
                words = text.split()
                time = ceil(len(words) / form.speed.data)
                flash(
                    _('Text box estimation is next. Words counted: '
                      '%(len)s. Reading time: ~ %(time)s min',
                      len=len(words),
                      time=time
                      ),
                    category='info'
                )
            if form.url.data:
                url = form.url.data.strip()
                try:
                    html = requests.get(
                        url,
                        headers=HEADERS
                    )
                except (ConnectionError, ConnectTimeout):
                    flash(
                        _('This link is unreachable.'),
                        category='danger'
                    )
                    return redirect(url_for('app.evaluation_form'))
                text = get_text(html.text)
                words = text.split()
                time = ceil(len(words) / form.speed.data)
                flash(
                    _('URL box estimation is next. Words counted: '
                      '%(len)s. Reading time: ~ %(time)s min',
                      len=len(words),
                      time=time
                      ),
                    category='info'
                )

            if not form.text.data and not form.url.data:
                flash(
                    _(
                        'You should specify at least one of next fields: '
                        'URL or/and Text box.'
                      ),
                    category='warning'
                )
            else:
                return redirect(url_for('app.evaluation_form'))

    return render_template(
        'app/evaluation_form.html',
        form=form
    )
