
setInterval(function() {
    $.getJSON("rpims.php", function(data) {
	$("#average_wind_direction").html(data['average_wind_direction']);
	$("#daily_average_wind_speed").html(data['daily_average_wind_speed']);
	$("#average_wind_speed").html(data['average_wind_speed']);
	$("#wind_speed").html(data['wind_speed']);
	$("#wind_gust").html(data['wind_gust']);
	$("#daily_wind_gust").html(data['daily_wind_gust']);

	$("#daily_rainfall").html(data['daily_rainfall']);

	$("#CPU_Temperature").html(data['CPU_Temperature']);

	$("#hostip").html(data['hostip']);
	$("#hostname").html(data['hostname']);
	$("#location").html(data['location']);

	$("#BME280_Temperature").html(data['BME280_Temperature']);
	$("#BME280_Humidity").html(data['BME280_Humidity']);
	$("#BME280_Pressure").html(data['BME280_Pressure']);

	$("#DHT_Temperature").html(data['DHT_Temperature']);
	$("#DHT_Humidity").html(data['DHT_Humidity']);

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
