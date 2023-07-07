# Import the dependencies.
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Create engine to hawaii.sqlite
# Set "check same thread" to false due to error
engine = create_engine("sqlite:///C:/Users/caize/Desktop/Data_Analysis/Analysis_Projects/sqlalchemy-challenge/Resources/hawaii.sqlite",
                        connect_args={'check_same_thread': False})

#reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
print(Base.classes.keys())

# #Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# List all available API routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start-end"
    )

# Create a route that returns json with the date as the key and the value as the precipitation
# And only returns the jsonified precipitation data for the last year in the database
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Calculate the date one year from the last date in data set in 2 steps:
    # Query for the most recent date in the dataset
    most_recent_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime.strptime(most_recent_date_str[0], '%Y-%m-%d').date()
    print(f"Most recent date: {most_recent_date}")
        
    # Calculate the earliest date by subtracting 365 days from the most recent date
    earliest_date = most_recent_date - dt.timedelta(days=365)
    print(f"Earliest date: {earliest_date}")

    # Perform a query to retrieve the the last 12 months of precipitation data
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date <= most_recent_date).filter(Measurement.date >= earliest_date).all()

    # Create a dictionary from the row data and append to a list of all_precipitation 
    all_precipitation = []
    for prcp, date in prcp_results:
        prcp_dict = {}
        prcp_dict["precipitation"] = prcp
        prcp_dict["date"] = date
        all_precipitation.append(prcp_dict)
    return jsonify(all_precipitation)

    session.close()

# Create a route that returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/stations")
def stations():

    # Query for all stations in the database
    stn_results = session.query(Station.station, Station.id).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, id in stn_results:
        stn_dict = {}
        stn_dict["station"] = station
        stn_dict["station id"] = id
        all_stations.append(stn_dict)
    return jsonify(all_stations)

    session.close()

# Create a route that returns jsonified data for the most active station (USC00519281)
# And only returns the jsonified data for the last year of data
@app.route("/api/v1.0/tobs")
def tobs():

    # Calculate the date one year from the last date in data set in 2 steps:
    # Query for the most recent date in the dataset
    most_recent_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime.strptime(most_recent_date_str[0], '%Y-%m-%d').date()
    print(f"Most recent date: {most_recent_date}")
        
    # Calculate the earliest date by subtracting 365 days from the most recent date
    earliest_date = most_recent_date - dt.timedelta(days=365)
    print(f"Earliest date: {earliest_date}")

    # Perform a query to retrieve the the last 12 months of tobs data for the most active station
    tobs_results = session.query(Measurement.tobs, Measurement.date,  Measurement.station).\
                    filter(Measurement.date <= most_recent_date).filter(Measurement.date >= earliest_date).\
                    filter(Measurement.station == 'USC00519281').all()

    # Create a dictionary from the row data and append to a list of tobs_data
    tobs_data = []
    for tobs, date, station in tobs_results:
        tobs_dict = {}
        tobs_dict["temperature"] = tobs
        tobs_dict["date"] = date
        tobs_dict["station"] = station
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

# Create a start route that accepts the start date as a parameter from the URL 
# And returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
# @app.route("/api/v1.0/start")
#     def start():


# Create a start/end route that accepts the start and end dates as parameters from the URL
# And returns the min, max, and average temperatures calculated from the given start date to the given end date
#@app.route("/api/v1.0/start-end")
#    def start-end():

# Run Flask
if __name__ == "__main__": 
    app.run(debug=True)

session.close()