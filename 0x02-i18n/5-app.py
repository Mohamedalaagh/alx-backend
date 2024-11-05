#!/usr/bin/env python3
"""A simple Flask application with dynamic localization and user support.

This application uses Flask to render an HTML template with user-specific
language and timezone support. Localization is managed by Flask-Babel, allowing
the app to serve content in multiple languages based on user preferences.

Attributes:
    app (Flask): The main Flask application instance.
    babel (Babel): The Babel instance to handle localization.
    users (dict): Sample user data, containing language and timezone settings.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config(object):
    """Configuration settings for localization in the Flask application.

    Defines supported languages, the default locale, and the default timezone
    for the application.

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


# Sample user data with predefined locale and timezone.
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieve a user dictionary based on the 'login_as' query parameter.

    Checks if a 'login_as' parameter is present in the request's URL. If found,
    attempts to fetch the corresponding user from the `users` dictionary.

    Returns:
        dict: A dictionary containing user data, or None if the user is not
              found or 'login_as' is not provided.
    """
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """Store the user in the global context before each request.

    Sets the `g.user` variable to the user retrieved from `get_user()`.
    This makes the user data accessible in templates or other routes.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """Select the best match for the user's preferred language.

    Checks for a 'locale' parameter in the request URL. If valid, uses it as
    the locale. Otherwise, falls back to the best match accepted languages.

    Returns:
        str: The selected language code (e.g., 'en' or 'fr').
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the homepage with user data if available.

    This route renders the '5-index.html' template when the root URL ('/') is
    accessed, and includes user-specific data if the user is logged in.

    Returns:
        A rendered HTML template for the homepage.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    # Run the application on port 5000, accessible on all network interfaces.
    app.run(port="5000", host="0.0.0.0", debug=True)
