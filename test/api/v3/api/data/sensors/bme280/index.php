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

if ($config["use_BME280_sensor"] == true){
    if ($config["BME280_i2c_address"] == "i2c"){ 
    $rpims_api["sensors"]["BME280"]["i2cAddress"] = $config["BME280_i2c_address"];
    };
    $rpims_api["sensors"]["BME280"]["interface"] = $config["BME280_interface"];
    $rpims_api["sensors"]["BME280"]["readInterval"] = $config["BME280_read_interval"];
    $rpims_api["sensors"]["BME280"]["temperature"] = $rpims["BME280_Temperature"];
    $rpims_api["sensors"]["BME280"]["humidity"] = $rpims["BME280_Humidity"];
    $rpims_api["sensors"]["BME280"]["pressure"] = $rpims["BME280_Pressure"];
}

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
