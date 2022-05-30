import os
import flask
from flask import request, jsonify, render_template
import redis
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
    config = json.loads(redis_db.get('config'))
    gpio = json.loads(redis_db.get('gpio'))
    sensors = json.loads(redis_db.get('sensors'))
    DOOR_SENSORS = redis_db.hgetall('DOOR_SENSORS')
    MOTION_SENSORS = redis_db.hgetall('MOTION_SENSORS')
    DHT = redis_db.hgetall('DHT')
    return render_template('index.html', ds = DOOR_SENSORS, ms = MOTION_SENSORS, dht = DHT)

@app.route('/api/', methods=['GET'])
def api():
    return render_template('api.html')

@app.route('/api/data/all', methods=['GET'])
def get_data(option='all'):
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
    #get config data
    config = json.loads(redis_db.get('config'))
    zabbix_agent = json.loads(redis_db.get('zabbix_agent'))
    #gpio = json.loads(redis_db.get('gpio'))
    #sensors = json.loads(redis_db.get('sensors'))

    SENSORS = {}
    if config['use_cpu_sensor']:
        CPU_Temperature = redis_db.get('CPU_Temperature')
        SENSORS['cpu'] = {'temperature':CPU_Temperature}
    if config['use_dht_sensor']:
        #DHT = redis_db.hgetall('DHT')
        #SENSORS['dht'] = {**DHT}
        SENSORS['dht'] = redis_db.hgetall('DHT')
    if config['use_door_sensor']:
        #DOOR_SENSORS = redis_db.hgetall('DOOR_SENSORS')
        #SENSORS['door_sensors'] = {**DOOR_SENSORS}
        SENSORS['door_sensors'] = redis_db.hgetall('DOOR_SENSORS')
    if config['use_motion_sensor']:
        #MOTION_SENSORS = redis_db.hgetall('MOTION_SENSORS')
        #SENSORS['motion_sensors'] = {**MOTION_SENSORS}
        SENSORS['motion_sensors'] = redis_db.hgetall('MOTION_SENSORS')
    alldata = {}
    alldata['settings'] = config
    alldata['system'] = redis_db.hgetall('SYSTEM')
    alldata['system']['hostname'] = zabbix_agent['hostname']
    alldata['system']['location'] = zabbix_agent['location']
    alldata['sensors'] = SENSORS
    return alldata

@app.route('/api/data/sensors', methods=['GET'])
def api_sensors():
    return sensors

@app.route('/api/data/sensors/bme280', methods=['GET'])
def api_bme280():
    return sensors['BME280']

@app.route('/api/data/sensors/cpu', methods=['GET'])
def api_cpu():
    return sensors['CPU']

@app.route('/api/data/sensors/dht', methods=['GET'])
def api_dht():
    return sensors['DHT']

@app.route('/api/data/sensors/ds18b20', methods=['GET'])
def api_ds18b20():
    return sensors['ONE_WIRE']

@app.route('/api/data/sensors/gpio', methods=['GET'])
def api_gpio():
    return gpio

@app.route('/api/data/sensors/config', methods=['GET'])
def api_config():
    return config
