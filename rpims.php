<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

$obj = $redis-> get('config');
$config = json_decode($obj, true);

$obj = $redis-> get('zabbix_agent');
$zabbix_agent = json_decode($obj, true);

$rpims_api["settings"]["verbose"] = $config["verbose"];
$rpims_api["settings"]["useZabbixSender"] = $config["use_zabbix_sender"];
$rpims_api["settings"]["usePiCamera"] = $config["use_picamera"];
$rpims_api["settings"]["usePiCameraRecording"] = $config["use_picamera_recording"];
$rpims_api["settings"]["useCpuSensor"] = $config["use_CPU_sensor"];
$rpims_api["settings"]["useBME280Sensor"] = $config["use_BME280_sensor"];
$rpims_api["settings"]["useDHTSensor"] = $config["use_DHT_sensor"];
$rpims_api["settings"]["useDS18B20Sensor"] = $config["use_DS18B20_sensor"];
$rpims_api["settings"]["useWeatherStation"] = $config["use_weather_station"];
$rpims_api["settings"]["useDoorSensor"] = $config["use_door_sensor"];
$rpims_api["settings"]["useMotionSensor"] = $config["use_motion_sensor"];

$rpims_api["system"]["hostip"] = $rpims["hostip"];
$rpims_api["system"]["hostname"] = $zabbix_agent["hostname"];
$rpims_api["system"]["location"] = $zabbix_agent["location"];


if ($config["use_CPU_sensor"] == true){
    $rpims_api["sensors"]["CPU"]["readInterval"] = $config["CPUtemp_read_interval"];
    $rpims_api["sensors"]["CPU"]["temperature"] = $rpims["CPU_Temperature"];
}

if ($config["use_BME280_sensor"] == true){
    $rpims_api["sensors"]["BME280"]["i2cAddress"] = $config["BME280_i2c_address"];
    $rpims_api["sensors"]["BME280"]["readInterval"] = $config["BME280_read_interval"];
    $rpims_api["sensors"]["BME280"]["temperature"] = round($rpims["BME280_Temperature"],2);
    $rpims_api["sensors"]["BME280"]["humidity"] = round($rpims["BME280_Humidity"],2);
    $rpims_api["sensors"]["BME280"]["pressure"] = round($rpims["BME280_Pressure"],1);
}

if ($config["use_DHT_sensor"] == true){
    $rpims_api["sensors"]["DHT"]["readInterval"] = $config["DHT_read_interval"];
    $rpims_api["sensors"]["DHT"]["gpioPin"] = $config["DHT_pin"];
    $rpims_api["sensors"]["DHT"]["dhtType"] = $config["DHT_type"];
    $rpims_api["sensors"]["DHT"]["temperature"] = $rpims["DHT_Temperature"];
    $rpims_api["sensors"]["DHT"]["humidity"] = $rpims["DHT_Humidity"];
}

if ($config["use_weather_station"] == true){
    $rpims_api["weather_station"]["windSpeedAcquisitionTime"] = $config["windspeed_acquisition_time"];
    $rpims_api["weather_station"]["windSpeedAgregationTime"] = $config["windspeed_agregation_time"];
    $rpims_api["weather_station"]["windSpeed"] = $rpims["wind_speed"];
    $rpims_api["weather_station"]["averageWindSpeed"] = $rpims["average_wind_speed"];
    $rpims_api["weather_station"]["dailyAveragewindSpeed"] = $rpims["daily_average_wind_speed"];
    $rpims_api["weather_station"]["windGust"] = $rpims["wind_gust"];
    $rpims_api["weather_station"]["dailyWindGust"] = $rpims["daily_wind_gust"];
    $rpims_api["weather_station"]["averageWindDirection"] = $rpims["average_wind_direction"];
    $rpims_api["weather_station"]["rainfallAcquisitionTime"] = $config["rainfall_acquisition_time"];
    $rpims_api["weather_station"]["rainfallAgregationTime"] = $config["rainfall_agregation_time"];
    $rpims_api["weather_station"]["dailyRainfall"] = $rpims["daily_rainfall"];
}

$obj = $redis-> get('gpio');
$gpio = json_decode($obj, true);

if ($config["use_door_sensor"] == true){
    foreach ($gpio as $key=> $value) {
	if ($gpio[$key]["type"] == "DoorSensor" ){
	    $door_sensors[$key] = ($gpio[$key]);
	}
    }
    foreach ($door_sensors as $key => $value){
	$rpims_api["sensors"]["door_sensors"]["$key"] = $rpims[$key];
    }
}

if ($config["use_motion_sensor"] == true){
    foreach ($gpio as $key=> $value) {
	if ($gpio[$key]["type"] == "MotionSensor" ){
	    $motion_sensors[$key] = ($gpio[$key]);
	}
    }
    foreach ($motion_sensors as $key => $value){
	$rpims_api["sensors"]["motion_sensors"]["$key"] = $rpims[$key];
    }
}

if ($config["use_DS18B20_sensor"] == true){
    $rpims_api["sensors"]["DS18B20_sensors"]["readInterval"] = $config["DS18B20_read_interval"];
    $DS18B20_sensors = $redis->smembers('DS18B20_sensors');
    foreach ($DS18B20_sensors as $key => $value){
	$rpims_api["sensors"]["DS18B20_sensors"]["array"]["$value"] = round($rpims[$value],2);
	}
    }

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
