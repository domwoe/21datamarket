#
# Datamarket Command Line Interface
#

import sys
import json
import click
import os

#import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests
from two1.lib.bitcoin.crypto import PublicKeyBase

#from daemon import Daemon
#from sensor import Sensor

#set up bitrequest client for BitTransfer requests:
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

# URL of datamarket backend
server_url = 'http://10.147.17.77:3100/'

valid_keys = [ 'name', 'endpoint', 'datatype', 'location', 'description', 'type','unit','price','min','max','interval','accuracy','manufacturer']
mandatory_keys = ['name', 'endpoint','datatype','type','unit','price']

# Example
# '{"name": "21BC hashrate", "endpoint": "htto://127.0.0.1:3002/measurement", "datatype": "float", "type":"hashrate", "unit": "GH/s", "price":2 }'
#


#class SensorDaemon(Daemon):
#        my_sensor = Sensor()

#daemon = SensorDaemon('/tmp/sensor.pid')

@click.group()
def cli():
	"""Datamarket Command Line Interface (CLI)"""

@click.command(name='publish')
@click.argument('sensor')
@click.option('--hours', default=1, type=int)
def cmd_publish(sensor,hours):
	"""Publish a sensor"""

	if sensor == '':

		name = click.promt('Please enter a name for your sensor', type=str)
		endpoint = click.promt('Measurement endpoint (e.g. http://10.5.20.6:3001/measurement)', type=str)
		price = click.promt('Price per measurement in satoshi', type=int)
		mtype = click.promt('Measurement type (e.g. temperature)', type=str)
		unit = click.promt('Measurement type (e.g. Kelvin)', type=str)
		datatype = click.promt('Data type (e.g. float)', type=str)

		sensor = { 'name': name, 'endpoint': endpoint, 'price': price, 'datatype': datatype, 'type': mtype, 'unit':unit}


	if isinstance(sensor, str):
		sensor = json.loads(sensor)

	sensor_keys = list(sensor.keys())

	# check if all mandatory keys are set
	for key in mandatory_keys:
		if key not in sensor_keys:
			print(key + " is mandatory.")
			raise SystemExit

	# check if there are only valid keys
	for key in sensor_keys:
		if key not in valid_keys:
			print(key + " is not allowed.")
			raise SystemExit

	#sensor['public_key'] = wallet.get_message_signing_public_key()

	# Encode to json object
	sensor_json = json.dumps(sensor)

	url = server_url+'publish?hours={0}'
	response = requests.post(url=url.format(hours),data = sensor_json)
	click.echo(response.text)

@click.command(name='renew')
@click.argument('sensor')
@click.option('--hours', default=1, type=int)
def cmd_renew(sensor, hours):
	"""Renew entry in sensor registry by hours"""

	url = server_url + 'renew?id={0}&hours={1}'
	response = requests.get(url=url.format(sensor, hours))

	click.echo(response.json())

@click.command(name='query')
@click.argument('query')
def cmd_query(query):
	"""Query sensor registry"""

	url = server_url+'query?query={0}'
	response = requests.get(url=url.format(query))
	click.echo(response.text)


@click.command(name='buy')
@click.argument('sensor', default='')
def cmd_buy(sensor):
	"""Buy measurement from sensor by id or endpoint"""

	if sensor == '':
		# Is piped from query
		try:
			sensors = sys.stdin.read()
		except:
			click.echo('Unknown input for buy')
			raise SystemExit

		sensors = json.loads(sensors)

		for sensor in sensors:
			try:
				endpoint = sensor['endpoint']
				response = requests.get(url=endpoint)
				data = json.loads(response.text)
				data['sensor_id'] = sensor['_id']['$oid']
				click.echo(json.dumps(data))
			except:
				click.echo('No endpoint')
	
	else:

		if sensor.find('.') == -1 & sensor.find(':') == -1:
			# is a sensor id 
			sensor_id = sensor
			url = server_url+'endpoint?id={0}'

			response = requests.get(url=url.format(sensor_id))

			try:
				endpoint = response.text
			except:
				click.echo('Sensor not found or no valid endpoint')
				raise SystemExit
		else:
			# is a endpoint url
			endpoint = sensor

		response = requests.get(url=endpoint)

		click.echo(response.json())

@click.command(name='open')
def cmd_open():
	"""Open sensor endpoint"""
	os.system("python3 sensor.py > sensor.log &")


@click.command(name='close')
def cmd_close():
	"""Close sensor endpoint"""
	daemon.stop()		



	 

cli.add_command(cmd_publish)
cli.add_command(cmd_renew)
cli.add_command(cmd_query)
cli.add_command(cmd_buy)
cli.add_command(cmd_open)
cli.add_command(cmd_close)

if __name__ == "__main__":
	cli()
