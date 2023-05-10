from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///""C:/Users/nigan/sqlalchemy-challenge/resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Flask routes
@app.route('/')
def index():
    """Return available routes"""
    return ( f'''Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/<start>
    /api/v1.0/<start>/<end>
    '''
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Return the precipitation data for the last 12 months"""
    # Create session link to the database
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query to retrieve the precipitation data for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()

    session.close()

    # Create dictionary from the query results
    precipitation_dict = {}
    for date, prcp in precipitation_data:
        precipitation_dict[date] = prcp

    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def stations():
    """Return the list of stations"""
    # Create session link to the database
    session = Session(engine)

    # Query to retrieve the list of stations
    station_data = session.query(Station.station).all()

    session.close()

    # Create list from the query results
    station_list = []
    for station in station_data:
        station_list.append(station[0])

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    """Return the temperature observations for the last 12 months"""
    # Create session link to the database
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query to retrieve the temperature observations for the last 12 months from the most active station
    temp_obs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()

    session.close()

    # Create list from the query results
    temp_obs_list = []
    for date, tobs in temp_obs_data:
        temp_obs_dict = {}
        temp_obs_dict['date'] = date
        temp_obs_dict['tobs'] = tobs


if __name__ == '__main__':
    app.run(debug=True)
