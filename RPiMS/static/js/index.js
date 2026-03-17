// --- Helpers -------------------------------------------------------------

const qs = sel => document.querySelector(sel);
const qsa = sel => document.querySelectorAll(sel);

const getEl = el => (typeof el === "string" ? qs(el) : el) || null;

const show = el => {
    el = getEl(el);
    if (el) el.style.display = "";
};

const hide = el => {
    el = getEl(el);
    if (el) el.style.display = "none";
};

const html = (el, v) => {
    el = getEl(el);
    if (el) el.innerHTML = v;
};

const toggle = (el, cond) => cond ? show(el) : hide(el);

const roundPrecised = (n, p) => Math.round(n * 10 ** p) / 10 ** p;

function setGaugeValue(gauge, value, divisor, unit) {
    gauge = getEl(gauge);
    if (!gauge || value < 0 || value > 1) return;
    const angle = value / 2;
    const display = roundPrecised(value * divisor, 2);
    const fill = gauge.querySelector(".gauge__fill");
    const cover = gauge.querySelector(".gauge__cover");
    if (fill) fill.style.transform = `rotate(${angle}turn)`;
    if (cover) cover.textContent = `${display} ${unit}`;
}

// --- Camera --------------------------------------------------------------

let lastUsePicamera = null;

function updateCamera(data) {
    const use = data.config.setup.use_picamera;
    if (use === lastUsePicamera) return;
    lastUsePicamera = use;

    const iframe = qs("#rpicamera iframe");
    iframe.src = use ? `http://${location.hostname}:8889/cam` : "";
    toggle("#rpicamera", use);
}

// --- Weather Station -----------------------------------------------------

function updateWheatherStation(data) {
    const cfg = data.config.sensors.WEATHER;
    const ws = data.sensors.weather_station;

    const use = data.config.setup.use_weather_station &&
                (cfg.WIND.SPEED.use || cfg.WIND.DIRECTION.use || cfg.RAINFALL.use);

    toggle("#weather_station", use);
    if (!use) return;

    // Wind speed
    toggle("#div_wind_speed", cfg.WIND.SPEED.use);
    if (cfg.WIND.SPEED.use) {
        html("#wind_speed", ws.wind_speed);
        html("#average_wind_speed", ws.average_wind_speed);
        html("#wind_gust", ws.wind_gust);
        html("#daily_wind_gust", ws.daily_wind_gust);
        html("#daily_average_wind_speed", ws.daily_average_wind_speed);

        setGaugeValue(qs("#gws"), Math.round(ws.wind_speed) / 100, 100, "km/h");
        setGaugeValue(qs("#gwg"), Math.round(ws.wind_gust) / 100, 100, "km/h");
        setGaugeValue(qs("#gwg24h"), Math.round(ws.daily_wind_gust) / 100, 100, "km/h");
    }

    // Wind direction
    toggle("#wind_direction", cfg.WIND.DIRECTION.use);
    if (cfg.WIND.DIRECTION.use) {
        html("#average_wind_direction", ws.average_wind_direction);
    }

    // Rainfall
    toggle("#rainfall", cfg.RAINFALL.use);
    if (cfg.RAINFALL.use) {
        html("#daily_rainfall", ws.daily_rainfall);
    }
}

// --- DS18B20 v2 ----------------------------------------------------------

function updateds18b20v2(data) {
    if (!data.config.setup.use_ds18b20_sensor || !data.sensors.one_wire) return;

    const container = qs("#ds18b20_container");
    container.innerHTML = "";

    const addresses = data.config.sensors.ONE_WIRE.DS18B20.addresses;
    const values = data.sensors.one_wire.ds18b20;

    const keys = Object.keys(addresses);
    if (!keys.length) {
        container.insertAdjacentHTML("beforeend",
            `<div class='sensors ds18b20_sensors'>
                <div class='w3-container w3-margin w3-text-grey'>
                    No DS18B20 sensors detected !
                </div>
            </div>`
        );
        return;
    }

    keys.forEach(addr => {
        const name = addresses[addr]?.name || addr;
        const temp = values?.[addr] ?? "--";

        container.insertAdjacentHTML("beforeend", `
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
        `);
    });
}

// --- DS18B20 gauges ------------------------------------------------------

