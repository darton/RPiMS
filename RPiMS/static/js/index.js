const DOOR_STATE = {
    0: "close",
    1: "open"
};

const MOTION_STATE = {
    0: "nomotion",
    1: "motion"
};

let lastUsePicamera = null;

function qs(sel) {
    return document.querySelector(sel);
}

function qsa(sel) {
    return document.querySelectorAll(sel);
}

function show(el) {
    if (typeof el === "string") el = qs(el);
    if (el) el.style.display = "";
}

function hide(el) {
    if (typeof el === "string") el = qs(el);
    if (el) el.style.display = "none";
}

function html(el, value) {
    if (typeof el === "string") el = qs(el);
    if (el) el.innerHTML = value;
}

function updateCamera(data) {
    const usePicamera = data.config.setup.use_picamera;

    if (usePicamera === lastUsePicamera) return;
    lastUsePicamera = usePicamera;

    const iframe = qs("#rpicamera iframe");

    if (usePicamera) {
        iframe.src = "http://" + window.location.hostname + ":8889/cam";
        show("#rpicamera");
    } else {
        iframe.src = "";
        hide("#rpicamera");
    }
}

function updateWheatherStation(data) {
    const useWS = data.config.setup.use_weather_station;
    const windSpeed = data.config.sensors.WEATHER.WIND.SPEED.use;
    const windDir = data.config.sensors.WEATHER.WIND.DIRECTION.use;
    const rainfall = data.config.sensors.WEATHER.RAINFALL.use;

    if (useWS && (windSpeed || windDir || rainfall)) {
        show("#weather_station");

        if (windSpeed) {
            show("#div_wind_speed");
            html("#wind_speed", data.sensors.weather_station.wind_speed);
            html("#average_wind_speed", data.sensors.weather_station.average_wind_speed);
            html("#wind_gust", data.sensors.weather_station.wind_gust);
            html("#daily_wind_gust", data.sensors.weather_station.daily_wind_gust);
            html("#daily_average_wind_speed", data.sensors.weather_station.daily_average_wind_speed);

            const gws = qs("#gws");
            const gwg = qs("#gwg");
            const gwg24h = qs("#gwg24h");

            setGaugeValue(gws, Math.round(data.sensors.weather_station.wind_speed) / 100, 100, "km/h");
            setGaugeValue(gwg, Math.round(data.sensors.weather_station.wind_gust) / 100, 100, "km/h");
            setGaugeValue(gwg24h, Math.round(data.sensors.weather_station.daily_wind_gust) / 100, 100, "km/h");
        } else hide("#div_wind_speed");

        if (windDir) {
            show("#wind_direction");
            html("#average_wind_direction", data.sensors.weather_station.average_wind_direction);
        } else hide("#wind_direction");

        if (rainfall) {
            show("#raifall");
            html("#daily_rainfall", data.sensors.weather_station.daily_rainfall);
        } else hide("#rainfall");

    } else {
        hide("#weather_station");
    }
}

