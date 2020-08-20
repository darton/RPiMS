<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$redis->setOption(Redis::OPT_SCAN, Redis::SCAN_RETRY);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}


//$it = NULL;
//$rpims_door_sensors = $redis->scan($it, 'door_sensor_*',100);
//$it = NULL;
//$rpims_motion_sensors = $redis->scan($it, 'motion_sensor_*', 100);


$rpims_yaml = yaml_parse_file ("/var/www/html/rpims.yaml");
$motion_sensors = $rpims_yaml['motion_sensors'];
$door_sensors = $rpims_yaml['door_sensors'];

include 'template.html';
