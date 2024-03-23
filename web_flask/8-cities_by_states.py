#!/usr/bin/python3
"""Module for starting a Flask web application."""


from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from os import getenv
from sqlalchemy import select
from models.engine.db_storage import DBStorage


app = Flask(__name__)


@app.teardown_appcontext
def remove_session(exception=None):
    """Removes the current SQLAlchemy Session."""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def state_list():
    """Displaying an HTML page inside the body tag."""
    class_name = "States"
    state_dict = dict()
    if getenv("HBNB_TYPE_STORAGE") != "db":
        state_objs = storage.all(State)
        for key, value in state_objs.items():
            curr_value = value.to_dict()
            state_name = curr_value['name']
            state_id = curr_value['id']
            if state_name not in state_dict:
                state_dict[state_name] = {'state_id': state_id,
                                          'cities': list()}

            cities_objs = value.cities
            for obj in cities_objs:
                city_dict = obj.to_dict()
                city_id = city_dict['id']
                city_name = city_dict['name']
                city_append = {'city_name': city_name, 'city_id': city_id}
                state_dict[state_name]['cities'].append(city_append)

    else:
        Session = storage._DBStorage__session
        stmnt = select(State.id, State.name, City.id, City.name)\
            .join(State.cities, isouter=True)\
            .order_by(State.name, City.name)

        instances = Session.execute(stmnt).all()
        for instance in instances:
            state_name = instance[1]
            state_id = instance[0]
            if state_name not in state_dict:
                state_dict[state_name] = {'state_id': state_id,
                                          'cities': list()}

            city_dict = {'city_id': instance[2],
                         'city_name': instance[3]}
            state_dict[state_name]['cities'].append(city_dict)

    return (render_template('8-cities_by_states.html', header_name=class_name,
                            states_cities=state_dict))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
