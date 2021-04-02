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

$obj = $redis-> get('zabbix_agent');
$zabbix_agent = json_decode($obj, true);

$rpims_api["system"]["hostip"] = $rpims["hostip"];
$rpims_api["system"]["hostname"] = $zabbix_agent["hostname"];
$rpims_api["system"]["location"] = $zabbix_agent["location"];

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
