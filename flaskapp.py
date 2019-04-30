'''
Welcome back! Let's create an accessible API of our climate data from our 
query in SQL Alchemy using Flask. 

We will use SQL Alchemy and ORM to read our data, and create available
routes in Flask, where each function returns an API in JSON format 
from a specific query.

As a result, we will have the following available routes: 
- homepage
- precipitation data of the previous 12 months 
- temperature data of the previous 12 months 
- list of stations
- calculated tmin, tavg, tmax from a range of the start date to the most 
recent record
- calculated tmin, tavg, tmax between a specified start and end date

'''

# import dependencies 
from flask import Flask, jsonify
import json
import pandas as pd 
import numpy as np

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# initialize SQL Alchemy, sqlite database, and Base 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# initialize classes using Base
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__) 

# function to calculate tavg, tmin, tmax for start and end date
def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# homepage with list of available routes
@app.route("/")
def home():
    return(
        "<h2>Welcome to the Climate Data API</h2><br>"
        "Available routes:<br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs"
    )

# precipitation API that lists date and precipitation in JSON
@app.route("/api/v1.0/precipitation")
def precipitation():

    # query to find date and precipitation data from previous year, after 2016-08-18
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-8-18").\
        order_by(Measurement.date).all()
    
    # create list comprehension for date, precipitation 
    precipitation_date = [result[0] for result in results]
    precipitation_data = [result[1] for result in results]

    # place data in pd.DataFrame 
    precipitation_df = pd.DataFrame({
            "Date": precipitation_date, 
            "Precipitation": precipitation_data})

    # load dataframe as JSON 
    precipitation_df = json.loads(precipitation_df.to_json(orient='records'))

    # return dictionary with key containing each date, precipitation data in JSON 
    return jsonify(precipitation_df)


# station API that lists all stations from CSV file in JSON
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.id, Station.station, Station.name).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)
    
    # below is an alternative code that also works, where Python 
    # reads the CSV file and reformat into JSON 
    
    # df = pd.read_csv("Resources/hawaii_stations.csv")
    # df = json.loads(df.to_json(orient='records'))
    # return jsonify(df)

# temperature API that lists date and temperature in JSON
@app.route("/api/v1.0/tobs")
def temp():

    # query to find date and temperature data from previous year, after 2016-08-18
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-8-18").\
        order_by(Measurement.date).all()

    # create list comprehension for date, temperature
    temp_date = [result[0] for result in results]
    temp_data = [result[1] for result in results]

    # place data in pd.DataFrame 
    temp_df = pd.DataFrame({
            "Date": temp_date, 
            "Temperature": temp_data})

    # load dataframe as JSON 
    temp_df = json.loads(temp_df.to_json(orient='records'))

    # return dictionary with key containing each date, temperature data in JSON 
    return jsonify(temp_df)

# API to calculate tmin, tmax, tavg from START DATE 
@app.route("/api/v1.0/<start>")
def start_calculations(start):

    # create a query to list all dates from Measurement
    dates = session.query(Measurement.date)
    date_list =[date[0] for date in dates]

    # check if start date in date_list 
    if start in date_list:

        # perform calculation using query 
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

        # create empty list to store results
        result_calculations = []

        # create dictionary for results
        for n, a, m in results:
            calucation_start = {}
            calucation_start["Minimum Temperature"] = n
            calucation_start["Avg Temperature"] = a
            calucation_start["Max Temperature"] = m
            result_calculations.append(calucation_start)
        
        # return results in JSON
        return jsonify(result_calculations)

    # return error message if start date not in dates database
    else:
        return jsonify({"error": f"Start Date on {start} not found."}), 404

# API to calculate tmin, tmax, tavg from a range of START DATE and END DATE
@app.route("/api/v1.0/<start>/<end>")
def start_end_calculations(start, end):

    # create a query to list all dates from Measurement
    dates = session.query(Measurement.date)
    date_list =[date[0] for date in dates]

    # check if start and end date in date_list 
    if start in date_list and end in date_list:

        # perform calculation 
        results = calc_temps(start, end)

        # create empty list to store results
        final_calculations = []

        # create dictionary for results
        for n, a, m in results:
            calucation_dict = {}
            calucation_dict["Minimum Temperature"] = n
            calucation_dict["Avg Temperature"] = a
            calucation_dict["Max Temperature"] = m
            final_calculations.append(calucation_dict)

            # return results in JSON
            return jsonify(final_calculations)
    
    # return error message if start date or end date not in dates database
    else: 
        return jsonify({"error": f"Start Date on {start} or End Date {end} not found."}), 404 

if __name__ == "__main__":
    app.run(debug=True)
