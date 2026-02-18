"""
Refactored Flask application (Step 1)
-------------------------------------
This version keeps everything in a single file, but reorganizes the code
to be cleaner, more maintainable, and ready for future modularization
(blueprints, services, config modules, etc.).
"""

# ============================
# Imports
# ============================

# Standard library
import os
import json

# Third‑party libraries
import flask
import redis
import yaml
from ruamel.yaml import YAML
from systemd import journal


# ============================
# Configuration & Constants
# ============================

BASE_DIR = os.environ.get("RPIMS_DIR", os.getcwd())

CONFIG_PATH = f"{BASE_DIR}/config/rpims.yaml"
ZABBIX_CONF = f"{BASE_DIR}/config/zabbix_rpims.conf"
ZABBIX_PSK = f"{BASE_DIR}/config/zabbix_rpims.psk"
MEDIAMTX_CONFIG = "/etc/mediamtx/mediamtx.yml"

# Flask app initialization
app = flask.Flask(__name__)
app.config.update(
    SECRET_KEY="b8f475757df5dc1cabfed8aee1ca84a6",
    DEBUG=True,
    JSON_AS_ASCII=False,
    JSONIFY_MIMETYPE="application/json; charset=utf-8",
)


# ============================
# Redis helper
# ============================

def get_redis():
    """Return a Redis connection instance."""
    return redis.StrictRedis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )


redis_db = get_redis()


# ============================
# Utility functions
# ============================

def bool_to_yesno(value: bool) -> str:
    """Convert boolean to 'yes'/'no' string."""
    return "yes" if value else "no"


# ============================
# Sensor loading helpers
# ============================

def load_cpu_sensor(redis_db, config):
    """Load CPU temperature sensor data."""
    if not config["setup"]["use_cpu_sensor"]:
        return None
    return {"temperature": redis_db.get("CPU_Temperature")}


def load_dht_sensor(redis_db, config):
    if not config["setup"]["use_dht_sensor"]:
        return None
    return redis_db.hgetall("DHT")


def load_door_sensor(redis_db, config):
    if not config["setup"]["use_door_sensor"]:
        return None
    return redis_db.hgetall("DOOR_SENSORS")


def load_motion_sensor(redis_db, config):
    if not config["setup"]["use_motion_sensor"]:
        return None
    return redis_db.hgetall("MOTION_SENSORS")


def load_bme280_sensor(redis_db, config):
    if not config["setup"]["use_bme280_sensor"]:
        return None

    result = {}
    for sensor_id in ("id1", "id2", "id3"):
        key = f"{sensor_id}_BME280"
        data = redis_db.hgetall(key)
        if data:
            result[sensor_id] = data
    return result


def load_ds18b20_sensor(redis_db, config):
    if not config["setup"]["use_ds18b20_sensor"]:
        return None

    raw = redis_db.hgetall("DS18B20")
    return {k: {"temperature": v} for k, v in raw.items()}


def load_weather_station(redis_db, config):
    if not config["setup"]["use_weather_station"]:
        return None
    return redis_db.hgetall("WEATHER")


def get_sensors(redis_db, config):
    """Load all sensors based on configuration flags."""
    sensors = {}

    if (cpu := load_cpu_sensor(redis_db, config)):
        sensors["cpu"] = cpu

    if (dht := load_dht_sensor(redis_db, config)):
        sensors["dht"] = dht

    if (door := load_door_sensor(redis_db, config)):
        sensors["door_sensors"] = door

    if (motion := load_motion_sensor(redis_db, config)):
        sensors["motion_sensors"] = motion

    if (bme := load_bme280_sensor(redis_db, config)):
        sensors["bme280"] = bme

    if (ds := load_ds18b20_sensor(redis_db, config)):
        sensors["one_wire"] = {"ds18b20": ds}

    if (weather := load_weather_station(redis_db, config)):
        sensors["weather_station"] = weather

    return sensors


# ============================
# Data aggregation
# ============================

def get_data():
    """Aggregate all system, config and sensor data into a single structure."""
    rpims = json.loads(redis_db.get("rpims"))

    system_info = redis_db.hgetall("SYSTEM")
    system_info["hostname"] = rpims["zabbix_agent"]["hostname"]
    system_info["location"] = rpims["zabbix_agent"]["location"]

    return {
        "config": rpims,
        "system": system_info,
        "sensors": get_sensors(redis_db, rpims),
    }


# ============================
# MediaMTX configuration update
# ============================

def update_mediamtx_config(width, height, fps, recording, vflip, hflip):
    """Update MediaMTX YAML configuration for PiCamera."""
    yaml_loader = YAML()
    yaml_loader.preserve_quotes = True

    with open(MEDIAMTX_CONFIG, "r", encoding="utf-8") as f:
        config = yaml_loader.load(f)

    config["pathDefaults"]["rpiCameraWidth"] = width
    config["pathDefaults"]["rpiCameraHeight"] = height
    config["pathDefaults"]["rpiCameraFPS"] = fps
    config["pathDefaults"]["record"] = bool_to_yesno(recording)
    config["pathDefaults"]["rpiCameraVFlip"] = bool_to_yesno(vflip)
    config["pathDefaults"]["rpiCameraHFlip"] = bool_to_yesno(hflip)

    with open(MEDIAMTX_CONFIG, "w", encoding="utf-8") as f:
        yaml_loader.dump(config, f)


