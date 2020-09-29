<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

    $rpims_api["hostIP"] = $rpims["hostip"];
    $rpims_api["hostname"] = $rpims["hostname"];
    $rpims_api["location"] = $rpims["location"];
    $rpims_api["CPU_Temperature"] = $rpims["CPU_Temperature"];

    $rpims_api["BME280_Temperature"] = $rpims["BME280_Temperature"];
    $rpims_api["BME280_Humidity"] = $rpims["BME280_Humidity"];
    $rpims_api["BME280_Pressure"] = $rpims["BME280_Pressure"];


    $rpims_api["DHT_Temperature"] = $rpims["DHT_Temperature"];
    $rpims_api["DHT_Humidity"] = $rpims["DHT_Humidity"];

    $rpims_api["wind_speed"] = $rpims["wind_speed"];
    $rpims_api["average_wind_speed"] = $rpims["average_wind_speed"];
    $rpims_api["daily_average_wind_speed"] = $rpims["daily_average_wind_speed"];
    $rpims_api["wind_gust"] = $rpims["wind_gust"];
    $rpims_api["daily_wind_gust"] = $rpims["daily_wind_gust"];
    $rpims_api["average_wind_direction"] = $rpims["average_wind_direction"];
    $rpims_api["daily_rainfall"] = $rpims["daily_rainfall"];


Header("Content-type: text/json");
echo json_encode($rpims_api);

