#!/usr/bin/env python3
"""A simple Flask application with language localization support.

This application renders an HTML template using Flask and handles localization
with Flask-Babel, supporting multiple languages based on user request headers.

Attributes:
    app (Flask): The main Flask application instance.
    babel (Babel): The Babel instance to handle localization.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration settings for localization in the Flask application.

    Defines the supported languages, the default locale, and the default
    timezone for the application.

    Attributes:
        LANGUAGES (list): List of languages supported by the app.
        BABEL_DEFAULT_LOCALE (str): The default language locale.
        BABEL_DEFAULT_TIMEZONE (str): The default timezone setting.
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

    This function uses the accepted languages from the request headers and
    finds the best match with the application's supported languages.

    Returns:
        str: The code of the matched language (e.g., 'en' or 'fr').
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the homepage template.

    This route serves the '3-index.html' template when the root URL ('/') is
    accessed.

    Returns:
        A rendered HTML template for the homepage.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    # Run the application on port 5000, accessible on all network interfaces.
    app.run(port="5000", host="0.0.0.0", debug=True)
