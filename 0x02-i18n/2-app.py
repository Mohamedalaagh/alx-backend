#!/usr/bin/env python3
"""A simple Flask application with language localization support.

This application uses Flask to render a basic HTML template and Flask-Babel
to handle localization in multiple languages (English and French) based on
user preferences in the request.

Attributes:
    app (Flask): The main Flask application instance.
    babel (Babel): The Babel instance to handle localization.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration settings for the Flask application.

    This class sets up localization parameters, including supported languages,
    the default locale, and the default timezone.

    Attributes:
        LANGUAGES (list): List of supported languages.
        BABEL_DEFAULT_LOCALE (str): Default locale setting.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone setting.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Initialize the Flask application with the specified configuration.
app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages.

    This function uses the request's accepted languages to find the best match
    with the application's supported languages.

    Returns:
        str: The best matched language code (e.g., 'en' or 'fr').
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the homepage.

    This route renders the '2-index.html' template when the root URL ('/') is
    accessed.

    Returns:
        A rendered HTML template for the homepage.
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    # Run the application on port 5000 and host 0.0.0.0 in debug mode.
    app.run(port="5000", host="0.0.0.0", debug=True)
