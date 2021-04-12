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

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
