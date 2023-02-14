import os
import yaml
import flask
import redis
import json
import requests
from time import sleep
#from flask_wtf import FlaskForm
#from wtforms import StringField, TextAreaField, SubmitField
#from wtforms.validators import DataRequired, Email

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = 'b8f475757df5dc1cabfed8aee1ca84a6'
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"


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
    if rpims['setup']['use_weather_station']:
      WEATHER = redis_db.hgetall('WEATHER')
      SENSORS['weather_station'] = WEATHER
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
    response = flask.jsonify(data)
    response.status_code = 200
    #response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


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
    elif type == 'weather-station':
        if data['config']['setup']['use_weather_station']:
            _data = data['sensors']['weather_station']
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
    try:
        import sys
        import yaml
        from systemd import journal
        config = {}
        _DS18B20 = redis_db.hgetall('DS18B20')
        path_to_config = '/var/www/html/conf/rpims.yaml'
        with open(path_to_config, 'r') as f:
            config = yaml.full_load(f)
    except Exception as error:
        #error = f"Can't load RPiMS config file: {path_to_config}"
        journal.send(error)
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
        setup['serial_display_type'] = flask.request.form.get('serial_display_type')
        setup['serial_type'] = flask.request.form.get('serial_type')
        setup['serial_display_refresh_rate'] = int(flask.request.form.get('serial_display_refresh_rate'))
        setup['serial_display_rotate'] = int(flask.request.form.get('serial_display_rotate'))
        zabbix_agent = {}
        zabbix_agent['TLSAccept'] = 'psk'
        zabbix_agent['TLSConnect'] = 'psk'
        zabbix_agent['TLSPSK'] = flask.request.form.get('TLSPSK')
        zabbix_agent['TLSPSKFile'] = '/var/www/html/conf/zabbix_agentd.psk'
        zabbix_agent['TLSPSKIdentity'] = flask.request.form.get('TLSPSKIdentity')
        zabbix_agent['Timeout'] = int(flask.request.form.get('Timeout'))
        zabbix_agent['hostname'] = flask.request.form.get('hostname')
        zabbix_agent['location'] = flask.request.form.get('location')
        zabbix_agent['chassis'] = 'embedded'
        zabbix_agent['deployment'] = 'RPiMS'
        zabbix_agent['zabbix_server'] = flask.request.form.get('zabbix_server')
        zabbix_agent['zabbix_server_active'] = flask.request.form.get('zabbix_server_active')
        id1 = {}
        id1['i2c_address'] = int(flask.request.form.get('id1_BME280_i2c_address'))
        id1['interface'] = flask.request.form.get('id1_BME280_interface')
        id1['name'] = flask.request.form.get('id1_BME280_name')
        id1['read_interval'] = int(flask.request.form.get('id1_BME280_read_interval'))
        id1['use'] = bool(flask.request.form.get('id1_BME280_use'))
        id1['id'] = 'id1'
        id2 = {}
        id2['serial_port'] = flask.request.form.get('id2_BME280_serial_port')
        id2['interface'] = flask.request.form.get('id2_BME280_interface')
        id2['name'] = flask.request.form.get('id2_BME280_name')
        id2['read_interval'] = int(flask.request.form.get('id2_BME280_read_interval'))
        id2['use'] = bool(flask.request.form.get('id2_BME280_use'))
        id2['id'] = 'id2'
        id3 = {}
        id3['serial_port'] = flask.request.form.get('id3_BME280_serial_port')
        id3['interface'] = flask.request.form.get('id3_BME280_interface')
        id3['name'] = flask.request.form.get('id3_BME280_name')
        id3['read_interval'] = int(flask.request.form.get('id3_BME280_read_interval'))
        id3['use'] = bool(flask.request.form.get('id3_BME280_use'))
        id3['id'] = 'id3'
        BME280 = {}
        BME280['id1'] = id1
        BME280['id2'] = id2
        BME280['id3'] = id3

        CPU = {'temp': {'read_interval': int(flask.request.form.get('CPUtemp_read_interval'))}}

        DHT = {}
        DHT['name'] = flask.request.form.get('DHT_name')
        DHT['pin'] = int(flask.request.form.get('DHT_pin'))
        DHT['read_interval'] = int(flask.request.form.get('DHT_read_interval'))
        DHT['type'] = flask.request.form.get('DHT_type')


        gpios = ['GPIO_5','GPIO_6','GPIO_12','GPIO_13','GPIO_16','GPIO_18','GPIO_19','GPIO_20','GPIO_21','GPIO_26']
        gpio = {}
        for item in gpios:
            a = {}
            a['pin'] = int(flask.request.form.get(str(item) +'_pin'))
            a['type'] = flask.request.form.get(str(item) +'_type')
            a['name'] = flask.request.form.get(str(item) +'_name')
            a['hold_time'] = int(flask.request.form.get(str(item) +'_hold_time')) if flask.request.form.get(str(item) +'_hold_time') != '' else ''
            gpio[item] = a 

        PICAMERA = {}
        PICAMERA['fps'] = int(flask.request.form.get('picamera_fps'))
        PICAMERA['mode'] = int(flask.request.form.get('picamera_mode'))
        PICAMERA['rotation'] = int(flask.request.form.get('picamera_rotation'))

        picamera_mode = int(flask.request.form.get('picamera_mode'))
        picamera_modes = {
            1: [1920,1080],
            6: [1280,720],
            7: [640,480],
        }
        picamera_width = picamera_modes[picamera_mode][0]
        picamera_height = picamera_modes[picamera_mode][1]
        PICAMERA['vr'] = picamera_height
        PICAMERA['hr'] = picamera_width

        RAINFALL = {}
        RAINFALL['acquisition_time'] = int(flask.request.form.get('rainfall_acquisition_time'))
        RAINFALL['agregation_time'] = int(flask.request.form.get('rainfall_agregation_time'))
        RAINFALL['sensor_pin'] = int(flask.request.form.get('rainfall_sensor_pin'))
        RAINFALL['use'] = bool(flask.request.form.get('rainfall_use'))

        DIRECTION = {}
        DIRECTION['acquisition_time'] = int(flask.request.form.get('winddirection_acquisition_time'))
        DIRECTION['adc_input'] = int(flask.request.form.get('winddirection_adc_input'))
        DIRECTION['adc_type'] = flask.request.form.get('winddirection_adc_type')
        DIRECTION['reference_voltage_adc_input'] = int(flask.request.form.get('reference_voltage_adc_input'))
        DIRECTION['use'] = bool(flask.request.form.get('winddirection_use'))
        SPEED = {}
        SPEED['acquisition_time'] = int(flask.request.form.get('windspeed_acquisition_time'))
        SPEED['agregation_time'] = int(flask.request.form.get('windspeed_agregation_time'))
        SPEED['sensor_pin'] = int(flask.request.form.get('windspeed_sensor_pin'))
        SPEED['use'] = bool(flask.request.form.get('windspeed_use'))
        WIND = {}
        WIND['DIRECTION'] = DIRECTION
        WIND['SPEED'] =SPEED
        WEATHER = {}
        WEATHER['RAINFALL'] = RAINFALL
        WEATHER['WIND'] = WIND

        sensors = {}
        sensors['CPU'] = CPU
        sensors['PICAMERA'] = PICAMERA
        sensors['BME280'] = BME280

        DS18B20 = {}
        addresses = {}
        DS18B20['addresses'] = addresses
        DS18B20['read_interval'] = 2
        if bool(flask.request.form.get('use_ds18b20_sensor')):
            DS18B20['read_interval'] = int(flask.request.form.get('DS18B20_read_interval'))
            for item in flask.request.form.getlist('DS18B20_address'):
                addresses[item]= {'name': flask.request.form.get('DS18B20_'+ str(item) + '_name')}
            DS18B20['addresses'] = addresses
        ONE_WIRE = {}
        ONE_WIRE['DS18B20'] = DS18B20
        sensors['ONE_WIRE'] = ONE_WIRE

        sensors['DHT'] = DHT
        sensors['WEATHER'] = WEATHER

        _rpims['setup'] = setup
        _rpims['sensors'] = sensors
        _rpims['gpio'] = gpio
        _rpims['zabbix_agent'] = zabbix_agent


        zabbix_config = []
        zabbix_config.append(f'Server=127.0.0.1,{zabbix_agent.get("zabbix_server")}')
        zabbix_config.append(f'ServerActive={zabbix_agent.get("zabbix_server_active")}')
        zabbix_config.append(f'Hostname={zabbix_agent.get("hostname")}')
        zabbix_config.append(f'TLSPSKIdentity={zabbix_agent.get("TLSPSKIdentity")}')
        zabbix_config.append(f'TLSPSKFile={zabbix_agent.get("TLSPSKFile")}')
        zabbix_config.append(f'TLSConnect={zabbix_agent.get("TLSConnect")}')
        zabbix_config.append(f'TLSAccept={zabbix_agent.get("TLSAccept")}')
        zabbix_config.append(f'Timeout={zabbix_agent.get("Timeout")}')
        with open('conf/zabbix_agentd.conf', 'w', encoding='utf-8') as f:
          f.write('\n'.join(zabbix_config))

        with open('conf/zabbix_agentd.psk', 'w', encoding='utf-8') as f:
          f.write(zabbix_agent.get("TLSPSK"))

        uv4l_raspicam_config = []
        uv4l_raspicam_config.append('# uv4l core options')
        uv4l_raspicam_config.append('driver = raspicam')
        uv4l_raspicam_config.append('auto-video_nr = yes')
        uv4l_raspicam_config.append('frame-buffers = 4')
        uv4l_raspicam_config.append('encoding = mjpeg')
        uv4l_raspicam_config.append('nopreview = yes')
        uv4l_raspicam_config.append('video-denoise = no')
        uv4l_raspicam_config.append('server-option = --www-webrtc-signaling-path=/webrtc')
        uv4l_raspicam_config.append(f'rotation = {int(flask.request.form.get("picamera_rotation"))}')

        uv4l_raspicam_config.append(f'width = {picamera_width}')
        uv4l_raspicam_config.append(f'height = {picamera_height}')
        uv4l_raspicam_config.append(f'framerate = {int(flask.request.form.get("picamera_fps"))}')
        with open('conf/uv4l-raspicam.conf', 'w', encoding='utf-8') as f:
          f.write('\n'.join(uv4l_raspicam_config))

        redis_db.set('rpims', json.dumps(_rpims))
        with open('conf/rpims.yaml','w') as f:
            yaml.dump(_rpims, f, default_flow_style=False, sort_keys=False, explicit_start=True)
        #return flask.jsonify(_rpims)

        sleep(2)
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('setup.html',config = config, _DS18B20 = _DS18B20)
