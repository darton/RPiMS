const DOOR_STATE = {
    0: "close",
    1: "open"
};

const MOTION_STATE = {
    0: "nomotion",
    1: "motion"
};

//$("#" + key).html(`${value} - ${DOOR_STATE[value]}`);


let lastUsePicamera = null;
function updateCamera(data) {
    const usePicamera = data.config.setup.use_picamera;

    // if the condition has not changed - do nothing
    if (usePicamera === lastUsePicamera) {
        return;
    }

    lastUsePicamera = usePicamera;

    if (usePicamera) {
        $("#rpicamera iframe").attr("src", "http://" + window.location.hostname + ":8889/cam");
        $("#rpicamera").show();
    } else {
        $("#rpicamera iframe").attr("src", "");
        $("#rpicamera").hide();
    }
}


function updateWheatherStation(data) {
    const useWheatherStation = data.config.setup.use_weather_station
    const useWheatherWindSpeed = data.config.sensors.WEATHER.WIND.SPEED.use
    const useWheatherWindDirection = data.config.sensors.WEATHER.WIND.DIRECTION.use
    const useWheatherRainfall = data.config.sensors.WEATHER.RAINFALL.use

    if (useWheatherStation && (useWheatherWindSpeed || useWheatherWindDirection || useWheatherRainfall)) {
	$("#weather_station").show();
		if (useWheatherWindSpeed) {
			$("#div_wind_speed").show();
			$("#wind_speed").html(data.sensors.weather_station.wind_speed);
			$("#average_wind_speed").html(data.sensors.weather_station.average_wind_speed);
			$("#wind_gust").html(data.sensors.weather_station.wind_gust);
			$("#daily_wind_gust").html(data.sensors.weather_station.daily_wind_gust);
			$("#daily_average_wind_speed").html(data.sensors.weather_station.daily_average_wind_speed);
			//const gws = document.querySelector("#gws");
			//const gwg = document.querySelector("#gwg");
			//const gwg24h = document.querySelector("#gwg24h");
			const gws = $("#gws")[0];
			const gwg = $("#gwg")[0];
			const gwg24h = $("#gwg24h")[0];
			var WindSpeed = Math.round(data.sensors.weather_station.wind_speed);
			var WindGust = Math.round(data.sensors.weather_station.wind_gust);
			var WindGust24h = Math.round(data.sensors.weather_station.daily_wind_gust);
			setGaugeValue(gws, WindSpeed/100, 100, "km/h");
			setGaugeValue(gwg, WindGust/100, 100, "km/h");
			setGaugeValue(gwg24h, WindGust24h/100, 100, "km/h");
		} else { $("#div_wind_speed").hide();}
		if (useWheatherWindDirection) {
			$("#wind_direction").show();
			$("#average_wind_direction").html(data.sensors.weather_station.average_wind_direction);
		} else { $("#wind_direction").hide();}
		if (useWheatherRainfall) {
			$("#raifall").show();
			$("#daily_rainfall").html(data.sensors.weather_station.daily_rainfall);
		} else { $("#rainfall").hide();}
    }
    else {
	$("#weather_station").hide();
    }
}


