import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Query to retrieve the last 12 months of precipitation data
    precip_scores = session.query(measurement.date,measurement.prcp).\
        filter(measurement.date > one_year).\
        order_by(measurement.date).all()
    
    # Convert list of tuples into normal list
    list_convert_1 = list(np.ravel(precip_scores))
    
    return jsonify(list_convert_1)

@app.route("/api/v1.0/stations")
def stations():
    
    # Query to retrieve the station data
    station_names = session.query(station.station,station.name).all()
    
    # Convert list of tuples into normal list
    list_convert_2 = list(np.ravel(station_names)
    
    return jsonify(list_convert_2)

@app.route("/api/v1.0/tobs")
def tobs():
    
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Query the dates and temperature observations of the most active station for the last year of data
    temp_obs = session.query(measurement.date,measurement.tobs).\
        filter(measurement.date > one_year,measurement.station == "USC00519281").all()
    
    # Convert list of tuples into normal list
    list_convert_3 = list(np.ravel(temp_obs))
    
    return jsonify(list_convert_3)                      
    
@app.route("/api/v1.0/<start>")
def start(start_date):
    
    # Query using the station id from the previous query, calculate the lowest temperature recorded, 
    # highest temperature recorded, and average temperature of the most active station
    
    temp_query = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    
    # Convert list of tuples into normal list
    list_convert_4 = list(np.ravel(temp_query))                      
                          
    return jsonify(list_convert_4)                

@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date,end_date):
    
    # Query when given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start 
    #and end date inclusive                      
    temp_query_2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
                          
    # Convert list of tuples into normal list
    list_convert_5 = list(np.ravel(temp_query_2))
    
    return jsonify(list_convert_5)
                          
if __name__ == "__main__":
    app.run(debug = True)