<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$obj = $redis-> get('config');
$rpims = json_decode($obj, true);

$obj = $redis-> get('gpio');
$gpio = json_decode($obj, true);

foreach ($gpio as $key=> $value) {
    if ($gpio[$key]["type"] == "DoorSensor" ){
	$door_sensors[$key] = ($gpio[$key]);
    }
}
foreach ($gpio as $key=> $value) {
    if ($gpio[$key]["type"] == "MotionSensor" ){
	$motion_sensors[$key] = ($gpio[$key]);
    }
}

$DS18B20_sensors = $redis->smembers('DS18B20_sensors');
include 'index_html.php';
