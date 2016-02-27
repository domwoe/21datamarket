#
# Data Producer Example 
#

from subprocess import check_output

from flask import Flask
from flask import request
from flask.json import jsonify

# Import from the 21 Bitcoin Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

import json
import time

# Configure the app and wallet
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

class Sensor():


    @app.route('/info')
    def get_info():
        """Returns details about available endpoints"""

        info = { 
            'endpoints': {
                'per-req': 1,
                'returns': {
                    'name': 'timestamp',
                    'description': 'Python UTC timestamp'},
                'name': 'value',
                'description': '21BC hashrate in GH/s',
                'route': '/measurement',
                'description':'Current 21BC mininig hashrate in GH/s'
            }   
        }

        return jsonify(info)

    # Charge a fixed fee of 10 satoshis per request to the
    # /measurement endpoint

    @app.route('/measurement')
    @payment.required(1)
    def measurement():
       
        data = check_output(['21','status'])
        timestamp = time.time()

        data = str(data)
        index0 = data.find('Hashrate')
        index1 = data[index0:].find(':')
        index2 = data[index0:].find('GH/s')

        try:
          data = float(data[index0+index1+2:index0+index2-1])
         
        except:
          data = data[index0+index1+2:index0+index2-1]



        measurement = {'timestamp':timestamp,'value':data}

        measurement_json = json.dumps(measurement)

        return measurement_json

    # Initialize and run the server
    if __name__ == '__main__':
        app.run(host='0.0.0.0',port=3002)
