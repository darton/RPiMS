<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$obj = $redis-> get('config');
$config = json_decode($obj, true);

$obj = $redis-> get('gpio');
$gpio = json_decode($obj, true);

$obj = $redis-> get('sensors');
$sensors = json_decode($obj, true);

if ($config["use_door_sensor"] == "True")
{
    foreach ($gpio as $key=> $value)
    {
	if ($gpio[$key]["type"] == "DoorSensor" )
	{
	    $door_sensors[$key] = ($gpio[$key]);
	}
    }
}

if ($config["use_motion_sensor"] == "True")
{
    foreach ($gpio as $key=> $value)
    {
	if ($gpio[$key]["type"] == "MotionSensor" )
	{
	    $motion_sensors[$key] = ($gpio[$key]);
	}
    }
}

if ($config["use_DS18B20_sensor"] == "True")
{
    sleep(2);
    $DS18B20_sensors = $redis->smembers('DS18B20_sensors');
}

include 'index_html.php';