# ============================
# JSON response helper
# ============================

def json_response(payload, status=200):
    """Return a JSON response with optional status code."""
    return flask.jsonify(payload), status


# ============================
# Routes
# ============================

@app.route("/")
def home():
    return flask.render_template("index.html", data=get_data())


@app.route("/api/")
def api():
    return flask.render_template("api.html")


@app.route("/api/data/all")
def api_json():
    return json_response(get_data())


# Mapping sensor types to config flags and extractors
SENSOR_MAP = {
    "cpu": ("use_cpu_sensor", lambda d: d["sensors"]["cpu"]),
    "bme280": ("use_bme280_sensor", lambda d: d["sensors"]["bme280"]),
    "dht": ("use_dht_sensor", lambda d: d["sensors"]["dht"]),
    "ds18b20": ("use_ds18b20_sensor", lambda d: d["sensors"]["one_wire"]["ds18b20"]),
    "door": ("use_door_sensor", lambda d: d["sensors"]["door_sensors"]),
    "motion": ("use_motion_sensor", lambda d: d["sensors"]["motion_sensors"]),
    "weather-station": ("use_weather_station", lambda d: d["sensors"]["weather_station"]),
}


@app.route("/api/data/sensors/<sensor_type>")
def api_sensors_json(sensor_type):
    data = get_data()

    if sensor_type == "all":
        return json_response(data["sensors"])

    if sensor_type not in SENSOR_MAP:
        flask.abort(404)

    flag, extractor = SENSOR_MAP[sensor_type]
    if not data["config"]["setup"].get(flag):
        flask.abort(404)

    return json_response(extractor(data))


@app.route("/api/data/<data_type>")
def api_types_json(data_type):
    data = get_data()

    if data_type not in ("config", "system", "sensors"):
        flask.abort(404)

    return json_response(data[data_type])


# ============================
# Setup route (large form handler)
# ============================
# NOTE: This function is still large, but now structured and ready
# for extraction into service modules in Step 2.

