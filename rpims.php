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


$obj = $redis-> get('sensors');
$sensors = json_decode($obj, true);

//$sensors = $redis-> get('sensors');

$rpims_api["settings"]["verbose"] = $config["verbose"];
$rpims_api["settings"]["use_zabbix_sender"] = $config["use_zabbix_sender"];
$rpims_api["settings"]["use_picamera"] = $config["use_picamera"];
$rpims_api["settings"]["use_picamera_recording"] = $config["use_picamera_recording"];
$rpims_api["settings"]["use_cpu_sensor"] = $config["use_CPU_sensor"];
$rpims_api["settings"]["use_bme280_sensor"] = $config["use_BME280_sensor"];
$rpims_api["settings"]["use_dht_sensor"] = $config["use_DHT_sensor"];
$rpims_api["settings"]["use_ds18b20_sensor"] = $config["use_DS18B20_sensor"];
$rpims_api["settings"]["use_weather_station"] = $config["use_weather_station"];
$rpims_api["settings"]["use_door_sensor"] = $config["use_door_sensor"];
$rpims_api["settings"]["use_motion_sensor"] = $config["use_motion_sensor"];

$rpims_api["system"]["hostip"] = $rpims["hostip"];
$rpims_api["system"]["hostname"] = $zabbix_agent["hostname"];
$rpims_api["system"]["location"] = $zabbix_agent["location"];


if ($config["use_CPU_sensor"] == true){
    $rpims_api["sensors"]["cpu"]["temperature"] = $rpims["CPU_Temperature"];
}

if ($config["use_BME280_sensor"] == true){

    foreach ($sensors['BME280'] as $key => $value)
    {
	$id = $sensors['BME280'][$key]["id"];
	$t = $id."_BME280_Temperature";
	$h = $id."_BME280_Humidity";
	$p = $id."_BME280_Pressure";

        if ($sensors["BME280"][$id]["use"] == true)
	{
	    $rpims_api["sensors"]["bme280"][$id]["name"] = $sensors["BME280"][$id]['name'] ;
	    $rpims_api["sensors"]["bme280"][$id]["temperature"] = $rpims[$t] ;
	    $rpims_api["sensors"]["bme280"][$id]["humidity"] = $rpims[$h] ;
	    $rpims_api["sensors"]["bme280"][$id]["pressure"] = $rpims[$p] ;
	}
    }
}

if ($config["use_DS18B20_sensor"] == true){
    $DS18B20_sensors = $redis->smembers('DS18B20_sensors');
    foreach ($DS18B20_sensors as $key => $value){
        $rpims_api["sensors"]["one_wire"]["ds18b20"]["$value"]["temperature"] = $rpims[$value];
        }
    }

if ($config["use_DHT_sensor"] == true){

    $rpims_api["sensors"]["dht"]["temperature"] = $rpims["DHT_Temperature"];
    $rpims_api["sensors"]["dht"]["humidity"] = $rpims["DHT_Humidity"];
}

if ($config["use_weather_station"] == true){
    $rpims_api["weather_station"]["wind_speed"] = $rpims["wind_speed"];
    $rpims_api["weather_station"]["average_wind_speed"] = $rpims["average_wind_speed"];
    $rpims_api["weather_station"]["daily_average_wind_speed"] = $rpims["daily_average_wind_speed"];
    $rpims_api["weather_station"]["wind_gust"] = $rpims["wind_gust"];
    $rpims_api["weather_station"]["daily_wind_gust"] = $rpims["daily_wind_gust"];
    $rpims_api["weather_station"]["average_wind_direction"] = $rpims["average_wind_direction"];
    $rpims_api["weather_station"]["daily_rainfall"] = $rpims["daily_rainfall"];
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

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
