#!/usr/bin/python3
"""Module for starting a Flask web application."""


from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """Returning a greeting message for visiting the `/`."""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def school():
    """Returning the `hbnb` name."""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def seas(text):
    """Returning `C` value and the value of the `<text>` variable."""
    return f'C {escape(text).replace("_", " ")}'


@app.route("/python/", defaults={'text': "is_cool"}, strict_slashes=False)
@app.route("/python/<text>")
def snakes(text):
    """Returning `Python` vlaue and the value of the `<text>` variable."""
    return f'Python {escape(text).replace("_", " ")}'


@app.route("/number/<int:n>", strict_slashes=False)
def nums(n):
    """Returning the number given before a certain text."""
    return f'{n} is a number'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
