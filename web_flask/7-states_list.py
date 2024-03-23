#!/usr/bin/python3
"""Module for starting a Flask web application."""


from flask import Flask, render_template
from models import storage
from os import getenv


app = Flask(__name__)


@app.teardown_appcontext
def remove_session(exception=None):
    """Removes the current SQLAlchemy Session."""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def state_list():
    """Displaying an HTML page inside the body tag."""
    class_name = "States"
    state_dict = dict()
    state_objs = storage.all("State")
    if getenv("HBNB_TYPE_STORAGE") != "db":
        for key, value in state_objs.items():
            curr_value = value.to_dict()
            key_name = curr_value['id']
            value_name = curr_value['name']
            state_dict[key_name] = value_name
    else:
        for key, value in state_objs.items():
            curr_value = value.to_dict()
            key_name = curr_value['id']
            value_name = curr_value['name']
            state_dict[key_name] = value_name

    return (render_template('7-states_list.html', header_name=class_name,
                            states=state_dict))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