function updateds18b20v2(data) {
    if (data.config.setup.use_ds18b20_sensor & typeof(data.sensors.one_wire) !== 'undefined' ) {
            const addresses = data.config.sensors.ONE_WIRE.DS18B20.addresses;
            const values = data.sensors.one_wire.ds18b20;
            $("#ds18b20_container").empty();
            const keys = Object.keys(addresses);
            if (keys.length === 0) {
                $("#ds18b20_container").append(
                    "<div class='sensors ds18b20_sensors'><div class='w3-container w3-margin w3-text-grey'>No DS18B20 sensors detected !</div></div>"
                );
                return;
            }
            keys.forEach(addr => {
                const name = addresses[addr]?.name || addr;
                const temp = values?.[addr] ?? "--";

                const html = `
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

                $("#ds18b20_container").append(html);
            });
    }
}


function updateDS18b20(data) {

//	if (data['settings']['use_DS18B20_sensor'] == "True") {
//		for (var DS18B20_id in data['sensors']['DS18B20_sensors']){
//	    		var value = Math.round(data['sensors']['DS18B20_sensors'][DS18B20_id]*10)/10;
//	    		$("#" + DS18B20_id).html(value);
//		}
//	}


    if (data.config.setup.use_ds18b20_sensor & typeof(data.sensors.one_wire) !== 'undefined' ) {
		$(".ds18b20_sensors").show();
		var DS18B20 = {};
		for (var DS18B20_id in data['sensors']['one_wire']['ds18b20']) {
			//console.log(DS18B20_id)
			DS18B20[DS18B20_id] = roundPrecised(data['sensors']['one_wire']['ds18b20'][DS18B20_id]['temperature'],1);
			//console.log(DS18B20[DS18B20_id])
		}
		var DS18B20_prefix = 'DS18B20_';
		for (var DS18B20_id in data['sensors']['one_wire']['ds18b20']) {
			var sensor_name = DS18B20_prefix + DS18B20_id;
			var sensor_value = DS18B20[DS18B20_id];
			//console.log(sensor_name);
			if (!!sensor_value) {
				$("#" + sensor_name).show();
				setGaugeValue(eval(sensor_name), sensor_value/100, 100, "°C");
			}
			else {
				$("#" + sensor_name).hide();
				setGaugeValue(eval(sensor_name), "NULL", "", "");
			}
		}
    }
    else {
		$(".ds18b20_sensors").hide();
    }
}


function updateContactSensors(data) {
    if (data.config.setup.use_contact_sensor) {
        $("#contact_sensors").show();
        for (var key in data['sensors']['contact_sensors']){
	    var value = Number(data['sensors']['contact_sensors'][key]);
            var text = value === 1 ? "open - 1" : "close - 0";
	    $("#" + key).html(text);
	    if (value === 1){
		$('#' + key).removeClass("value");
		$('#' + key).addClass("alarm");
	    }
	    if (value === 0){
		$('#' + key).removeClass("alarm");
		$('#' + key).addClass("value");
	    }
	}
    }
    else {
	$("#contact_sensors").hide(); 
    }
}


function updateDigitalSensors(data) {
    if (data.config.setup.use_digital_sensor) {
	$("#digital_sensors").show();
	for (var key in data['sensors']['digital_sensors']){
	    var value = Number(data['sensors']['digital_sensors'][key]);
            var text = value === 1 ? "motion - 1" : "nomotion - 0";
	    $("#" + key).html(text);
	    if (value === 1){
		$('#' + key).removeClass("value");
		$('#' + key).addClass("alarm");
	    }
	    if (value === 0){
		$('#' + key).removeClass("alarm");
		$('#' + key).addClass("value");
	    }
	}
    }
    else {
	$("#digital_sensors").hide(); 
    }
}

function updateDHTSensor(data){
//    if (data['config']['setup']['use_dht_sensor'] == true) {
//	$("#DHT_Temperature").html(data['sensors']['dht']['temperature']);
//	$("#DHT_Humidity").html(data['sensors']['dht']['humidity']);
//    }

    if (data.config.setup.use_dht_sensor) {
	$("#dht_sensor").show();
	var DHTTemperature = roundPrecised(data.sensors.dht.temperature,1);
	var DHTHumidity = Math.round(data.sensors.dht.humidity);
	//const gDHTt = document.querySelector("#gdhttemp");
	//const gDHTh = document.querySelector("#gdhthum");
	const gDHTt = $("#gdhttemp")[0];
	const gDHTh = $("#gdhthum")[0];
	setGaugeValue(gDHTt, DHTTemperature/100, 100, "°C");
	setGaugeValue(gDHTh, DHTHumidity/100, 100, "%");
    }
    else {
	$("#dht_sensor").hide();
    }
}


function updateBME280Sensor(data){
    const useBME280 = data.config.setup.use_bme280_sensor;
    const useId1BME280 = data.config.sensors.BME280.id1.use;
    const useId2BME280 = data.config.sensors.BME280.id2.use;
    const useId3BME280 = data.config.sensors.BME280.id3.use;


    function readBME280data(data, BME280_id){

	var BME280 = {};
	var BME280_T = '_BME280_Temperature';
	var BME280_H = '_BME280_Humidity';
	var BME280_P = '_BME280_Pressure';

	if (!data.sensors || !data.sensors.bme280) {
    	    console.log("No data from BME280");
    	    return;
	}

	// No specific sensor
	const sensor = data.sensors.bme280[BME280_id];
	if (!sensor) {
    	    console.log("No data from the sensor:", BME280_id);
    	    return;
	}

	// not temp / hum / press
	if (sensor.temperature == null ||
    	    sensor.humidity == null ||
    	    sensor.pressure == null) {
    	    console.log("Sensor data incomcomplete:", BME280_id);
    	    return;
	}

	    var BME280t = roundPrecised(data.sensors.bme280[BME280_id].temperature,1);
	    var BME280h = Math.round(data.sensors.bme280[BME280_id].humidity);
	    var BME280p = Math.round(data.sensors.bme280[BME280_id].pressure);
	    var BME280n = data.sensors.bme280[BME280_id].name;

	    var BME280_name = BME280_id + '_BME280_name';
	    $("#" + BME280_name).html(BME280n);

	    var t_sensor_name = BME280_id + BME280_T;
	    var t_sensor_value = BME280t;
	    var h_sensor_name = BME280_id + BME280_H;
	    var h_sensor_value = BME280h;
	    var p_sensor_name = BME280_id + BME280_P;
	    var p_sensor_value = BME280p;

	    //console.log(eval(sensor_name));
	    if (!!t_sensor_value || h_sensor_value || p_sensor_value  ) {
		setGaugeValue(eval(t_sensor_name), t_sensor_value/100, 100, "°C");
		setGaugeValue(eval(h_sensor_name), h_sensor_value/100, 100, "%");
		setGaugeValue(eval(p_sensor_name), p_sensor_value/1100, 1100, "hPa");
	    }
	    else {
		setGaugeValue(eval(t_sensor_name), "NULL", "", "");
		setGaugeValue(eval(h_sensor_name), "NULL", "", "");
		setGaugeValue(eval(p_sensor_name), "NULL", "", "");
	    }
    }

    if (useBME280 && (useId1BME280 || useId2BME280 || useId3BME280)) {
	$("#bme280_sensors").show();

	for (var BME280_id in data.config.sensors.BME280) {

	    if ((BME280_id == 'id1') && useId1BME280){
		readBME280data(data, BME280_id)
		$("#id1_BME280").show();
	    } else { $("#id1_BME280").hide(); }

	    if ((BME280_id == 'id2') && useId2BME280){
		readBME280data(data, BME280_id)
		$("#id2_BME280").show();
	    } else { $("#id2_BME280").hide(); }

	    if ((BME280_id == 'id3') && useId3BME280){
		readBME280data(data, BME280_id)
		$("#id3_BME280").show();
	    } else { $("#id3_BME280").hide(); }
	}
    }
    else {
	$("#bme280_sensors").hide();
    }
}


function updateSystemInfo(data){
    if (data.config.setup.show_sys_info) {
	$("#sys_info").show(); 
	$("#hostip").html(data['system']['hostip']);
	$("#hostname").html(data['system']['hostname']);
	$("#location").html(data['system']['location']);
    }
    else {
	$("#sys_info").hide(); 
    }

    if (data.config.setup.use_cpu_sensor) {
        $("#CPU_Temperature").show();
        var CPUTEMP = data.sensors.cpu.temperature;
	if (!!CPUTEMP) {
		$("#CPU_Temperature_value").html(roundPrecised(CPUTEMP,0));
		$("#CPU_Temperature_unit").html("°C");
	}
	else {
		$("#CPU_Temperature_value").html('NaN');
		$("#CPU_Temperature_unit").html('');
	}
    }
    else {
            $("#CPU_Temperature").hide();
    }
}

function roundPrecised(number, precision) {
    var power = Math.pow(10, precision);
    return Math.round(number * power) / power;
}


function setGaugeValue(gauge, value, divisor, unit ) {
	if (value < 0 || value > 1) {
	    return;
	}
	var value1 = value/2;
	var value2 = roundPrecised((value*divisor), 2);
  
	gauge.querySelector(".gauge__fill").style.transform = `rotate(${value1}turn)`;
	gauge.querySelector(".gauge__cover").textContent = `${ value2 } ${unit}`;
  }


function getJsonData() {
  $.getJSON("/api/data/all", function(data) {
    updateSystemInfo(data)
    updateContactSensors(data)
    updateDigitalSensors(data)
    updateCamera(data);
    updateBME280Sensor(data)
    updateDHTSensor(data)
    updateWheatherStation(data)
    updateds18b20v2(data)
  });
}

setInterval(getJsonData, 1000);
