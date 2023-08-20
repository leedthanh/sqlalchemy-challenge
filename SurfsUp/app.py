# Import the dependencies.
import numpy as np
import sqlalchemy
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
        f"Welcome to Hawaii climate app. <br/>"
        f"Available Route.<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/2010-01-01<br/>"
        f"/api/v1.0/start/2010-01-01/end/2017-08-23"
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





#close session and app run debug
session.close()
if __name__ == '__main__':
    app.run(debug=True)