function updateDS18b20(data) {
    const use = data.config.setup.use_ds18b20_sensor && data.sensors.one_wire;
    qsa(".ds18b20_sensors").forEach(el => toggle(el, use));
    if (!use) return;

    const sensors = data.sensors.one_wire.ds18b20;

    Object.entries(sensors).forEach(([id, obj]) => {
        const gauge = qs(`#DS18B20_${id}`);
        const temp = roundPrecised(obj.temperature, 1);

        if (temp) {
            show(gauge);
            setGaugeValue(gauge, temp / 100, 100, "°C");
        } else {
            hide(gauge);
            setGaugeValue(gauge, 0, 1, "");
        }
    });
}

// --- Contact sensors -----------------------------------------------------

function updateContactSensors(data) {
    const use = data.config.setup.use_contact_sensor;
    toggle("#contact_sensors", use);
    if (!use) return;

    Object.entries(data.sensors.contact_sensors).forEach(([id, val]) => {
        const el = qs("#" + id);
        const num = Number(val);
        html(el, num ? "open - 1" : "close - 0");
        el.classList.toggle("alarm", num === 1);
        el.classList.toggle("value", num === 0);
    });
}

// --- Digital sensors -----------------------------------------------------

function updateDigitalSensors(data) {
    const use = data.config.setup.use_digital_sensor;
    toggle("#digital_sensors", use);
    if (!use) return;

    Object.entries(data.sensors.digital_sensors).forEach(([id, val]) => {
        const el = qs("#" + id);
        const num = Number(val);
        html(el, num ? "motion - 1" : "nomotion - 0");
        el.classList.toggle("alarm", num === 1);
        el.classList.toggle("value", num === 0);
    });
}

// --- DHT -----------------------------------------------------------------

function updateDHTSensor(data) {
    const use = data.config.setup.use_dht_sensor;
    toggle("#dht_sensor", use);
    if (!use) return;

    const t = roundPrecised(data.sensors.dht.temperature, 1);
    const h = Math.round(data.sensors.dht.humidity);

    setGaugeValue(qs("#gdhttemp"), t / 100, 100, "°C");
    setGaugeValue(qs("#gdhthum"), h / 100, 100, "%");
}

// --- BME280 --------------------------------------------------------------

function updateBME280Sensor(data) {
    const cfg = data.config.sensors.BME280;
    const use = data.config.setup.use_bme280_sensor &&
                (cfg.id1.use || cfg.id2.use || cfg.id3.use);

    toggle("#bme280_sensors", use);
    if (!use) return;

    const read = id => {
        const s = data.sensors.bme280?.[id];
        if (!s) return;

        html(`#${id}_BME280_name`, s.name);

        setGaugeValue(qs(`#${id}_BME280_Temperature`), roundPrecised(s.temperature, 1) / 100, 100, "°C");
        setGaugeValue(qs(`#${id}_BME280_Humidity`), Math.round(s.humidity) / 100, 100, "%");
        setGaugeValue(qs(`#${id}_BME280_Pressure`), Math.round(s.pressure) / 1100, 1100, "hPa");
    };

    ["id1", "id2", "id3"].forEach(id => {
        toggle(`#${id}_BME280`, cfg[id].use);
        if (cfg[id].use) read(id);
    });
}

// --- System info ---------------------------------------------------------

function updateSystemInfo(data) {
    const sys = data.system || {};

    const showSys = data.config.setup.show_sys_info;
    toggle("#sys_info", showSys);
    if (showSys) {
        html("#hostip", sys.hostip ?? "");
        html("#hostname", sys.hostname ?? "");
        html("#location", sys.location ?? "");
    }

    const cpu = data.config.setup.use_cpu_sensor;
    toggle("#CPU_Temperature", cpu);

    if (cpu) {
        const t = data.sensors.cpu?.temperature;
        html("#CPU_Temperature_value", t != null ? roundPrecised(t, 0) : "NaN");
        html("#CPU_Temperature_unit", t != null ? "°C" : "");
    }
}

// --- Fetch loop ----------------------------------------------------------

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
        updateDS18b20(data);

    } catch (e) {
        console.error("API error:", e);
    }
}

setInterval(getJsonData, 1000);
