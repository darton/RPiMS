import os
import yaml
import flask
import redis
import json
import requests
#from flask_wtf import FlaskForm
#from wtforms import StringField, TextAreaField, SubmitField
#from wtforms.validators import DataRequired, Email

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = 'b8f475757df5dc1cabfed8aee1ca84a6'
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
    if rpims['setup']['use_ds18b20_sensor']:
        DS18B20 = {}
        _DS18B20 = redis_db.hgetall('DS18B20')
        for k, v in _DS18B20.items():
            DS18B20[k] = {'temperature': v}
        SENSORS['one_wire'] = {'ds18b20': DS18B20 }
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
    elif type == 'ds18b20':
        if data['config']['setup']['use_ds18b20_sensor']:
            _data = data['sensors']['one_wire']['ds18b20']
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

@app.route('/setup/', methods=['GET', 'POST'])
def setup():
    data = get_data()
    if flask.request.method == "POST":
        _rpims = {}
        setup = {}
        setup['verbose'] = bool(flask.request.form.get('verbose'))
        setup['show_sys_info'] = bool(flask.request.form.get('show_sys_info'))
        setup['use_system_buttons'] = bool(flask.request.form.get('use_system_buttons'))
        setup['use_door_led_indicator'] = bool(flask.request.form.get('use_door_led_indicator'))
        setup['use_motion_led_indicator'] = bool(flask.request.form.get('use_motion_led_indicator'))
        setup['use_door_sensor'] = bool(flask.request.form.get('use_door_sensor'))
        setup['use_motion_sensor'] = bool(flask.request.form.get('use_motion_sensor'))
        setup['use_bme280_sensor'] = bool(flask.request.form.get('use_bme280_sensor'))
        setup['use_ds18b20_sensor'] = bool(flask.request.form.get('use_ds18b20_sensor'))
        setup['use_dht_sensor'] = bool(flask.request.form.get('use_dht_sensor'))
        setup['use_cpu_sensor'] = bool(flask.request.form.get('use_cpu_sensor'))
        setup['use_weather_station'] = bool(flask.request.form.get('use_weather_station'))
        setup['use_zabbix_sender'] = bool(flask.request.form.get('use_zabbix_sender'))
        setup['use_picamera'] = bool(flask.request.form.get('use_picamera'))
        setup['use_picamera_recording'] = bool(flask.request.form.get('use_picamera_recording'))
        setup['use_serial_display'] = bool(flask.request.form.get('use_serial_display'))
        setup['serial_display_refresh_rate'] = flask.request.form.get('serial_display_refresh_rate')
        setup['serial_display_rotate'] = flask.request.form.get('serial_display_rotate')
        setup['serial_display_type'] = flask.request.form.get('serial_display_type')
        setup['serial_type'] = flask.request.form.get('serial_type')
        zabbix_agent = {}
        zabbix_agent['TLSAccept'] = 'psk'
        zabbix_agent['TLSConnect'] = 'psk'
        zabbix_agent['TLSPSK'] = flask.request.form.get('TLSPSK')
        zabbix_agent['TLSPSKFile'] = '/var/www/html/conf/zabbix_agentd.psk'
        zabbix_agent['TLSPSKIdentity'] = flask.request.form.get('TLSPSKIdentity')
        zabbix_agent['Timeout'] = flask.request.form.get('Timeout')
        zabbix_agent['hostname'] = flask.request.form.get('hostname')
        zabbix_agent['location'] = flask.request.form.get('location')
        zabbix_agent['chassis'] = 'embedded'
        zabbix_agent['deployment'] = 'RPiMS'
        zabbix_agent['zabbix_server'] = flask.request.form.get('zabbix_server')
        zabbix_agent['zabbix_server_active'] = flask.request.form.get('zabbix_server_active')
        id1 = {}
        id1['i2c_address'] = flask.request.form.get('id1_BME280_i2c_address')
        id1['interface'] = flask.request.form.get('id1_BME280_interface')
        id1['name'] = flask.request.form.get('id1_BME280_name')
        id1['read_interval'] = flask.request.form.get('id1_BME280_read_interval')
        id1['use'] = bool(flask.request.form.get('id1_BME280_use'))
        id1['id'] = 'id1'
        id2 = {}
        id2['serial_port'] = flask.request.form.get('id2_BME280_serial_port')
        id2['interface'] = flask.request.form.get('id2_BME280_interface')
        id2['name'] = flask.request.form.get('id2_BME280_name')
        id2['read_interval'] = flask.request.form.get('id2_BME280_read_interval')
        id2['use'] = bool(flask.request.form.get('id2_BME280_use'))
        id2['id'] = 'id2'
        id3 = {}
        id3['serial_port'] = flask.request.form.get('id3_BME280_serial_port')
        id3['interface'] = flask.request.form.get('id3_BME280_interface')
        id3['name'] = flask.request.form.get('id3_BME280_name')
        id3['read_interval'] = flask.request.form.get('id3_BME280_read_interval')
        id3['use'] = bool(flask.request.form.get('id3_BME280_use'))
        id3['id'] = 'id3'
        BME280 = {}
        BME280['id1'] = id1
        BME280['id2'] = id2
        BME280['id3'] = id3
        CPU = {'temp': {'read_intervatl': flask.request.form.get('CPUtemp_read_interval')}}
        DHT = {}
        DHT['name'] = flask.request.form.get('DHT_name')
        DHT['pin'] = flask.request.form.get('DHT_pin')
        DHT['read_interval'] = flask.request.form.get('DHT_read_interval')
        DHT['type'] = flask.request.form.get('DHT_type')
        DS18B20 = {}
        DS18B20['read_interval'] = flask.request.form.get('DS18B20_read_interval')
        for item in data['sensors']['one_wire']['ds18b20']:
            DS18B20[item]= {'name': flask.request.form.get('DS18B20_'+ str(item) + '_name')}
        ONE_WIRE = {}
        ONE_WIRE['DS18B20'] = DS18B20
        PICAMERA = {}
        PICAMERA['fps'] = flask.request.form.get('picamera_fps')
        PICAMERA['mode'] = flask.request.form.get('picamera_mode')
        PICAMERA['rotation'] = flask.request.form.get('picamera_rotation')
        RAINFALL = {}
        RAINFALL['acquisition_time'] = flask.request.form.get('rainfall_acquisition_time')
        RAINFALL['agregation_time'] = flask.request.form.get('rainfall_agregation_time')
        RAINFALL['sensor_pin'] = flask.request.form.get('rainfall_sensor_pin')
        RAINFALL['use'] = bool(flask.request.form.get('rainfall_use'))
        DIRECTION = {}
        DIRECTION['acquisition_time'] = flask.request.form.get('winddirection_acquisition_time')
        DIRECTION['adc_input'] = flask.request.form.get('winddirection_adc_input')
        DIRECTION['adc_type'] = flask.request.form.get('winddirection_adc_type')
        DIRECTION['reference_voltage_adc_input'] = flask.request.form.get('reference_voltage_adc_input')
        DIRECTION['use'] = bool(flask.request.form.get('winddirection_use'))
        SPEED = {}
        SPEED['acquisition_time'] = flask.request.form.get('windspeed_acquisition_time')
        SPEED['agregation_time'] = flask.request.form.get('windspeed_agregation_time')
        SPEED['sensor_pin'] = flask.request.form.get('windspeed_sensor_pin')
        SPEED['use'] = bool(flask.request.form.get('windspeed_use'))
        WIND = {}
        WIND['DIRECTION'] = DIRECTION
        WIND['SPEED'] =SPEED
        WEATHER = {}
        WEATHER['RAINFALL'] = RAINFALL
        WEATHER['WIND'] = WIND
        sensors = {}
        sensors['BME280'] = BME280
        sensors['CPU'] = CPU
        sensors['DHT'] = DHT
        sensors['ONE_WIRE'] = ONE_WIRE
        sensors['PICAMERA'] = PICAMERA
        sensors['WEATHER'] = WEATHER
        _rpims['sensors'] = sensors
        _rpims['zabbix_agent'] = zabbix_agent
        _rpims['setup'] = setup
        with open('conf/_rpims.yaml','w') as f:
            yaml.dump(_rpims, f, default_flow_style=False)
        return flask.jsonify(_rpims)
    return flask.render_template('setup.html',data = data)
