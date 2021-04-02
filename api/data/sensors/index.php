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

if ($config["use_CPU_sensor"] == true){
    $rpims_api["sensors"]["CPU"]["readInterval"] = $config["CPUtemp_read_interval"];
    $rpims_api["sensors"]["CPU"]["temperature"] = $rpims["CPU_Temperature"];
}

if ($config["use_BME280_sensor"] == true){
    $rpims_api["sensors"]["BME280"]["i2cAddress"] = $config["BME280_i2c_address"];
    $rpims_api["sensors"]["BME280"]["readInterval"] = $config["BME280_read_interval"];
    $rpims_api["sensors"]["BME280"]["temperature"] = $rpims["BME280_Temperature"];
    $rpims_api["sensors"]["BME280"]["humidity"] = $rpims["BME280_Humidity"];
    $rpims_api["sensors"]["BME280"]["pressure"] = $rpims["BME280_Pressure"];
}

if ($config["use_DHT_sensor"] == true){
    $rpims_api["sensors"]["DHT"]["readInterval"] = $config["DHT_read_interval"];
    $rpims_api["sensors"]["DHT"]["gpioPin"] = $config["DHT_pin"];
    $rpims_api["sensors"]["DHT"]["dhtType"] = $config["DHT_type"];
    $rpims_api["sensors"]["DHT"]["temperature"] = $rpims["DHT_Temperature"];
    $rpims_api["sensors"]["DHT"]["humidity"] = $rpims["DHT_Humidity"];
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
	$rpims_api["sensors"]["DS18B20_sensors"]["array"]["$value"] = $rpims[$value];
	}
    }

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
