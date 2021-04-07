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

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
