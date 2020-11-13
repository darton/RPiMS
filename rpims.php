<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}
$rpims_api["settings"]["verbose"] = $rpims["verbose"];
$rpims_api["settings"]["useZabbixSender"] = $rpims["use_zabbix_sender"];
$rpims_api["settings"]["usePiCamera"] = $rpims["use_picamera"];
$rpims_api["settings"]["usePiCameraRecording"] = $rpims["use_picamera_recording"];
$rpims_api["settings"]["useCpuSensor"] = $rpims["use_CPU_sensor"];
$rpims_api["settings"]["useBME280Sensor"] = $rpims["use_BME280_sensor"];
$rpims_api["settings"]["useDHTSensor"] = $rpims["use_DHT_sensor"];
$rpims_api["settings"]["useDS18B20Sensor"] = $rpims["use_DS18B20_sensor"];
$rpims_api["settings"]["useWeatherStation"] = $rpims["use_weather_station"];
$rpims_api["settings"]["useDoorSensor"] = $rpims["use_door_sensor"];
$rpims_api["settings"]["useMotionSensor"] = $rpims["use_motion_sensor"];
$rpims_api["settings"]["hostip"] = $rpims["hostip"];
$rpims_api["settings"]["hostname"] = $rpims["hostname"];
$rpims_api["settings"]["location"] = $rpims["location"];


if ($rpims["use_CPU_sensor"] == "True"){
    $rpims_api["sensors"]["CPU"]["readInterval"] = $rpims["CPUtemp_read_interval"];
    $rpims_api["sensors"]["CPU"]["temperature"] = $rpims["CPU_Temperature"];
}

if ($rpims["use_BME280_sensor"] == "True"){
    $rpims_api["sensors"]["BME280"]["i2cAddress"] = $rpims["BME280_i2c_address"];
    $rpims_api["sensors"]["BME280"]["readInterval"] = $rpims["BME280_read_interval"];
    $rpims_api["sensors"]["BME280"]["temperature"] = round($rpims["BME280_Temperature"],2);
    $rpims_api["sensors"]["BME280"]["humidity"] = round($rpims["BME280_Humidity"],2);
    $rpims_api["sensors"]["BME280"]["pressure"] = round($rpims["BME280_Pressure"],1);
}

if ($rpims["use_DHT_sensor"] == "True"){
    $rpims_api["sensors"]["DHT"]["readInterval"] = $rpims["DHT_read_interval"];
    $rpims_api["sensors"]["DHT"]["gpioPin"] = $rpims["DHT_pin"];
    $rpims_api["sensors"]["DHT"]["dhtType"] = $rpims["DHT_type"];
    $rpims_api["sensors"]["DHT"]["temperature"] = $rpims["DHT_Temperature"];
    $rpims_api["sensors"]["DHT"]["humidity"] = $rpims["DHT_Humidity"];
}

if ($rpims["use_weather_station"] == "True"){
    $rpims_api["weather_station"]["windSpeed"] = $rpims["wind_speed"];
    $rpims_api["weather_station"]["windSpeedAcquisitionTime"] = $rpims["windspeed_acquisition_time"];
    $rpims_api["weather_station"]["windSpeedAgregationTime"] = $rpims["windspeed_agregation_time"];
    $rpims_api["weather_station"]["averageWindSpeed"] = $rpims["average_wind_speed"];
    $rpims_api["weather_station"]["dailyAveragewindSpeed"] = $rpims["daily_average_wind_speed"];
    $rpims_api["weather_station"]["windGust"] = $rpims["wind_gust"];
    $rpims_api["weather_station"]["dailyWindGust"] = $rpims["daily_wind_gust"];
    $rpims_api["weather_station"]["averageWindDirection"] = $rpims["average_wind_direction"];
    $rpims_api["weather_station"]["dailyRainfall"] = $rpims["daily_rainfall"];
    $rpims_api["weather_station"]["rainfallAcquisitionTime"] = $rpims["rainfall_acquisition_time"];
    $rpims_api["weather_station"]["rainfallAgregationTime"] = $rpims["rainfall_agregation_time"];
}

$obj = $redis-> get('gpio');
$gpio = json_decode($obj, true);

if ($rpims["use_door_sensor"] == "True"){
    foreach ($gpio as $key=> $value) {
	if ($gpio[$key]["type"] == "DoorSensor" ){
	    $door_sensors[$key] = ($gpio[$key]);
	}
    }
    foreach ($door_sensors as $key => $value){
	$rpims_api["sensors"]["door_sensors"]["$key"] = $rpims[$key];
    }
}

if ($rpims["use_motion_sensor"] == "True"){
    foreach ($gpio as $key=> $value) {
	if ($gpio[$key]["type"] == "MotionSensor" ){
	    $motion_sensors[$key] = ($gpio[$key]);
	}
    }
    foreach ($motion_sensors as $key => $value){
	$rpims_api["sensors"]["motion_sensors"]["$key"] = $rpims[$key];
    }
}

if ($rpims["use_DS18B20_sensor"] == "True"){
    $rpims_api["sensors"]["DS18B20_sensors"]["readInterval"] = $rpims["DS18B20_read_interval"];
    $DS18B20_sensors = $redis->smembers('DS18B20_sensors');
    foreach ($DS18B20_sensors as $key => $value){
	$rpims_api["sensors"]["DS18B20_sensors"]["array"]["$value"] = round($rpims[$value],2);
	}
    }

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
