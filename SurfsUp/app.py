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

@app.route("/api/v1.0/precipitation")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query date and prcp from measurement table
    prcp_date = session.query(measurement.date, measurement.prcp).all()
    session.close()

    precipitation = []
    for date, prcp in prcp_date:
        date_dict = {}
        date_dict[date] = prcp
        precipitation.append(date_dict)    
    return jsonify(precipitation)


#close session and app run debug
session.close()
if __name__ == '__main__':
    app.run(debug=True)