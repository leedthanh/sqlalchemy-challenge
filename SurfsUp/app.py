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
        f"Welcome.<br/>"
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
    latest_date = dt.date(2017,8,23)
    sel = [measurement.date,measurement.tobs]

    # get the yearly date 

    query_yearly = latest_date - dt.timedelta(days=365)

    # query tobs for the yearly most active stations
    # yearly_station = session.query(*sel).filter(measurement.date >= query_yearly).all()

    yearly_station = session.query(measurement.date, measurement.tobs).filter_by(station="USC00519281").\
        filter(measurement.date >= query_yearly).all()

    # yearly_station=yearly_station.set_index('tobs')
    
    yearly_station_converted = list(np.ravel(yearly_station))


    session.close()

    # create a dictionary from row data and  append it to yearly_station_list 
    
    yearly_station_list = []
    for date, tobs in yearly_station_converted:
        tobs_dict = {"date": date, "tobs": tobs}
        yearly_station_list.append(tobs_dict)

    return jsonify(yearly_station_list)

@app.route("/api/v1.0/<start>")
def start_json(start):
    session=Session(engine)

    #quert data greater >= to start
    sel = [func.min(measurement.tobs).label('TMIN'),
           func.avg(measurement.tobs).label('TAVG'),
           func.max(measurement.tobs).label('TMAX')]

    #filter calculate tmin tavg and tmax

    start_json_filter = session.query(*sel).filter(measurement.data >= start).all()
    
    temp_list= []
    for i in start_json_filter:
        temp_dict = {}
        temp_dict['TMIN'] = i.TMIN
        temp_dict['TAVG'] = i.TAVG
        temp_dict['TMAX'] = i.TMAX

        temp_list.append(temp_dict)
  
    return jsonify(f"start:{start}", temp_list)
   
    

app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session.Session(engine) 
    sel = [func.min(measurement.tobs).label('TMIN'),
           func.avg(measurement.tobs).label('TAVG'),
           func.max(measurement.tobs).label('TMAX')
    ]

    start_end_filter = session.query(*sel).\
        filter(measurement.date.between(start, end)).all()
    
    temp_list = []
    for i in start_end_filter:
        temp_dict = {}
        temp_dict['TMIN'] = i.TMIN
        temp_dict['TAVG'] = i.TAVG
        temp_dict['TMAX'] = i.TMAX

        temp_list.append(temp_dict)
    
    return jsonify(f"start date:{start}", f"End date:{end}", temp_list)




    session.close()
if __name__ == '__main__':
    app.run(debug=True)