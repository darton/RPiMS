
setInterval(function() {
    $.getJSON("rpims.php", function(data) {
	if (data['system']['use_weather_station'] == "True") {
		$("#average_wind_direction").html(data['weather_station']['average_wind_direction']);
		$("#daily_average_wind_speed").html(data['weather_station']['daily_average_wind_speed']);
		$("#average_wind_speed").html(data['weather_station']['average_wind_speed']);
		$("#wind_speed").html(data['weather_station']['wind_speed']);
		$("#wind_gust").html(data['weather_station']['wind_gust']);
		$("#daily_wind_gust").html(data['weather_station']['daily_wind_gust']);
		$("#daily_rainfall").html(data['weather_station']['daily_rainfall']);
	}

	if (data['system']['use_CPU_sensor'] == "True") {
		$("#CPU_Temperature").html(data['sensors']['CPU']['Temperature']);
	}
	if (data['system']['use_BME280_sensor'] == "True") {
		$("#BME280_Temperature").html(data['sensors']['BME280']['Temperature']);
		$("#BME280_Humidity").html(data['sensors']['BME280']['Humidity']);
		$("#BME280_Pressure").html(data['sensors']['BME280']['Pressure']);
	}

	if (data['system']['use_DHT_sensor'] == "True") {
		$("#DHT_Temperature").html(data['sensors']['DHT']['Temperature']);
		$("#DHT_Humidity").html(data['sensors']['DHT']['Humidity']);
	}

//	if (data['system']['use_DS18B20_sensor'] == "True") {
//		for (var DS18B20_id in data['sensors']['DS18B20_sensors']){
//	    		var value = Math.round(data['sensors']['DS18B20_sensors'][DS18B20_id]*10)/10;
//	    		$("#" + DS18B20_id).html(value);
//		}
//	}

	if (data['system']['use_door_sensor'] == "True") {
		for (var key in data['door_sensors']){
	    		var value = data['door_sensors'][key];
	    		$("#" + key).html(value);
		}
	}
	if (data['system']['use_motion_sensor'] == "True") {
		for (var key in data['motion_sensors']){
	    		var value = data['motion_sensors'][key];
	    		$("#" + key).html(value);
		}
	}

	$("#hostip").html(data['system']['hostip']);
	$("#hostname").html(data['system']['hostname']);
	$("#location").html(data['system']['location']);

function roundPrecised(number, precision) {
    var power = Math.pow(10, precision);

    return Math.round(number * power) / power;
}

if (data['system']['use_BME280_sensor'] == "True") {
    var BME280Temperature = Math.round(data['sensors']['BME280']['Temperature'] * 10)/10;
    var BME280Humidity = Math.round(data['sensors']['BME280']['Humidity']);
    var BME280Pressure = data['sensors']['BME280']['Pressure'];
}

if (data['system']['use_weather_station'] == "True") {
    var WindSpeed = Math.round(data['weather_station']['wind_speed']);
    var WindGust = Math.round(data['weather_station']['wind_gust']);
    var WindGust24h = Math.round(data['weather_station']['daily_wind_gust']);
}

if (data['system']['use_DHT_sensor'] == "True") {
    var DHTTemperature = Math.round(data['sensors']['DHT']['Temperature'] * 10)/10;
    var DHTHumidity = Math.round(data['sensors']['DHT']['Humidity']);
}

if (data['system']['use_DS18B20_sensor'] == "True") {
    var DS18B20 = {};
    for (var DS18B20_id in data['sensors']['DS18B20_sensors']){
    DS18B20[DS18B20_id] = data['sensors']['DS18B20_sensors'][DS18B20_id];
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

if (data['system']['use_BME280_sensor'] == "True") {
    setGaugeValue(g1, BME280Temperature/100, 100, "°C");
    setGaugeValue(g2, BME280Humidity/100, 100, "%");
    setGaugeValue(g3, BME280Pressure/1100, 1100, "hPa");
}

if (data['system']['use_weather_station'] == "True") {
    setGaugeValue(g4, WindSpeed/100, 100, "km/h");
    setGaugeValue(g5, WindGust/100, 100, "km/h");
    setGaugeValue(g6, WindGust24h/100, 100, "km/h");
}

if (data['system']['use_DHT_sensor'] == "True") {
    setGaugeValue(g11, DHTTemperature/100, 100, "°C");
    setGaugeValue(g12, DHTHumidity/100, 100, "%");
}

if (data['system']['use_DS18B20_sensor'] == "True") {
    var DS18B20_prefix = 'DS18B20_';
    for (var DS18B20_id in data['sensors']['DS18B20_sensors']){
    var sensor_name = DS18B20_prefix + DS18B20_id;
    var sensor_value = DS18B20[DS18B20_id];
    //console.log(eval(sensor_name));
    setGaugeValue(eval(sensor_name), sensor_value/100, 100, "°C");
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