@app.route("/setup/", methods=["GET", "POST"])
def setup():
    """Render or update the RPiMS configuration."""
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.full_load(f)
    except Exception as error:
        journal.send(str(error))
        config = {}

    if flask.request.method == "POST":
        form = flask.request.form

        # --- Setup flags ---
        setup = {
            key: bool(form.get(key))
            for key in [
                "verbose", "show_sys_info", "use_system_buttons",
                "use_door_led_indicator", "use_motion_led_indicator",
                "use_door_sensor", "use_motion_sensor",
                "use_bme280_sensor", "use_ds18b20_sensor",
                "use_dht_sensor", "use_cpu_sensor",
                "use_weather_station", "use_zabbix_sender",
                "use_picamera", "use_picamera_recording",
                "use_serial_display"
            ]
        }

        setup["serial_display_type"] = form.get("serial_display_type")
        setup["serial_type"] = form.get("serial_type")
        setup["serial_display_refresh_rate"] = int(form.get("serial_display_refresh_rate"))
        setup["serial_display_rotate"] = int(form.get("serial_display_rotate"))

        # --- Zabbix agent ---
        zabbix_agent = {
            "TLSAccept": "psk",
            "TLSConnect": "psk",
            "TLSPSK": form.get("TLSPSK"),
            "TLSPSKFile": ZABBIX_PSK,
            "TLSPSKIdentity": form.get("TLSPSKIdentity"),
            "Timeout": int(form.get("Timeout")),
            "hostname": form.get("hostname"),
            "location": form.get("location"),
            "chassis": "embedded",
            "deployment": "RPiMS",
            "zabbix_server": form.get("zabbix_server"),
            "zabbix_server_active": form.get("zabbix_server_active"),
        }

        # --- GPIO configuration ---
        gpios = ["GPIO_5", "GPIO_6", "GPIO_12", "GPIO_13", "GPIO_16",
                 "GPIO_18", "GPIO_19", "GPIO_20", "GPIO_21", "GPIO_26"]

        gpio = {}
        for item in gpios:
            gpio[item] = {
                "pin": int(form.get(f"{item}_pin")),
                "type": form.get(f"{item}_type"),
                "name": form.get(f"{item}_name"),
                "hold_time": int(form.get(f"{item}_hold_time"))
                if form.get(f"{item}_hold_time") else ""
            }

        # --- BME280 sensors ---
        BME280 = {}
        for sensor_id in ("id1", "id2", "id3"):
            prefix = f"{sensor_id}_BME280"
            entry = {
                "id": sensor_id,
                "interface": form.get(f"{prefix}_interface"),
                "name": form.get(f"{prefix}_name"),
                "read_interval": int(form.get(f"{prefix}_read_interval")),
                "use": bool(form.get(f"{prefix}_use")),
            }
            if sensor_id == "id1":
                entry["i2c_address"] = int(form.get(f"{prefix}_i2c_address"))
            else:
                entry["serial_port"] = form.get(f"{prefix}_serial_port")
            BME280[sensor_id] = entry

        # --- CPU sensor ---
        CPU = {"temp": {"read_interval": int(form.get("CPUtemp_read_interval"))}}

        # --- DHT sensor ---
        DHT = {
            "name": form.get("DHT_name"),
            "pin": int(form.get("DHT_pin")),
            "read_interval": int(form.get("DHT_read_interval")),
            "type": form.get("DHT_type"),
        }

        # --- PiCamera ---
        PICAMERA = {
            "fps": int(form.get("picamera_fps")),
            "mode": int(form.get("picamera_mode")),
            "vflip": bool(form.get("picamera_vflip")),
            "hflip": bool(form.get("picamera_hflip")),
        }

        picamera_modes = {
            1: (1920, 1080),
            6: (1280, 720),
            7: (640, 480),
        }

        mode = PICAMERA["mode"]
        width, height = picamera_modes[mode]
        recording = setup["use_picamera_recording"]

        update_mediamtx_config(
            width, height, PICAMERA["fps"], recording,
            PICAMERA["vflip"], PICAMERA["hflip"]
        )

        PICAMERA["hr"] = width
        PICAMERA["vr"] = height

        # --- Weather station ---
        RAINFALL = {
            "acquisition_time": int(form.get("rainfall_acquisition_time")),
            "agregation_time": int(form.get("rainfall_agregation_time")),
            "sensor_pin": int(form.get("rainfall_sensor_pin")),
            "use": bool(form.get("rainfall_use")),
        }

        DIRECTION = {
            "acquisition_time": int(form.get("winddirection_acquisition_time")),
            "adc_input": int(form.get("winddirection_adc_input")),
            "adc_type": form.get("winddirection_adc_type"),
            "reference_voltage_adc_input": int(form.get("reference_voltage_adc_input")),
            "use": bool(form.get("winddirection_use")),
        }

        SPEED = {
            "acquisition_time": int(form.get("windspeed_acquisition_time")),
            "agregation_time": int(form.get("windspeed_agregation_time")),
            "sensor_pin": int(form.get("windspeed_sensor_pin")),
            "use": bool(form.get("windspeed_use")),
        }

        WEATHER = {"RAINFALL": RAINFALL, "WIND": {"DIRECTION": DIRECTION, "SPEED": SPEED}}

        # --- DS18B20 ---
        DS18B20 = {
            "read_interval": int(form.get("DS18B20_read_interval")),
            "addresses": {}
        }

        if setup["use_ds18b20_sensor"]:
            for addr in form.getlist("DS18B20_address"):
                DS18B20["addresses"][addr] = {
                    "name": form.get(f"DS18B20_{addr}_name")
                }

        ONE_WIRE = {"DS18B20": DS18B20}

        # --- Final sensors structure ---
        sensors = {
            "CPU": CPU,
            "PICAMERA": PICAMERA,
            "BME280": BME280,
            "ONE_WIRE": ONE_WIRE,
            "DHT": DHT,
            "WEATHER": WEATHER,
        }

        # --- Final RPiMS structure ---
        rpims = {
            "setup": setup,
            "zabbix_agent": zabbix_agent,
            "gpio": gpio,
            "sensors": sensors,
        }

        # --- Write Zabbix config ---
        zabbix_config = [
            f"Server=127.0.0.1,{zabbix_agent['zabbix_server']}",
            f"ServerActive={zabbix_agent['zabbix_server_active']}",
            f"Hostname={zabbix_agent['hostname']}",
            f"TLSPSKIdentity={zabbix_agent['TLSPSKIdentity']}",
            f"TLSPSKFile={zabbix_agent['TLSPSKFile']}",
            f"TLSConnect={zabbix_agent['TLSConnect']}",
            f"TLSAccept={zabbix_agent['TLSAccept']}",
            f"Timeout={zabbix_agent['Timeout']}",
        ]

        with open(ZABBIX_CONF, "w", encoding="utf-8") as f:
            f.write("\n".join(zabbix_config))

        with open(ZABBIX_PSK, "w", encoding="utf-8") as f:
            f.write(zabbix_agent["TLSPSK"])

        # --- Save to Redis & YAML ---
        redis_db.set("rpims", json.dumps(rpims))
        with open(CONFIG_PATH, "w") as f:
            yaml.dump(rpims, f, default_flow_style=False, sort_keys=False, explicit_start=True)

        return flask.redirect(flask.url_for("setup"))

    # GET request
    DS18B20 = redis_db.hgetall("DS18B20")
    return flask.render_template("setup.html", config=config, _DS18B20=DS18B20)


# ============================
# Error handlers
# ============================

@app.errorhandler(404)
def not_found(error):
    return json_response({"error": "404 Not Found"}, 404)


# ============================
# Main entry point
# ============================

if __name__ == "__main__":
    app.run(host="0.0.0.0")

