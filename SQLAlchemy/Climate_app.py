import numpy as np
import pandas as pd
import os
import datetime as dt

import sqlalchemy
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, Date

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#create dates to be used
most_current = dt.date(2017, 8, 23)
last_year = most_current - dt.timedelta(days=365)


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date=most_current):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()



# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/&lt;start&gt; <br/>"
        f"enter date in place of &lt;start&gt; in format %Y-%m-%d<br/>"
        f"<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt; <br/>"
        f"enter start date in place of &lt;start&gt; and end date in place of &lt;end&gt; in format %Y-%m-%d<br/>"

    )

@app.route("/api/v1.0/precipitation")
def prcp():
    results = session.query(Measurements.date, Measurements.tobs).group_by(Measurements.date).all()

    all_datepcrp = []
    for date, tobs in results:
        datepcrp_dict = {}
        datepcrp_dict["date"] = date
        datepcrp_dict["tobs"] = tobs
        all_datepcrp.append(datepcrp_dict)
    return jsonify(all_datepcrp)



@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Stations.station, Stations.name).all()
    return jsonify(station_list)




@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date>=last_year).all()
    return jsonify(results)




@app.route("/api/v1.0/<start>/")
def start_date(start):
    start_data = calc_temps(start)
    tmin, tmax, tavg = start_data[0]
    temp_info = {
        "Min Temp":tmin,
        "Max Temp":tmax,
        "Avg Temp":tavg
    }
    return jsonify(temp_info)


@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    date_range = calc_temps(start, end)
    tmin, tmax, tavg = date_range[0]
    temp_info = {
        "Min Temp":tmin,
        "Max Temp":tmax,
        "Avg Temp":tavg
    }
    return jsonify(temp_info)


if __name__ == '__main__':
    app.run(debug=True)