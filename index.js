
setInterval(function() {
    $.getJSON("rpims.php", function(data) {

	$("#hostip").html(data['system']['hostip']);
	$("#hostname").html(data['system']['hostname']);
	$("#location").html(data['system']['location']);

	$("#average_wind_direction").html(data['weather_station']['average_wind_direction']);
	$("#daily_average_wind_speed").html(data['weather_station']['daily_average_wind_speed']);
	$("#average_wind_speed").html(data['weather_station']['average_wind_speed']);
	$("#wind_speed").html(data['weather_station']['wind_speed']);
	$("#wind_gust").html(data['weather_station']['wind_gust']);
	$("#daily_wind_gust").html(data['weather_station']['daily_wind_gust']);
	$("#daily_rainfall").html(data['weather_station']['daily_rainfall']);

	$("#CPU_Temperature").html(data['sensors']['CPU']['Temperature']);

	$("#BME280_Temperature").html(data['sensors']['BME280']['Temperature']);
	$("#BME280_Humidity").html(data['sensors']['BME280']['Humidity']);
	$("#BME280_Pressure").html(data['sensors']['BME280']['Pressure']);

	$("#DHT_Temperature").html(data['sensors']['DHT']['Temperature']);
	$("#DHT_Humidity").html(data['sensors']['DHT']['Humidity']);


	for (var key in data['DS18B20_sensors']){
	    var value = data['DS18B20_sensors'][key];
	    $("#" + key).html(value);
	}

	for (var key in data['door_sensors']){
	    var value = data['door_sensors'][key];
	    $("#" + key).html(value);
	}

	for (var key in data['motion_sensors']){
	    var value = data['motion_sensors'][key];
	    $("#" + key).html(value);
	}



});
}, 500);
