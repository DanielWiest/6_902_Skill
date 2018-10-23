from flask import Flask
from flask import jsonify
from APIHitterShuttle import nextArrivalTimeAt
from APIHitterLaundry import getLaundryStatus
from APIHitterEvents import fetchUpcomingMITEvents
from APIHitterDining import callableThing
import os

app = Flask(__name__)


@app.route('/shuttle/<stop>')
def handleShuttle(stop):
    response = nextArrivalTimeAt(stop)
    return jsonify([response])

@app.route('/washing/<dorm>')
def handleWasher(dorm):
    return jsonify([getLaundryStatus(dorm,True,False)])

@app.route('/drying/<dorm>')
def handleDryer(dorm):
    return jsonify([getLaundryStatus(dorm,False,True)])

@app.route('/events')
def handleEvents():
    aribitraryNumber = 5
    return jsonify([fetchUpcomingMITEvents(aribitraryNumber)])

@app.route('/dining/<location>/<meal>')
def handleDining(meal,location):
    CAFE_NAMES = ['the-howard-dining-hall-at-maseeh','next','simmons',]
    response = callableThing(meal,location)
    return jsonify([response])


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000)) #The port to be listening to — hence, the URL must be <hostname>:<port>/ inorder to send the request to this program
	app.run(host='0.0.0.0', port=port)  #Start listening