function updateds18b20v2(data) {
    if (data.config.setup.use_ds18b20_sensor && data.sensors.one_wire) {
        const container = qs("#ds18b20_container");
        container.innerHTML = "";

        const addresses = data.config.sensors.ONE_WIRE.DS18B20.addresses;
        const values = data.sensors.one_wire.ds18b20;

        const keys = Object.keys(addresses);
        if (keys.length === 0) {
            container.insertAdjacentHTML("beforeend",
                "<div class='sensors ds18b20_sensors'><div class='w3-container w3-margin w3-text-grey'>No DS18B20 sensors detected !</div></div>"
            );
            return;
        }

        keys.forEach(addr => {
            const name = addresses[addr]?.name || addr;
            const temp = values?.[addr] ?? "--";

            const htmlBlock = `
                <div class='sensors ds18b20_sensors'>
                    <div class='w3-container w3-margin'>
                        <b>${name}</b> (${addr})
                        <div style='width: 100%; display: table;'>
                            <div style='display: table-row'>
                                <div class='gauge_ds18b20' id='DS18B20_${addr}'>
                                    <div class='gauge__body'>
                                        <div class='gauge__fill'></div>
                                        <div class='gauge__cover'></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class='ds18b20_value'>${temp} °C</div>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML("beforeend", htmlBlock);
        });
    }
}

function updateDS18b20(data) {
    if (data.config.setup.use_ds18b20_sensor && data.sensors.one_wire) {
        qsa(".ds18b20_sensors").forEach(el => show(el));

        const values = {};
        for (let id in data.sensors.one_wire.ds18b20) {
            values[id] = roundPrecised(data.sensors.one_wire.ds18b20[id].temperature, 1);
        }

        for (let id in values) {
            const el = qs("#DS18B20_" + id);
            const val = values[id];

            if (val) {
                show(el);
                setGaugeValue(el, val / 100, 100, "°C");
            } else {
                hide(el);
                setGaugeValue(el, "NULL", "", "");
            }
        }
    } else {
        qsa(".ds18b20_sensors").forEach(el => hide(el));
    }
}

function updateContactSensors(data) {
    if (data.config.setup.use_contact_sensor) {
        show("#contact_sensors");

        for (let key in data.sensors.contact_sensors) {
            const value = Number(data.sensors.contact_sensors[key]);
            const el = qs("#" + key);

            html(el, value === 1 ? "open - 1" : "close - 0");

            el.classList.toggle("alarm", value === 1);
            el.classList.toggle("value", value === 0);
        }
    } else hide("#contact_sensors");
}

function updateDigitalSensors(data) {
    if (data.config.setup.use_digital_sensor) {
        show("#digital_sensors");

        for (let key in data.sensors.digital_sensors) {
            const value = Number(data.sensors.digital_sensors[key]);
            const el = qs("#" + key);

            html(el, value === 1 ? "motion - 1" : "nomotion - 0");

            el.classList.toggle("alarm", value === 1);
            el.classList.toggle("value", value === 0);
        }
    } else hide("#digital_sensors");
}

function updateDHTSensor(data) {
    if (data.config.setup.use_dht_sensor) {
        show("#dht_sensor");

        const t = roundPrecised(data.sensors.dht.temperature, 1);
        const h = Math.round(data.sensors.dht.humidity);

        setGaugeValue(qs("#gdhttemp"), t / 100, 100, "°C");
        setGaugeValue(qs("#gdhthum"), h / 100, 100, "%");
    } else hide("#dht_sensor");
}

function updateBME280Sensor(data) {
    const use = data.config.setup.use_bme280_sensor;
    const use1 = data.config.sensors.BME280.id1.use;
    const use2 = data.config.sensors.BME280.id2.use;
    const use3 = data.config.sensors.BME280.id3.use;

    function read(id) {
        const sensor = data.sensors.bme280?.[id];
        if (!sensor) return;

        const t = roundPrecised(sensor.temperature, 1);
        const h = Math.round(sensor.humidity);
        const p = Math.round(sensor.pressure);

        html("#" + id + "_BME280_name", sensor.name);

        setGaugeValue(qs(`#${id}_BME280_Temperature`), t / 100, 100, "°C");
        setGaugeValue(qs(`#${id}_BME280_Humidity`), h / 100, 100, "%");
        setGaugeValue(qs(`#${id}_BME280_Pressure`), p / 1100, 1100, "hPa");
    }

    if (use && (use1 || use2 || use3)) {
        show("#bme280_sensors");

        if (use1) { read("id1"); show("#id1_BME280"); } else hide("#id1_BME280");
        if (use2) { read("id2"); show("#id2_BME280"); } else hide("#id2_BME280");
        if (use3) { read("id3"); show("#id3_BME280"); } else hide("#id3_BME280");

    } else hide("#bme280_sensors");
}

function updateSystemInfo(data) {
    if (data.config.setup.show_sys_info) {
        show("#sys_info");
        html("#hostip", data.system.hostip);
        html("#hostname", data.system.hostname);
        html("#location", data.system.location);
    } else hide("#sys_info");

    if (data.config.setup.use_cpu_sensor) {
        show("#CPU_Temperature");

        const temp = data.sensors.cpu.temperature;
        if (temp) {
            html("#CPU_Temperature_value", roundPrecised(temp, 0));
            html("#CPU_Temperature_unit", "°C");
        } else {
            html("#CPU_Temperature_value", "NaN");
            html("#CPU_Temperature_unit", "");
        }
    } else hide("#CPU_Temperature");
}

function roundPrecised(number, precision) {
    const power = Math.pow(10, precision);
    return Math.round(number * power) / power;
}

function setGaugeValue(gauge, value, divisor, unit) {
    if (!gauge) return;
    if (value < 0 || value > 1) return;

    const value1 = value / 2;
    const value2 = roundPrecised(value * divisor, 2);

    gauge.querySelector(".gauge__fill").style.transform = `rotate(${value1}turn)`;
    gauge.querySelector(".gauge__cover").textContent = `${value2} ${unit}`;
}

async function getJsonData() {
    try {
        const res = await fetch("/api/data/all");
        const data = await res.json();

        updateSystemInfo(data);
        updateContactSensors(data);
        updateDigitalSensors(data);
        updateCamera(data);
        updateBME280Sensor(data);
        updateDHTSensor(data);
        updateWheatherStation(data);
        updateds18b20v2(data);

    } catch (e) {
        console.error("API error:", e);
    }
}

setInterval(getJsonData, 1000);
