<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

//$rpims_yaml = yaml_parse_file ("/var/www/html/conf/rpims.yaml");
//$motion_sensors = $rpims_yaml['motion_sensors'];
//$door_sensors = $rpims_yaml['door_sensors'];

$door_sensors = $redis->smembers('door_sensors');
$motion_sensors = $redis->smembers('motion_sensors');


include 'index_html.php';
