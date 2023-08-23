# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """ list all available api routes."""
    return (
        f"Welcome to weather API.<br/>"
        f"Available Route.<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# this route show date and prcp from measurement table.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query date and prcp from measurement table
    prcp_date = session.query(measurement.date, measurement.prcp).all()
    session.close()

    # create a list and use for loop to add date and prcp into jsonify
    precipitation = []
    for date, prcp in prcp_date:
        date_dict = {}
        date_dict[date] = prcp
        precipitation.append(date_dict)    
    return jsonify(precipitation)
    session.close()

# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query all stations in dataset

    results = session.query(measurement.station).all()

    session.close()

    #convert list of tuple into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
    session.close()

#Query the dates and temperature observations of the most-active station 
# for the previous year of data.


@app.route('/api/v1.0/tobs')
def active_station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # get the latest date 
    latest_date = dt.date(2016,8,23)

    # get the yearly date 

    query_yearly = latest_date - dt.timedelta(days=365)

    # query tobs for the yearly most active stations

    yearly_station = session.query(measurement.date, measurement.tobs).filter_by(station="USC00519281").\
        filter(measurement.date >= query_yearly).all()

    session.close()

    # create a dictionary from row data and  append it to yearly_station_list 
    
    yearly_station_list = []
    for date, tobs in yearly_station:
        tobs_dict = {"date": date, "tobs": tobs}
        yearly_station_list.append(tobs_dict)

    return jsonify(yearly_station_list)


@app.route("/api/v1.0/<start>")
def stats(start):
    # Create our session (link) from Python to the DB
    session=Session(engine)

    #query result for min avg and max

    query_result= session.query(func.min(measurement.tobs),\
                                func.avg(measurement.tobs),\
                                    func.max(measurement.tobs).\
                                    filter(measurement.date >= start)).all()
    
    session.close()

    result_list =[]

    for min, avg, max in query_result:
        tobs_dict= {}
        tobs_dict["TMIN"] = min
        tobs_dict["TAVG"] = avg
        tobs_dict["TMAX"] = max
        result_list.append(tobs_dict)
    return jsonify(result_list)

@app.route("/api/v1.0/<start>/<end>")
def stats_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),\
                            func.avg(measurement.tobs))\
        .filter(measurement.date >= start)\
        .filter(measurement.date<= start).all()
    
    session.close()
    stats_tobs = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["TMIN"] = min
        tobs_dict["TAVG"] = avg
        tobs_dict["TMAX"] = max

        stats_tobs.append(tobs_dict)

    return jsonify(f"Start date:{start}",f"End date:{end}",stats_tobs)




session.close()
if __name__ == '__main__':
    app.run(debug=True)