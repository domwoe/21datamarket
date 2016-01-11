## 21 Datamarket

The Internet of Things is digitalizing the physical world we are living in. Real-time measurement data from billions of devices will be the basis for better decisions. However, real-time measurement data has to be available publicly to unleash their full potential. Therefore, sensors have to be compensated for providing this service.

The 21 datamarket allows to publish sensors to sell their measurement data. Data requesters are able to query the datamarket for sensors and buy data directly from the sensor in peer-to-peer fashion.

In this repository you'll find a simple implementation of this concept. I'd be very happy to receive feedback and suggestions. 


### Datamarket-cli

For data producers the datamarket command line interface allows to publish and renew entries in the datamarket sensor registry

#### Installation

```bash
git clone https://github.com/domwoe/21datamarket.git
cd ./21datamarket
sudo pip3 install --editable .
```

#### Usage

##### Publish
```bash
datamarket publish --hours=10 '{"name": "21BC hashrate", "endpoint": "http://10.147.17.77:3002/measurement", "datatype": "float", "type":"hashrate", "unit": "GH/s", "price":2 }'
```
Publishes a sensor on the datamarket sensor registry. Entries will expire after defined hours (default is 1 hour). Each hour costs 2 Satoshis.

Returns
```bash
{"id": "56698e32961b6b64b473e71c", "expireAt": "2015-12-24 12:30:00"}
```
##### Renew

As long as a sensor is not expired it can be renewed with the following command
```bash
datamarket renew --hours=5 '56698e32961b6b64b473e71c'
```

Returns
```bash
{"id": "56698e32961b6b64b473e71c", "expireAt": "2015-12-24 17:30:00"}
```

##### Query
```bash
datamarket query '{"type": "temperature"}'
```
##### Buy

The buy command can currently be used with a sensor id or an endpoint url.
```bash
datamarket buy '56698e32961b6b64b473e71c'
```
Returns
```bash
{"timestamp": "1234123432.2342", "value": "52.1"}
```
Moreover, you can pipe the results of a query directly to the buy command.

Alternatively sensor data can be bought using the 21 buy command and the endpoint url
```bash
21 buy url http://10.147.17.77:3002/measurement
```

### Data producer


### Datamarket sensor registry


