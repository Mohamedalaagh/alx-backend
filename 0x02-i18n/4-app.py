#!/usr/bin/env python3
"""A simple Flask application with dynamic localization support.

This application uses Flask to render an HTML template and Flask-Babel for
localization, supporting multiple languages (English and French) based on
user preferences in the request or query parameters.

Attributes:
    app (Flask): The main Flask application instance.
    babel (Babel): The Babel instance to handle localization.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration settings for localization in the Flask application.

    Defines the supported languages, default locale, and default timezone.

    Attributes:
        LANGUAGES (list): List of supported languages.
        BABEL_DEFAULT_LOCALE (str): Default language locale.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone setting.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Initialize the Flask application with configuration settings.
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Select the best match for the user's preferred language.

    Checks if a 'locale' query parameter is provided in the request URL. If
    the parameter matches a supported language, it is used as the locale.
    Otherwise, the best match from the request headers is chosen.

    Returns:
        str: The selected language code (e.g., 'en' or 'fr').
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the homepage.

    This route renders the '4-index.html' template when the root URL ('/') is
    accessed.

    Returns:
        A rendered HTML template for the homepage.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    # Run the application on port 5000, accessible on all network interfaces.
    app.run(port="5000", host="0.0.0.0", debug=True)
