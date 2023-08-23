
Using Python and SQLAlchemy ORM queries, Pandas, and Matplotlib to do basic climate
analysis and data exploration.

Design basic climate app using Flask API based on the queries developed.  
used Flask to create routes as follows:
/start at homepage
list all available routes
/api/v1.0/precipitation
convert query results from precipitation analysis 

/api/v1.0/stations
return a JSON list of stations from the dataset.

/api/v1.0/tobs
query the dates and temperature observations for the most active station
for the previous year of data.  Return a JSON list of temerature observations
for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>
return a JSON list of the minumum temperature the average temperature and the
maximum temperature for a specified start or start-end range 







