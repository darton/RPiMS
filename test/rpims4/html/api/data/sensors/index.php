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
    $rpims_api["CPU"]["readInterval"] = $config["CPUtemp_read_interval"];
    $rpims_api["CPU"]["temperature"] = $rpims["CPU_Temperature"];
}

if ($config["use_BME280_sensor"] == true){
    $rpims_api["BME280"]["i2cAddress"] = $config["BME280_i2c_address"];
    $rpims_api["BME280"]["readInterval"] = $config["BME280_read_interval"];
    $rpims_api["BME280"]["temperature"] = $rpims["BME280_Temperature"];
    $rpims_api["BME280"]["humidity"] = $rpims["BME280_Humidity"];
    $rpims_api["BME280"]["pressure"] = $rpims["BME280_Pressure"];
}

if ($config["use_DHT_sensor"] == true){
    $rpims_api["DHT"]["readInterval"] = $config["DHT_read_interval"];
    $rpims_api["DHT"]["gpioPin"] = $config["DHT_pin"];
    $rpims_api["DHT"]["dhtType"] = $config["DHT_type"];
    $rpims_api["DHT"]["temperature"] = $rpims["DHT_Temperature"];
    $rpims_api["DHT"]["humidity"] = $rpims["DHT_Humidity"];
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
	$rpims_api["door_sensors"]["$key"] = $rpims[$key];
    }
}

if ($config["use_motion_sensor"] == true){
    foreach ($gpio as $key=> $value) {
	if ($gpio[$key]["type"] == "MotionSensor" ){
	    $motion_sensors[$key] = ($gpio[$key]);
	}
    }
    foreach ($motion_sensors as $key => $value){
	$rpims_api["motion_sensors"]["$key"] = $rpims[$key];
    }
}

if ($config["use_DS18B20_sensor"] == true){
    $rpims_api["one_wire"]["readInterval"] = $config["DS18B20_read_interval"];
    $DS18B20_sensors = $redis->smembers('DS18B20_sensors');
    foreach ($DS18B20_sensors as $key => $value){
	$rpims_api["one_wire"]["ds18b20"]["$value"] = $rpims[$value];
	}
    }

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
