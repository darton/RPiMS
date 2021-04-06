function roundPrecised(number, precision) {
    var power = Math.pow(10, precision);

    return Math.round(number * power) / power;
}

setInterval(function() {
    $.getJSON("rpims.php", function(data) {

    if (data['settings']['use_weather_station'] == true) {
	$("#average_wind_direction").html(data['weather_station']['average_wind_direction']);
	$("#daily_average_wind_speed").html(data['weather_station']['daily_average_wind_speed']);
	$("#average_wind_speed").html(data['weather_station']['average_wind_speed']);
	$("#wind_speed").html(data['weather_station']['wind_speed']);
	$("#wind_gust").html(data['weather_station']['wind_gust']);
	$("#daily_wind_gust").html(data['weather_station']['daily_wind_gust']);
	$("#daily_rainfall").html(data['weather_station']['daily_rainfall']);
    }

    if (data['settings']['use_cpu_sensor'] == true) {
        var CPUTEMP = data['sensors']['cpu']['temperature'];
	if (!!CPUTEMP){
	    $("#CPU_Temperature").html(roundPrecised(CPUTEMP,1));
	    $("#CPU_Temperature_unit").html("°C");
        }
	else {
	    $("#CPU_Temperature").html('NaN');
	    $("#CPU_Temperature_unit").html('');
	}
    }
    else {
	$("#CPU_Temperature_name").hide();
    }

    if (data['settings']['use_bme280_sensor'] == true) {
	$("#BME280_Temperature").html(data['sensors']['bme280']['temperature']);
	$("#BME280_Humidity").html(data['sensors']['bme280']['humidity']);
	$("#BME280_Pressure").html(data['sensors']['bme280']['pressure']);
    }

    if (data['settings']['use_dht_sensor'] == true) {
	$("#DHT_Temperature").html(data['sensors']['dht']['temperature']);
	$("#DHT_Humidity").html(data['sensors']['dht']['humidity']);
    }

//	if (data['settings']['use_DS18B20_sensor'] == "True") {
//		for (var DS18B20_id in data['sensors']['DS18B20_sensors']){
//	    		var value = Math.round(data['sensors']['DS18B20_sensors'][DS18B20_id]*10)/10;
//	    		$("#" + DS18B20_id).html(value);
//		}
//	}

    if (data['settings']['use_door_sensor'] == true) {
	for (var key in data['sensors']['door_sensors']){
    	    var value = data['sensors']['door_sensors'][key];
    	    $("#" + key).html(value);
	}
    }
    if (data['settings']['use_motion_sensor'] == true) {
	for (var key in data['sensors']['motion_sensors']){
    	    var value = data['sensors']['motion_sensors'][key];
    	    $("#" + key).html(value);
	}
    }

    $("#hostip").html(data['system']['hostip']);
    $("#hostname").html(data['system']['hostname']);
    $("#location").html(data['system']['location']);


if (data['settings']['use_bme280_sensor'] == true) {
    var BME280 = {};
    for (var item in data['sensors']['bme280'])
	{
	var BME280Temperature = roundPrecised(data['sensors']['bme280'][item]['temperature'],1);
	var BME280Humidity = Math.round(data['sensors']['bme280'][item]['humidity']);
	var BME280Pressure = Math.round(data['sensors']['bme280'][item]['pressure']);
	var bme280 = {};
	bme280['temperature'] = BME280Temperature;;
	bme280['humidity'] = BME280Humidity;
	bme280['pressure'] = BME280Pressure;
	BME280[item] = bme280;
	}

 //console.log(BME280[2]);
 //console.log(BME280.1.temperature, BME280.1.humidity, BME280.1.pressure);
 // console.log( bme280_1.temperature);
}

if (data['settings']['use_weather_station'] == true) {
    var WindSpeed = Math.round(data['weather_station']['wind_speed']);
    var WindGust = Math.round(data['weather_station']['wind_gust']);
    var WindGust24h = Math.round(data['weather_station']['daily_wind_gust']);
}

if (data['settings']['use_dht_sensor'] == true) {
    var DHTTemperature = roundPrecised(data['sensors']['dht']['temperature'],1);
    var DHTHumidity = Math.round(data['sensors']['dht']['humidity']);
}

if (data['settings']['use_ds18b20_sensor'] == true)
{
    var DS18B20 = {};
    for (var DS18B20_id in data['sensors']['one_wire']['ds18b20'])
    {
    //console.log(DS18B20_id)
    DS18B20[DS18B20_id] = roundPrecised(data['sensors']['one_wire']['ds18b20'][DS18B20_id],1);
    }
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

const g1 = document.querySelector("#g1");
const g2 = document.querySelector("#g2");
const g3 = document.querySelector("#g3");
const g4 = document.querySelector("#g4");
const g5 = document.querySelector("#g5");
const g6 = document.querySelector("#g6");

const g11 = document.querySelector("#g11");
const g12 = document.querySelector("#g12");

if (data['settings']['use_bme280_sensor'] == true) {
    if (!!BME280Temperature) {
    setGaugeValue(g1, BME280Temperature/100, 100, "°C");
    setGaugeValue(g2, BME280Humidity/100, 100, "%");
    setGaugeValue(g3, BME280Pressure/1100, 1100, "hPa");
}
else {
    setGaugeValue(g1, "NULL", "", "");
    setGaugeValue(g2, "NULL", "", "");
    setGaugeValue(g3, "NULL", "", "");
}
}

if (data['settings']['use_weather_station'] == true) {
    setGaugeValue(g4, WindSpeed/100, 100, "km/h");
    setGaugeValue(g5, WindGust/100, 100, "km/h");
    setGaugeValue(g6, WindGust24h/100, 100, "km/h");
}

if (data['settings']['use_dht_sensor'] == true) {
    setGaugeValue(g11, DHTTemperature/100, 100, "°C");
    setGaugeValue(g12, DHTHumidity/100, 100, "%");
}

if (data['settings']['use_ds18b20_sensor'] == true) {
    var DS18B20_prefix = 'DS18B20_';
    for (var DS18B20_id in data['sensors']['one_wire']['ds18b20']){
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

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
