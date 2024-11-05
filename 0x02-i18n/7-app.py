#!/usr/bin/env python3
"""A simple Flask application with localization and user timezone support.

This application serves a webpage using Flask and Flask-Babel for
internationalization and timezone handling. Users can log in with
preferences for locale and timezone, and the application adapts the
content accordingly.

Attributes:
    app (Flask): The main Flask application instance.
    babel (Babel): The Babel instance for localization support.
    users (dict): Sample user data containing localization and timezone
                  settings.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from pytz import timezone
import pytz.exceptions


class Config(object):
    """Configuration settings for the Flask application.

    Defines the supported languages, default locale, and default timezone
    for the application.

    Attributes:
        LANGUAGES (list): List of supported languages for localization.
        BABEL_DEFAULT_LOCALE (str): Default language for the application.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the application.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Configure the Flask application with the defined settings.
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


# Sample user data containing names, locales, and timezones.
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieve a user dictionary based on the 'login_as' query parameter.

    Checks if a 'login_as' parameter is present in the request. If found,
    attempts to retrieve the corresponding user from the `users` dictionary.

    Returns:
        dict: A dictionary containing user data or None if the user is
              not found or 'login_as' is not provided.
    """
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """Set user data in the global context before each request.

    This function runs before every request to make user information
    accessible in templates and routes by storing it in `g.user`.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """Determine the best locale for the user based on various sources.

    Checks for a 'locale' parameter in the URL, user preferences,
    and request headers to determine the best match for localization.

    Returns:
        str: The selected language code (e.g., 'en' or 'fr').
    """
    # Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # Locale from user settings
    if g.user:
        locale = g.user.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale

    # Locale from request header
    locale = request.headers.get('locale', None)
    if locale in app.config['LANGUAGES']:
        return locale

    # Default locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Select and return the appropriate timezone for the user.

    This function determines the user's timezone preference by checking
    the 'timezone' parameter in the URL, user settings, and defaults
    to UTC if no valid timezone is found.

    Returns:
        str: The selected timezone string, or the default timezone.
    """
    # Find timezone parameter in URL parameters
    tzone = request.args.get('timezone', None)
    if tzone:
        try:
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Find time zone from user settings
    if g.user:
        try:
            tzone = g.user.get('timezone')
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Default to UTC
    default_tz = app.config['BABEL_DEFAULT_TIMEZONE']
    return default_tz


@app.route('/')
def index():
    """Render the homepage template.

    This route serves the main page of the application and returns the
    '5-index.html' template to the client.

    Returns:
        A rendered HTML template for the homepage.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    # Run the application on port 5000, accessible on all network interfaces.
    app.run(port="5000", host="0.0.0.0", debug=True)
