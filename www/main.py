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
#    return '''<h1>Distant Reading Archive</h1>
#<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/', methods=['GET'])
def api():
    return render_template('api.html')

@app.route('/api/data/all', methods=['GET'])
def get_data():
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
#get config data
    config = json.loads(redis_db.get('config'))
    gpio = json.loads(redis_db.get('gpio'))
    sensors = json.loads(redis_db.get('sensors'))
    zabbix_agent = json.loads(redis_db.get('zabbix_agent'))
#get dynamic values
    SYSTEM = redis_db.hgetall('SYSTEM')
    DOOR_SENSORS = redis_db.hgetall('DOOR_SENSORS')
    MOTION_SENSORS = redis_db.hgetall('MOTION_SENSORS')
    CPU_Temperature = redis_db.get('CPU_Temperature')
    DHT = redis_db.hgetall('DHT')
    #SENSORS = {'sensors':{'cpu':{'temperature':CPU_Temperature}}}
    #allsensors = {**gpio, **sensors}
#Concatenation
    alldata = {'settings':{**config},'system':{**zabbix_agent,**SYSTEM},'sensors':{'cpu':{'temperature':CPU_Temperature},'dht':{**DHT},'door_sensors':{**DOOR_SENSORS},'motion_sensors':{**MOTION_SENSORS}}}
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

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_allbooks():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

