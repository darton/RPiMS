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

if ($config["use_weather_station"] == true){
    $rpims_api["weather_station"]["windSpeedAcquisitionTime"] = $config["windspeed_acquisition_time"];
    $rpims_api["weather_station"]["windSpeedAgregationTime"] = $config["windspeed_agregation_time"];
    $rpims_api["weather_station"]["windSpeed"] = $rpims["wind_speed"];
    $rpims_api["weather_station"]["averageWindSpeed"] = $rpims["average_wind_speed"];
    $rpims_api["weather_station"]["dailyAveragewindSpeed"] = $rpims["daily_average_wind_speed"];
    $rpims_api["weather_station"]["windGust"] = $rpims["wind_gust"];
    $rpims_api["weather_station"]["dailyWindGust"] = $rpims["daily_wind_gust"];
    $rpims_api["weather_station"]["averageWindDirection"] = $rpims["average_wind_direction"];
    $rpims_api["weather_station"]["rainfallAcquisitionTime"] = $config["rainfall_acquisition_time"];
    $rpims_api["weather_station"]["rainfallAgregationTime"] = $config["rainfall_agregation_time"];
    $rpims_api["weather_station"]["dailyRainfall"] = $rpims["daily_rainfall"];
}

Header("Content-type: application/json");
echo json_encode($rpims_api);
?>
