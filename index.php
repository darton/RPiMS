<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

$rpims_yaml = yaml_parse_file ("/var/www/html/rpims.yaml");
$motion_sensors = $rpims_yaml['motion_sensors'];
$door_sensors = $rpims_yaml['door_sensors'];

include 'template.html';
