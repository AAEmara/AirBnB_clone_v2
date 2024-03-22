#!/usr/bin/python3
"""Module for starting a Flask web application."""


from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def remove_session():
    """Removes the current SQLAlchemy Session."""
    storage.close()


@app.route("/state_list", strict_slashes=False)
def state_list():
    """Displaying an HTML page inside the body tag."""
    class_name = "State"
    state_objs = storage.all(class_name)
    return (render_template(header_name=class_name, states=state_objs))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
