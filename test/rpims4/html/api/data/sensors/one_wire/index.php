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
