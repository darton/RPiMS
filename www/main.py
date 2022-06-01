import os
import flask
import redis
import json
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

def get_data():
    rpims = json.loads(redis_db.get('rpims'))
    SENSORS = {}
    if rpims['setup']['use_cpu_sensor']:
        CPU_Temperature = redis_db.get('CPU_Temperature')
        SENSORS['cpu'] = {'temperature':CPU_Temperature}
    if rpims['setup']['use_dht_sensor']:
        SENSORS['dht'] = redis_db.hgetall('DHT')
    if rpims['setup']['use_door_sensor']:
        SENSORS['door_sensors'] = redis_db.hgetall('DOOR_SENSORS')
    if rpims['setup']['use_motion_sensor']:
        SENSORS['motion_sensors'] = redis_db.hgetall('MOTION_SENSORS')
    if rpims['setup']['use_bme280_sensor']:
        BME280 = {}
        if redis_db.hgetall('id1_BME280'):
            BME280['id1'] = redis_db.hgetall('id1_BME280')
        if redis_db.hgetall('id2_BME280'):
            BME280['id2'] = redis_db.hgetall('id2_BME280')
        if redis_db.hgetall('id3_BME280'):
            BME280['id3'] = redis_db.hgetall('id3_BME280')
        SENSORS['bme280'] = BME280
    data = {}
    data['config'] = rpims
    data['system'] = redis_db.hgetall('SYSTEM')
    data['system']['hostname'] = rpims['zabbix_agent']['hostname']
    data['system']['location'] = rpims['zabbix_agent']['location']
    data['sensors'] = SENSORS
    return data

@app.route('/', methods=['GET'])
def home():
    data = get_data()
    return flask.render_template('index.html',data = data)

@app.route('/api/', methods=['GET'])
def api():
    return flask.render_template('api.html')

@app.route('/api/data/all', methods=['GET'])
def api_json():
    data = get_data()
    return flask.jsonify(data)

@app.route('/api/data/sensors/<type>', methods=['GET'])
def api_sensors_json(type):
    data = get_data()
    _data = {}
    if type == 'all':
        _data = data['sensors']
    elif type == 'cpu':
        if data['config']['setup']['use_cpu_sensor']:
            _data = data['sensors']['cpu']
    elif type == 'bme280':
        if data['config']['setup']['use_bme280_sensor']:
            _data = data['sensors']['bme280']
    elif type == 'dht':
        if data['config']['setup']['use_dht_sensor']:
            _data = data['sensors']['dht']
    elif type == 'door':
        if data['config']['setup']['use_door_sensor']:
            _data = data['sensors']['door_sensors']
    elif type == 'motion':
        if data['config']['setup']['use_motion_sensor']:
            _data = data['sensors']['motion_sensors']
    else:
        _data = {}
    return flask.jsonify(_data)

@app.route('/api/data/<type>', methods=['GET'])
def api_types_json(type):
    data = get_data()
    _data = {}
    if type == 'config':
        _data = data['config']
    elif type == 'system':
        _data = data['system']
    elif type == 'sensors':
        _data = data['sensors']
    else:
        _data = {}
    return flask.jsonify(_data)
