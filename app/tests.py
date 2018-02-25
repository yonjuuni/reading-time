import unittest

from flask import url_for
from functools import wraps

from app.views import app_bp
from core import create_app

app = create_app()


def wrap_test_context(func):
    """
    Wraps a test request context.
    :param func: any func that should be wrapped with test request context
    :return: wrapped function with test request context
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with app.test_request_context():
            return func(*args, **kwargs)

    return wrapper


class TestCaseSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.register_blueprint(app_bp)
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.client = app.test_client()

    @wrap_test_context
    def test_main_page_response(self):
        response = self.client.get(url_for('app.home'))
        self.assertEqual(response.status_code, 200)

    @wrap_test_context
    def test_evaluation_form_response(self):
        response = self.client.get(url_for('app.evaluation_form'))
        self.assertEqual(response.status_code, 200)

    @wrap_test_context
    def test_submit_of_empty_form(self):
        response = self.client.post(
            url_for('app.evaluation_form'),
            data={
                'speed': 200,
                'url': '',
                'text': ''
            }
        )
        self.assertIn(b'warning', response.data)
        self.assertEqual(response.status_code, 200)

    @wrap_test_context
    def test_submit_of_broken_url(self):
        response = self.client.post(
            url_for('app.evaluation_form'),
            data={
                'speed': 200,
                'url': 'https://broken1xyz1-url.com',
                'text': ''
            },
            follow_redirects=True
        )
        self.assertIn(b'danger', response.data)
        self.assertEqual(response.status_code, 200)

    @wrap_test_context
    def test_invalid_url_response(self):
        response = self.client.post(
            url_for('app.evaluation_form'),
            data={
                'speed': 200,
                'url': 'https://xyz',
                'text': ''
            },
            follow_redirects=True
        )
        self.assertIn(b'Invalid URL.', response.data)
        self.assertEqual(response.status_code, 200)

    @wrap_test_context
    def test_valid_url_response(self):
        response = self.client.post(
            url_for('app.evaluation_form'),
            data={
                'speed': 200,
                'url': 'https://google.com',
                'text': ''
            },
            follow_redirects=True
        )
        self.assertIn(b'info', response.data)
        self.assertEqual(response.status_code, 200)

    @wrap_test_context
    def test_valid_text_box(self):
        response = self.client.post(
            url_for('app.evaluation_form'),
            data={
                'speed': 200,
                'url': '',
                'text': 'test case test case test case'
            },
            follow_redirects=True
        )
        self.assertIn(b'info', response.data)
        self.assertIn(b'6', response.data)
        self.assertEqual(response.status_code, 200)
