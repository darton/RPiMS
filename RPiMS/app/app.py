# -*- coding:utf-8 -*-
#
#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

"""Flask App"""

# Standard library
import os
import json
import logging

# Third-party libraries
import flask
import redis
from ruamel.yaml import YAML


logging.basicConfig(
    level=logging.INFO,
    format="RPiMS: %(levelname)s: %(message)s"
)

# =========================
# Configuration & Constants
# =========================

BASE_DIR = os.environ.get("RPIMS_DIR", os.getcwd())

CONFIG_PATH = "../config/rpims.yaml"
ZABBIX_CONF = "../config/zabbix_rpims.conf"
ZABBIX_PSK = "../config/zabbix_rpims.psk"
MEDIAMTX_CONFIG = "/etc/mediamtx/mediamtx.yml"

# Flask app initialization
app = flask.Flask(__name__)
app.config.update(
    SECRET_KEY="b8f475757df5dc1cabfed8aee1ca84a6",
    DEBUG=True,
    JSON_AS_ASCII=False,
    JSONIFY_MIMETYPE="application/json; charset=utf-8",
)

logger = app.logger

app.config["REDIS_DB"] = redis.StrictRedis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


# ==============================================
# YAML helpers (ruamel.yaml, preserves comments)
# ==============================================

yaml_loader = YAML()
yaml_loader.preserve_quotes = True
yaml_loader.indent(mapping=2, sequence=4, offset=2)
yaml_loader.width = 4096  # avoid line wrapping

