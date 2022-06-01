import os
import flask
#from flask import request, jsonify, render_template
import redis
import json
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

def get_data():
    config = json.loads(redis_db.get('config'))
    zabbix_agent = json.loads(redis_db.get('zabbix_agent'))
    SENSORS = {}
    if config['use_cpu_sensor']:
        CPU_Temperature = redis_db.get('CPU_Temperature')
        SENSORS['cpu'] = {'temperature':CPU_Temperature}
    if config['use_dht_sensor']:
        SENSORS['dht'] = redis_db.hgetall('DHT')
    if config['use_door_sensor']:
        SENSORS['door_sensors'] = redis_db.hgetall('DOOR_SENSORS')
    if config['use_motion_sensor']:
        SENSORS['motion_sensors'] = redis_db.hgetall('MOTION_SENSORS')
    if config['use_bme280_sensor']:
        BME280 = {}
        if redis_db.hgetall('id1_BME280'):
            BME280['id1'] = redis_db.hgetall('id1_BME280')
        if redis_db.hgetall('id2_BME280'):
            BME280['id2'] = redis_db.hgetall('id2_BME280')
        if redis_db.hgetall('id3_BME280'):
            BME280['id3'] = redis_db.hgetall('id3_BME280')
        SENSORS['bme280'] = BME280
    data = {}
    data['settings'] = config
    data['system'] = redis_db.hgetall('SYSTEM')
    data['system']['hostname'] = zabbix_agent['hostname']
    data['system']['location'] = zabbix_agent['location']
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
def api_json(option='all'):
    data = get_data()
    return data
