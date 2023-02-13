
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



setInterval(function() {
    $.getJSON("/api/data/all", function(data) {

    if (data['config']['setup']['use_weather_station'] == true) {
		$("#average_wind_direction").html(data['sensors']['weather_station']['average_wind_direction']);
		$("#daily_average_wind_speed").html(data['sensors']['weather_station']['daily_average_wind_speed']);
		$("#average_wind_speed").html(data['sensors']['weather_station']['average_wind_speed']);
		$("#wind_speed").html(data['sensors']['weather_station']['wind_speed']);
		$("#wind_gust").html(data['sensors']['weather_station']['wind_gust']);
		$("#daily_wind_gust").html(data['sensors']['weather_station']['daily_wind_gust']);
		$("#daily_rainfall").html(data['sensors']['weather_station']['daily_rainfall']);
    }

    if (data['config']['setup']['use_cpu_sensor'] == true) {
        $("#CPU_Temperature").show();
        var CPUTEMP = data['sensors']['cpu']['temperature'];
		if (!!CPUTEMP) {
			$("#CPU_Temperature_value").html(roundPrecised(CPUTEMP,0));
			$("#CPU_Temperature_unit").html("°C");
			}
		else {
			$("#CPU_Temperature_value").html('NaN');
			$("#CPU_Temperature_unit").html('');
		}
    }
    else{
            $("#CPU_Temperature").hide();
    }

    if (data['config']['setup']['use_bme280_sensor'] == true) {
		$("#bme280_sensors").show();
		var BME280 = {};
		var BME280_T = '_BME280_Temperature';
		var BME280_H = '_BME280_Humidity';
		var BME280_P = '_BME280_Pressure';

		for (var BME280_id in data['sensors']['bme280']) {
			var BME280t = roundPrecised(data['sensors']['bme280'][BME280_id]['temperature'],1);
			var BME280h = Math.round(data['sensors']['bme280'][BME280_id]['humidity']);
			var BME280p = Math.round(data['sensors']['bme280'][BME280_id]['pressure']);
				var BME280n = data['sensors']['bme280'][BME280_id]['name'];
			//BME280[BME280_id] = BME280t;
			//BME280[BME280_id] = BME280h;
			//BME280[BME280_id] = BME280p;
			//console.log(BME280[BME280_id], BME280t,BME280h,BME280p);
			//$("#" + BME280_id + "_BME280_T_val").html(BME280t);
			//$("#" + BME280_id + "_BME280_H_val").html(BME280h);
			//$("#" + BME280_id + "_BME280_P_val").html(BME280p);
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
    }
    else{
	$("#bme280_sensors").hide();
    }

    if (data['config']['setup']['use_dht_sensor'] == true) {
		$("#DHT_Temperature").html(data['sensors']['dht']['temperature']);
		$("#DHT_Humidity").html(data['sensors']['dht']['humidity']);
    }

//	if (data['settings']['use_DS18B20_sensor'] == "True") {
//		for (var DS18B20_id in data['sensors']['DS18B20_sensors']){
//	    		var value = Math.round(data['sensors']['DS18B20_sensors'][DS18B20_id]*10)/10;
//	    		$("#" + DS18B20_id).html(value);
//		}
//	}

    if (data['config']['setup']['use_door_sensor'] == true) {
	    $("#door_sensors").show();
	    for (var key in data['sensors']['door_sensors']){
		var value = data['sensors']['door_sensors'][key];
		$("#" + key).html(value);
	    if (value == "open"){
		$('#' + key).removeClass("value");
		$('#' + key).addClass("alarm");
	    }
	    if (value == "close"){
		$('#' + key).removeClass("alarm");
		$('#' + key).addClass("value");
	    }
	    }
    }
    if (data['config']['setup']['use_door_sensor'] == false) {
		$("#door_sensors").hide(); 
    }

	
    if (data['config']['setup']['use_motion_sensor'] == true) {
	$("#motion_sensors").show();
	for (var key in data['sensors']['motion_sensors']){
	    var value = data['sensors']['motion_sensors'][key];
	    $("#" + key).html(value);
	    if (value == "motion"){
		$('#' + key).removeClass("value");
		$('#' + key).addClass("alarm");
	    }
	    if (value == "nomotion"){
		$('#' + key).removeClass("alarm");
		$('#' + key).addClass("value");
	    }
	}
    }

    if (data['config']['setup']['use_motion_sensor'] == false) {
	$("#motion_sensors").hide(); 
    }

    if (data['config']['setup']['show_sys_info'] == true) {
	$("#sys_info").show(); 
    }
    else {
	$("#sys_info").hide(); 
    }

    $("#hostip").html(data['system']['hostip']);
    $("#hostname").html(data['system']['hostname']);
    $("#location").html(data['system']['location']);

if (data['config']['setup']['use_weather_station'] == true) {
    var WindSpeed = Math.round(data['sensors']['weather_station']['wind_speed']);
    var WindGust = Math.round(data['sensors']['weather_station']['wind_gust']);
    var WindGust24h = Math.round(data['sensors']['weather_station']['daily_wind_gust']);
}

if (data['config']['setup']['use_dht_sensor'] == true) {
	$("#dht_sensor").show();
    var DHTTemperature = roundPrecised(data['sensors']['dht']['temperature'],1);
    var DHTHumidity = Math.round(data['sensors']['dht']['humidity']);
}
if (data['config']['setup']['use_dht_sensor'] == false) {
	$("#dht_sensor").hide();
}

if (data['config']['setup']['use_ds18b20_sensor'] == true & typeof(data['sensors']['one_wire']) !== 'undefined' ) {
	$("#ds18b20_sensors").show();
    var DS18B20 = {};
    for (var DS18B20_id in data['sensors']['one_wire']['ds18b20']) {
		//console.log(DS18B20_id)
		DS18B20[DS18B20_id] = roundPrecised(data['sensors']['one_wire']['ds18b20'][DS18B20_id]['temperature'],1);
		//console.log(DS18B20[DS18B20_id])
    }
}

const g4 = document.querySelector("#g4");
const g5 = document.querySelector("#g5");
const g6 = document.querySelector("#g6");

const g11 = document.querySelector("#g11");
const g12 = document.querySelector("#g12");

if (data['config']['setup']['use_weather_station'] == true) {
    setGaugeValue(g4, WindSpeed/100, 100, "km/h");
    setGaugeValue(g5, WindGust/100, 100, "km/h");
    setGaugeValue(g6, WindGust24h/100, 100, "km/h");
}

if (data['config']['setup']['use_dht_sensor'] == true) {
    setGaugeValue(g11, DHTTemperature/100, 100, "°C");
    setGaugeValue(g12, DHTHumidity/100, 100, "%");
}

if (data['config']['setup']['use_ds18b20_sensor'] == true  & typeof(data['sensors']['one_wire']) !== 'undefined') {
    var DS18B20_prefix = 'DS18B20_';
    for (var DS18B20_id in data['sensors']['one_wire']['ds18b20']) {
		var sensor_name = DS18B20_prefix + DS18B20_id;
		var sensor_value = DS18B20[DS18B20_id];
		//console.log(eval(sensor_name));
		if (!!sensor_value) {
			setGaugeValue(eval(sensor_name), sensor_value/100, 100, "°C");
		}
		else {
			setGaugeValue(eval(sensor_name), "NULL", "", "");
		}
    }
}

});
}, 500);
