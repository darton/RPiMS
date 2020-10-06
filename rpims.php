<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

$rpims_api["system"]["use_CPU_sensor"] = $rpims["use_CPU_sensor"];
$rpims_api["system"]["use_BME280_sensor"] = $rpims["use_BME280_sensor"];
$rpims_api["system"]["use_DHT_sensor"] = $rpims["use_DHT_sensor"];
$rpims_api["system"]["use_DS18B20_sensor"] = $rpims["use_DS18B20_sensor"];
$rpims_api["system"]["use_weather_station"] = $rpims["use_weather_station"];
$rpims_api["system"]["use_door_sensor"] = $rpims["use_door_sensor"];
$rpims_api["system"]["use_motion_sensor"] = $rpims["use_motion_sensor"];
$rpims_api["system"]["hostip"] = $rpims["hostip"];
$rpims_api["system"]["hostname"] = $rpims["hostname"];
$rpims_api["system"]["location"] = $rpims["location"];


if ($rpims["use_CPU_sensor"] == "True"){
    $rpims_api["sensors"]["CPU"]["Temperature"] = round($rpims["CPU_Temperature"],1);
}

if ($rpims["use_BME280_sensor"] == "True"){
    $rpims_api["sensors"]["BME280"]["Temperature"] = round($rpims["BME280_Temperature"],1);
    $rpims_api["sensors"]["BME280"]["Humidity"] = round($rpims["BME280_Humidity"],1);
    $rpims_api["sensors"]["BME280"]["Pressure"] = round($rpims["BME280_Pressure"],0);
}

if ($rpims["use_DHT_sensor"] == "True"){
    $rpims_api["sensors"]["DHT"]["Temperature"] = $rpims["DHT_Temperature"];
    $rpims_api["sensors"]["DHT"]["Humidity"] = $rpims["DHT_Humidity"];
}

if ($rpims["use_weather_station"] == "True"){
    $rpims_api["weather_station"]["wind_speed"] = $rpims["wind_speed"];
    $rpims_api["weather_station"]["average_wind_speed"] = $rpims["average_wind_speed"];
    $rpims_api["weather_station"]["daily_average_wind_speed"] = $rpims["daily_average_wind_speed"];
    $rpims_api["weather_station"]["wind_gust"] = $rpims["wind_gust"];
    $rpims_api["weather_station"]["daily_wind_gust"] = $rpims["daily_wind_gust"];
    $rpims_api["weather_station"]["average_wind_direction"] = $rpims["average_wind_direction"];
    $rpims_api["weather_station"]["daily_rainfall"] = $rpims["daily_rainfall"];
}

if ($rpims["use_motion_sensor"] == "True"){
    $motion_sensors = $redis->smembers('motion_sensors');
    foreach ($motion_sensors as $key => $value){
	$rpims_api["motion_sensors"]["$value"] = $rpims[$value];
    }
}

if ($rpims["use_door_sensor"] == "True"){
    $door_sensors = $redis->smembers('door_sensors');
    foreach ($door_sensors as $key => $value){
	$rpims_api["door_sensors"]["$value"] = $rpims[$value];
    }
}

if ($rpims["use_DS18B20_sensor"] == "True"){
    $DS18B20_sensors = $redis->smembers('DS18B20_sensors');
    foreach ($DS18B20_sensors as $key => $value){
	$rpims_api["sensors"]["DS18B20_sensors"]["$value"] = $rpims[$value];
	}
    }


Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