def load_yaml_preserve(path):
    """Load YAML preserving comments and ordering. Returns ruamel CommentedMap or None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml_loader.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error("Failed to load YAML %s: %s", path, e)
        return None

def save_yaml_preserve(path, data, explicit_start=False):
    """Save data (CommentedMap or dict) to YAML preserving comments where possible."""
    # Optionally set explicit_start for this dump only
    prev = getattr(yaml_loader, "explicit_start", False)
    yaml_loader.explicit_start = explicit_start
    try:
        with open(path, "w", encoding="utf-8") as f:
            yaml_loader.dump(data, f)
    except Exception as e:
        logger.error("Failed to save YAML %s: %s", path, e)
        raise
    finally:
        yaml_loader.explicit_start = prev

def to_plain_dict(obj):
    """
    Convert ruamel CommentedMap/CommentedSeq to plain Python dict/list recursively.
    Useful before json.dumps or other operations that expect plain types.
    """
    if obj is None:
        return None
    # Primitive types
    if isinstance(obj, (str, int, float, bool)):
        return obj
    # Mapping-like
    try:
        if hasattr(obj, "items"):
            return {k: to_plain_dict(v) for k, v in obj.items()}
        # Sequence-like
        if hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes)):
            return [to_plain_dict(v) for v in obj]
    except Exception:
        pass
    return obj


# =================
# Utility functions
# =================

def bool_to_yesno(value: bool) -> str:
    """Convert boolean to 'yes'/'no' string."""
    return "yes" if value else "no"


def json_response(payload, status=200):
    """Return a JSON response with optional status code."""
    return flask.jsonify(payload), status


def error_response(message, status=400):
    """Return a standardized JSON error response."""
    return flask.jsonify({
        "status": "error",
        "error": message
    }), status


# ========================
# Global exception handler
# ========================

@app.errorhandler(Exception)
def handle_exception(e):
    """Catch-all for unexpected exceptions."""
    logger.error("Unhandled exception: %s", str(e))

    # If it's an HTTPException, return its own response
    if isinstance(e, flask.exceptions.HTTPException):
        return error_response(e.description, e.code)

    # Otherwise return generic 500
    return error_response("Unexpected server error", 500)


# ======================
# Sensor loading helpers
# ======================

def load_cpu_sensor(redis_db, config):
    if not config.get("setup", {}).get("use_cpu_sensor"):
        return None
    return {"temperature": redis_db.get("CPU_Temperature")}


def load_dht_sensor(redis_db, config):
    if not config.get("setup", {}).get("use_dht_sensor"):
        return None
    # fixed key: DHT (was DDHT)
    return redis_db.hgetall("DHT")


def load_door_sensor(redis_db, config):
    if not config.get("setup", {}).get("use_door_sensor"):
        return None
    return redis_db.hgetall("DOOR_SENSORS")


def load_motion_sensor(redis_db, config):
    if not config.get("setup", {}).get("use_motion_sensor"):
        return None
    return redis_db.hgetall("MOTION_SENSORS")


def load_bme280_sensor(redis_db, config):
    if not config.get("setup", {}).get("use_bme280_sensor"):
        return None

    result = {}
    for sensor_id in ("id1", "id2", "id3"):
        key = f"{sensor_id}_BME280"
        data = redis_db.hgetall(key)
        if data:
            result[sensor_id] = data
    return result


def load_ds18b20_sensor(redis_db, config):
    if not config.get("setup", {}).get("use_ds18b20_sensor"):
        return None

    raw = redis_db.hgetall("DS18B20")
    return {k: {"temperature": v} for k, v in raw.items()}


def load_weather_station(redis_db, config):
    if not config.get("setup", {}).get("use_weather_station"):
        return None
    return redis_db.hgetall("WEATHER")


def get_sensors(redis_db, config):
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


# ================
# Data aggregation
# ================

def get_data(redis_db):
    rpims_raw = redis_db.get("rpims")
    rpims = json.loads(rpims_raw) if rpims_raw else {"zabbix_agent": {}}

    system_info = redis_db.hgetall("SYSTEM")
    system_info["hostname"] = rpims.get("zabbix_agent", {}).get("hostname", "")
    system_info["location"] = rpims.get("zabbix_agent", {}).get("location", "")

    return {
        "config": rpims,
        "system": system_info,
        "sensors": get_sensors(redis_db, rpims),
    }


# =============================
# MediaMTX configuration update
# =============================

def update_mediamtx_config(width, height, fps, recording, vflip, hflip):
    config = load_yaml_preserve(MEDIAMTX_CONFIG)
    if config is None:
        config = {}

    # Ensure pathDefaults exists
    if "pathDefaults" not in config or config["pathDefaults"] is None:
        config["pathDefaults"] = {}

    config["pathDefaults"]["rpiCameraWidth"] = width
    config["pathDefaults"]["rpiCameraHeight"] = height
    config["pathDefaults"]["rpiCameraFPS"] = fps
    config["pathDefaults"]["record"] = bool_to_yesno(recording)
    config["pathDefaults"]["rpiCameraVFlip"] = bool_to_yesno(vflip)
    config["pathDefaults"]["rpiCameraHFlip"] = bool_to_yesno(hflip)

    save_yaml_preserve(MEDIAMTX_CONFIG, config)


# ===========================
# Small form helper functions
# ===========================

def load_gpio_from_form(form, gpios):
    gpio = {}
    for item in gpios:
        hold = form.get(f"{item}_hold_time")
        gpio[item] = {
            "pin": int(form.get(f"{item}_pin")) if form.get(f"{item}_pin") else "",
            "type": form.get(f"{item}_type"),
            "name": form.get(f"{item}_name"),
            "hold_time": int(hold) if hold else ""
        }
    return gpio


def load_bme280_from_form(form):
    sensors = {}
    for sensor_id in ("id1", "id2", "id3"):
        prefix = f"{sensor_id}_BME280"
        read_interval = form.get(f"{prefix}_read_interval")
        entry = {
            "id": sensor_id,
            "interface": form.get(f"{prefix}_interface"),
            "name": form.get(f"{prefix}_name"),
            "read_interval": int(read_interval) if read_interval else 0,
            "use": bool(form.get(f"{prefix}_use")),
        }
        if sensor_id == "id1":
            addr = form.get(f"{prefix}_i2c_address")
            entry["i2c_address"] = int(addr) if addr else None
        else:
            entry["serial_port"] = form.get(f"{prefix}_serial_port")
        sensors[sensor_id] = entry
    return sensors


def load_ds18b20_from_form(form, enabled):
    ds = {
        "read_interval": int(form.get("DS18B20_read_interval")) if form.get("DS18B20_read_interval") else 0,
        "addresses": {}
    }
    if enabled:
        for addr in form.getlist("DS18B20_address"):
            ds["addresses"][addr] = {
                "name": form.get(f"DS18B20_{addr}_name")
            }
    return ds


def load_weather_from_form(form):
    rainfall = {
        "acquisition_time": int(form.get("rainfall_acquisition_time")) if form.get("rainfall_acquisition_time") else 0,
        "agregation_time": int(form.get("rainfall_agregation_time")) if form.get("rainfall_agregation_time") else 0,
        "sensor_pin": int(form.get("rainfall_sensor_pin")) if form.get("rainfall_sensor_pin") else 0,
        "use": bool(form.get("rainfall_use")),
    }

    direction = {
        "acquisition_time": int(form.get("winddirection_acquisition_time")) if form.get("winddirection_acquisition_time") else 0,
        "adc_input": int(form.get("winddirection_adc_input")) if form.get("winddirection_adc_input") else 0,
        "adc_type": form.get("winddirection_adc_type"),
        "reference_voltage_adc_input": int(form.get("reference_voltage_adc_input")) if form.get("reference_voltage_adc_input") else 0,
        "use": bool(form.get("winddirection_use")),
    }

    speed = {
        "acquisition_time": int(form.get("windspeed_acquisition_time")) if form.get("windspeed_acquisition_time") else 0,
        "agregation_time": int(form.get("windspeed_agregation_time")) if form.get("windspeed_agregation_time") else 0,
        "sensor_pin": int(form.get("windspeed_sensor_pin")) if form.get("windspeed_sensor_pin") else 0,
        "use": bool(form.get("windspeed_use")),
    }

    return {"RAINFALL": rainfall, "WIND": {"DIRECTION": direction, "SPEED": speed}}


def load_picamera_from_form(form, setup):
    picamera = {
        "fps": int(form.get("picamera_fps")) if form.get("picamera_fps") else 0,
        "mode": int(form.get("picamera_mode")) if form.get("picamera_mode") else 1,
        "vflip": bool(form.get("picamera_vflip")),
        "hflip": bool(form.get("picamera_hflip")),
    }

    picamera_modes = {
        1: (1920, 1080),
        6: (1280, 720),
        7: (640, 480),
    }

    mode = picamera["mode"]
    width, height = picamera_modes.get(mode, (1920, 1080))
    recording = setup.get("use_picamera_recording", False)

    update_mediamtx_config(
        width, height, picamera["fps"], recording,
        picamera["vflip"], picamera["hflip"]
    )

    picamera["hr"] = width
    picamera["vr"] = height
    return picamera


def write_zabbix_config(agent):
    lines = [
        f"Server=127.0.0.1,{agent.get('zabbix_server','')}",
        f"ServerActive={agent.get('zabbix_server_active','')}",
        f"Hostname={agent.get('hostname','')}",
        f"TLSPSKIdentity={agent.get('TLSPSKIdentity','')}",
        f"TLSPSKFile={agent.get('TLSPSKFile','')}",
        f"TLSConnect={agent.get('TLSConnect','')}",
        f"TLSAccept={agent.get('TLSAccept','')}",
        f"Timeout={agent.get('Timeout','')}",
    ]
    try:
        with open(ZABBIX_CONF, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except Exception as e:
        logger.error("Failed to write Zabbix config: %s", e)
        raise


# ======
# Routes
# ======

@app.route("/")
def home():
    redis_db = flask.current_app.config["REDIS_DB"]
    return flask.render_template("index.html", data=get_data(redis_db))


@app.route("/api/")
def api():
    return flask.render_template("api.html")


@app.route("/api/data/all")
def api_json():
    redis_db = flask.current_app.config["REDIS_DB"]
    return json_response(get_data(redis_db))


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
    redis_db = flask.current_app.config["REDIS_DB"]
    data = get_data(redis_db)

    if sensor_type == "all":
        return json_response(data["sensors"])

    if sensor_type not in SENSOR_MAP:
        return error_response("Unknown sensor type", 404)

    flag, extractor = SENSOR_MAP[sensor_type]
    if not data["config"].get("setup", {}).get(flag):
        return error_response("Sensor disabled", 404)

    return json_response(extractor(data))


@app.route("/api/data/<data_type>")
def api_types_json(data_type):
    redis_db = flask.current_app.config["REDIS_DB"]
    data = get_data(redis_db)

    if data_type not in ("config", "system", "sensors"):
        return error_response("Unknown data type", 404)

    return json_response(data[data_type])


# ===========
# Setup route
# ===========

@app.route("/setup/", methods=["GET", "POST"])
def setup():
    redis_db = flask.current_app.config["REDIS_DB"]
    try:
        config_cm = load_yaml_preserve(CONFIG_PATH)
        config = to_plain_dict(config_cm) if config_cm is not None else {}
    except Exception as error:
        logger.error(str(error))
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
        setup["serial_display_refresh_rate"] = int(form.get("serial_display_refresh_rate")) if form.get("serial_display_refresh_rate") else 0
        setup["serial_display_rotate"] = int(form.get("serial_display_rotate")) if form.get("serial_display_rotate") else 0

        # --- Zabbix agent ---
        zabbix_agent = {
            "TLSAccept": "psk",
            "TLSConnect": "psk",
            "TLSPSK": form.get("TLSPSK"),
            "TLSPSKFile": ZABBIX_PSK,
            "TLSPSKIdentity": form.get("TLSPSKIdentity"),
            "Timeout": int(form.get("Timeout")) if form.get("Timeout") else 0,
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

        gpio = load_gpio_from_form(form, gpios)

        # --- BME280 sensors ---
        BME280 = load_bme280_from_form(form)

        # --- CPU sensor ---
        CPU = {"temp": {"read_interval": int(form.get("CPUtemp_read_interval")) if form.get("CPUtemp_read_interval") else 0}}

        # --- DHT sensor ---
        DHT = {
            "name": form.get("DHT_name"),
            "pin": int(form.get("DHT_pin")) if form.get("DHT_pin") else 0,
            "read_interval": int(form.get("DHT_read_interval")) if form.get("DHT_read_interval") else 0,
            "type": form.get("DHT_type"),
        }

        # --- PiCamera ---
        PICAMERA = load_picamera_from_form(form, setup)

        # --- Weather station ---
        WEATHER = load_weather_from_form(form)

        # --- DS18B20 ---
        DS18B20 = load_ds18b20_from_form(form, setup.get("use_ds18b20_sensor", False))

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
        write_zabbix_config(zabbix_agent)
        try:
            with open(ZABBIX_PSK, "w", encoding="utf-8") as f:
                f.write(zabbix_agent.get("TLSPSK", "") or "")
        except Exception as e:
            logger.error("Failed to write Zabbix PSK: %s", e)

        # --- Save to Redis & YAML ---
        try:
            redis_db.set("rpims", json.dumps(rpims))
        except Exception as e:
            logger.error("Failed to save rpims to Redis: %s", e)

        try:
            # Save YAML without losing comments in other files; rpims is plain dict
            save_yaml_preserve(CONFIG_PATH, rpims, explicit_start=True)
        except Exception as e:
            logger.error("Failed to save rpims YAML: %s", e)

        return flask.redirect(flask.url_for("setup"))

    # GET request
    DS18B20 = redis_db.hgetall("DS18B20")
    return flask.render_template("setup.html", config=config, _DS18B20=DS18B20)


# ==============
# Error handlers
# ==============

@app.errorhandler(404)
def handle_404(error):
    logger.error("404 Not Found: %s - %s", flask.request.path, error)
    return error_response("Resource not found", 404)


@app.errorhandler(400)
def handle_400(error):
    logger.error("400 Bad Request: %s - %s", flask.request.path, error)
    return error_response("Bad request", 400)


@app.errorhandler(500)
def handle_500(error):
    logger.error("500 Internal Server Error: %s", error)
    return error_response("Internal server error", 500)


# ================
# Main entry point
# ================

if __name__ == "__main__":
    app.run(host="0.0.0.0")
