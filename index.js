document.addEventListener("DOMContentLoaded", () => {

function roundPrecised(number, precision) {
    var power = Math.pow(10, precision);

    return Math.round(number * power) / power;
}

setInterval(function() {
    $.getJSON("rpims.php", function(data) {

	if (data['settings']['useWeatherStation'] == "True") {
		$("#average_wind_direction").html(data['weather_station']['averageWindDirection']);
		$("#daily_average_wind_speed").html(data['weather_station']['dailyAverageWindSpeed']);
		$("#average_wind_speed").html(data['weather_station']['averageWindSpeed']);
		$("#wind_speed").html(data['weather_station']['windSpeed']);
		$("#wind_gust").html(data['weather_station']['windGust']);
		$("#daily_wind_gust").html(data['weather_station']['dailyWindGust']);
		$("#daily_rainfall").html(data['weather_station']['dailyRainfall']);
	}

	if (data['settings']['useCpuSensor'] == "True") {
		$("#CPU_Temperature").html(roundPrecised(data['sensors']['CPU']['temperature'],1));
	}

	if (data['settings']['useBME280Sensor'] == "True") {
		$("#BME280_Temperature").html(data['sensors']['BME280']['temperature']);
		$("#BME280_Humidity").html(data['sensors']['BME280']['humidity']);
		$("#BME280_Pressure").html(data['sensors']['BME280']['pressure']);
	}

	if (data['settings']['useDHTSensor'] == "True") {
		$("#DHT_Temperature").html(data['sensors']['DHT']['temperature']);
		$("#DHT_Humidity").html(data['sensors']['DHT']['humidity']);
	}

//	if (data['settings']['use_DS18B20_sensor'] == "True") {
//		for (var DS18B20_id in data['sensors']['DS18B20_sensors']){
//	    		var value = Math.round(data['sensors']['DS18B20_sensors'][DS18B20_id]*10)/10;
//	    		$("#" + DS18B20_id).html(value);
//		}
//	}

	if (data['settings']['useDoorSensor'] == "True") {
		for (var key in data['sensors']['door_sensors']){
	    		var value = data['sensors']['door_sensors'][key];
	    		$("#" + key).html(value);
		}
	}
	if (data['settings']['useMotionSensor'] == "True") {
		for (var key in data['sensors']['motion_sensors']){
	    		var value = data['sensors']['motion_sensors'][key];
	    		$("#" + key).html(value);
		}
	}

	$("#hostip").html(data['settings']['hostip']);
	$("#hostname").html(data['settings']['hostname']);
	$("#location").html(data['settings']['location']);


if (data['settings']['useBME280Sensor'] == "True") {
    var BME280Temperature = roundPrecised(data['sensors']['BME280']['temperature'],1);
    var BME280Humidity = Math.round(data['sensors']['BME280']['humidity']);
    var BME280Pressure = Math.round(data['sensors']['BME280']['pressure']);
}

if (data['settings']['useWeatherStation'] == "True") {
    var WindSpeed = Math.round(data['weather_station']['windSpeed']);
    var WindGust = Math.round(data['weather_station']['windGust']);
    var WindGust24h = Math.round(data['weather_station']['dailyWindGust']);
}

if (data['settings']['useDHTSensor'] == "True") {
    var DHTTemperature = roundPrecised(data['sensors']['DHT']['temperature'],1);
    var DHTHumidity = Math.round(data['sensors']['DHT']['humidity']);
}

if (data['settings']['useDS18B20Sensor'] == "True") {
    var DS18B20 = {};
    for (var DS18B20_id in data['sensors']['DS18B20_sensors']['array']){
    console.log(DS18B20_id)
    DS18B20[DS18B20_id] = roundPrecised(data['sensors']['DS18B20_sensors']['array'][DS18B20_id],1);
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

if (data['settings']['useBME280Sensor'] == "True") {
    setGaugeValue(g1, BME280Temperature/100, 100, "°C");
    setGaugeValue(g2, BME280Humidity/100, 100, "%");
    setGaugeValue(g3, BME280Pressure/1100, 1100, "hPa");
}

if (data['settings']['useWeatherStation'] == "True") {
    setGaugeValue(g4, WindSpeed/100, 100, "km/h");
    setGaugeValue(g5, WindGust/100, 100, "km/h");
    setGaugeValue(g6, WindGust24h/100, 100, "km/h");
}

if (data['settings']['useDHTSensor'] == "True") {
    setGaugeValue(g11, DHTTemperature/100, 100, "°C");
    setGaugeValue(g12, DHTHumidity/100, 100, "%");
}

if (data['settings']['useDS18B20Sensor'] == "True") {
    var DS18B20_prefix = 'DS18B20_';
    for (var DS18B20_id in data['sensors']['DS18B20_sensors']['array']){
    var sensor_name = DS18B20_prefix + DS18B20_id;
    var sensor_value = DS18B20[DS18B20_id];
    console.log(eval(sensor_name));
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

});
