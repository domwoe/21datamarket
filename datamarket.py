# 
# Datamarket Sensor Registry
#

from flask import Flask
from flask import request
from flask.json import jsonify

# Import from the 21 Bitcoin Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

from pymongo import MongoClient

from datetime import datetime, timedelta
import json
from bson import json_util

# Configure the app and wallet
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

# Sensor registry database
db_client = MongoClient('localhost', 27017)
registry = db_client.registry # database
sensors = registry.sensors # collection


def valid_publish_request(request):
	"""Checks if request is a valid publish request"""
    # TODO
	return True

def get_publish_price(request):
    """Calculates price according to hours to be registered"""
    if not valid_publish_request(request):
        return "invalid publish request"

    hours = int(request.args.get('hours'))

    price = hours * 2                # 2 satoshis per hour

    if price < 2:
        price = 2
    return price

@app.route('/publish', methods=['POST'])
@payment.required(get_publish_price)
def add_sensor():
    """"Add sensor to sensor registry"""

    sensor = request.data.decode('utf-8')

    hours = int(request.args.get('hours'))

    expire_date = datetime.now() + timedelta(hours=hours)

    print(sensor)
    sensor = json.loads(sensor)
    sensor['expireAt'] = expire_date

    sensor_id = sensors.insert_one(sensor).inserted_id
    print(sensor_id)

    return json.dumps({'sensor_id' : str(sensor_id), 'expireAt': expire_date.strftime("%Y-%m-%d %H:%M:%S")})

@app.route('/renew')
@payment.required(get_publish_price)
def renew_sensor():
    """Renew sensor in registry"""

    sensor_id = request.args.get('sensor')
    hours = int(request.args.get('hours'))

    entry = sensors.find_one(ObjectId(sensor))
    expire_date = entry['expireAt']
    expire_date = expire_date + timedelta(hours=hours)

    result = sensors.update_one(ObjectId(sensor),{"$set": {"expireAt": expire_date}})

    return jsonify(result)

@app.route('/query')
def query_registry():
    """Query sensor registry"""

    query = json.loads(request.args.get('query'))

    results = sensors.find(query)

    json_docs = []
    for doc in results:
        #doc.pop("expireAt",None)
        json_doc = json.dumps(doc, default=json_util.default)
        json_docs.append(json_doc)

    return jsonify({'results':json_docs})


# Initialize and run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3100, debug=True)