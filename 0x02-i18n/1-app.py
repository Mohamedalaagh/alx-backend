#!/usr/bin/env python3
"""A simple Flask application with localization support.

This application uses Flask to render a basic HTML template. It also uses
Flask-Babel to support localization in multiple languages (English and French).

Attributes:
    app (Flask): The main Flask application instance.
    babel (Babel): The Babel instance to handle localization.
"""

from flask import Flask, render_template
from flask_babel import Babel


class Config(object):
    """Configuration class for the Flask app.

    This class defines configuration settings for localization, including
    supported languages, the default locale, and the default timezone.

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


@app.route('/')
def index():
    """Render the homepage.

    This route renders the '1-index.html' template when the root URL ('/') is
    accessed.

    Returns:
        A rendered HTML template for the homepage.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    # Run the application on port 5000 and host 0.0.0.0 in debug mode.
    app.run(port="5000", host="0.0.0.0", debug=True)
