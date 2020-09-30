<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

$door_sensors = $redis->smembers('door_sensors');
$motion_sensors = $redis->smembers('motion_sensors');
$DS18B20_sensors = $redis->smembers('DS18B20_sensors');

include 'index_html.php';
