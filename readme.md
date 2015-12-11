## 21 Datamarket


The datamarket allows to publish sensors to sell their measurement data. Data requesters are able to query the datamarket for sensors and buy data directly from the sensor in peer-to-peer fashion.


### Datamarket-cli

For data producers the datamarket command line interface allows to publish and renew entries in the datamarket sensor registry

#### Publish
```bash
datamarket publish --hours=10 '{"name": "21BC hashrate", "endpoint": "htto://127.0.0.1:3002/measurement", "datatype": "float", "type":"hashrate", "unit": "GH/s", "price":2 }'
```
Publishes a sensor on the datamarket sensor registry. Entries will expire after defined hours (default is 1 hour). Each hour costs 2 Satoshis.

Returns
```bash
{"id": "56698e32961b6b64b473e71c", "expireAt": "2015-12-24 12:30:00"}
```
#### Renew

As long as a sensor is not expired it can be renewed with the following command
```bash
datamarket renew --hours=5 '56698e32961b6b64b473e71c'
```

Returns
```bash
{"id": "56698e32961b6b64b473e71c", "expireAt": "2015-12-24 17:30:00"}
```

#### Query
```bash
datamarket query '{"type": "temperature"}'
```
#### Buy
```bash
datamarket buy '56698e32961b6b64b473e71c'
```
Returns
```bash
{"timestamp": "1234123432.2342", "vakue": "52.1"}
```