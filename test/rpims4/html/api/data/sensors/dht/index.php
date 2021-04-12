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

if ($config["use_DHT_sensor"] == true){
    $rpims_api["sensors"]["DHT"]["readInterval"] = $config["DHT_read_interval"];
    $rpims_api["sensors"]["DHT"]["gpioPin"] = $config["DHT_pin"];
    $rpims_api["sensors"]["DHT"]["dhtType"] = $config["DHT_type"];
    $rpims_api["sensors"]["DHT"]["temperature"] = $rpims["DHT_Temperature"];
    $rpims_api["sensors"]["DHT"]["humidity"] = $rpims["DHT_Humidity"];
}

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
