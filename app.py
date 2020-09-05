# 1. Import Flask
from flask import Flask,jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def index():

    home = (
        '/api/v1.0/precipitation<br>'
        '/api/v1.0/stations<br>'
        '/api/v1.0/tobs<br>'
        '/api/v1.0/start-date/end-date'
    )
    return home

@app.route("/api/v1.0/precipitation")
def prcp():
    result = session.query(measurement.date,measurement.prcp).all()

    obj = { date:prcp for (date,prcp) in result }

    return jsonify(obj)

@app.route("/api/v1.0/stations")
def stations():
    result = session.query(station.station,station.name).all()

    return jsonify(result)

@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate a year since last date in data
    lastDate = session.query(func.max(measurement.date)).first()[0]
    lastDate = dt.datetime.strptime(lastDate,'%Y-%m-%d')
    priorYear = lastDate - dt.timedelta(days=365)

    # Calculate the most active station
    mostActive = session.query(measurement.station).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()[0]

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    
    prevYearTobs = session.query(measurement.tobs).filter((measurement.date >= priorYear) & (measurement.station == mostActive)).all()

    return jsonify(prevYearTobs)

@app.route('/api/v1.0/<start>/<end>')
@app.route('/api/v1.0/<start>')
def fromTo(start,end='2017-08-23'):

    result = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).filter((measurement.date>=start) & (measurement.date<=end)).all()

    return jsonify(result)



# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
