#!/usr/bin/python3
"""Module for starting a Flask web application."""


from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from os import getenv
from sqlalchemy import select, text
from sqlalchemy import exc
from models.engine.db_storage import DBStorage


app = Flask(__name__)


@app.teardown_appcontext
def remove_session(exception=None):
    """Removes the current SQLAlchemy Session."""
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """Displaying an HTML page inside the body tag with sorted the states."""
    class_name = "States"
    state_dict = dict()
    state_objs = storage.all(State)
    for key, value in state_objs.items():
        curr_value = value.to_dict()
        state_name = curr_value['name']
        state_id = curr_value['id']
        state_dict[state_name] = {'state_id': state_id, 'cities': list()}

    return (render_template('9-states.html', header_name=class_name,
                            states_cities=state_dict))


@app.route("/states/<id>", strict_slashes=False)
def states_with_id(id):
    """Displaying an HTML page inside the body tag for certain state's id."""
    state_name = ""
    state_format = ""
    city_format = ""
    state_dict = dict()

    if getenv("HBNB_TYPE_STORAGE") != 'db':
        states_objs = storage.all(State)

        for key, value in states_objs.items():
            curr_value = value.to_dict()
            if id == curr_value['id']:
                state_name = curr_value['name']
                state_format = f"State: {state_name}"
                city_format = "Cities:"

                if state_name not in state_dict:
                    state_dict[state_name] = {'state_id': curr_value['id'],
                                              'cities': dict()}

                cities_objs = value.cities
                for obj in cities_objs:
                    city_dict = obj.to_dict()
                    city_id = city_dict['id']
                    city_name = city_dict['name']
                    state_dict[state_name]['cities'][city_name] = city_id

    else:
        Session = storage._DBStorage__session

        # Querying on the state that mathces the given `id`.
        stmnt_1 = select(State.name)\
            .filter(text("id=:value").params(value=id))
        # Handling the exeception of not finiding the state according to
        # given `id`.
        try:
            state_instance = Session.execute(stmnt_1).one()
        except exc.NoResultFound:
            state_instance = None

        if state_instance:
            state_name = state_instance[0]
            state_format = f"State: {state_name}"
            city_format = "Cities:"

            # Querying on states and cities to get the related cities according
            # to state's id.
            stmnt_2 = select(State.id, State.name, City.id, City.name)\
                .join(State.cities, isouter=True)\
                .filter(text("states.id=:value").params(value=id))\
                .order_by(State.name, City.name)

            instances = Session.execute(stmnt_2).all()
            for instance in instances:
                state_id = instance[0]
                if state_name not in state_dict:
                    state_dict[state_name] = {'state_id': state_id,
                                              'cities': dict()}

                state_dict[state_name]['cities'][instance[3]] = instance[2]

    return (render_template('9-states.html', header_name=state_format,
                            states_cities=state_dict,
                            second_header=city_format))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
