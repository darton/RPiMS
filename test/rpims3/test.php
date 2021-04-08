<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

$obj = $redis-> get('sensors');
$sensors = json_decode($obj, true);

foreach ($sensors['BME280'] as $key => $value)
{
    $id = $sensors['BME280'][$key]["id"];
    $t = $id."_BME280_Temperature";
    $h = $id."_BME280_Humidity";
    $p = $id."_BME280_Pressure";

    $rpims_api["sensors"]["bme280"][$id]["temperature"] = $rpims[$t] ;
    $rpims_api["sensors"]["bme280"][$id]["humidity"] = $rpims[$h] ;
    $rpims_api["sensors"]["bme280"][$id]["pressure"] = $rpims[$p] ;
}

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
