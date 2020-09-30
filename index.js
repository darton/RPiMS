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

	if (data['system']['use_DS18B20_sensor'] == "True") {
		for (var key in data['DS18B20_sensors']){
	    		var value = data['DS18B20_sensors'][key];
	    		$("#" + key).html(value);
		}
	}

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

});
}, 500);
