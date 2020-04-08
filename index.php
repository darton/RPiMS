<!DOCTYPE html>
<html>
<head>
<title>RPiMS</title>
<meta http-equiv="refresh" content="2"/>
</head>
<body>
<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

print "<p style='color:blue;'>RPiMS location : " . $rpims["location"] . "</p>";

if ($rpims["use_CPU_sensor"] == 1) {
    print "<p style='color:blue;'>RPiMS CPU Temperature : " . round($rpims["CPU_Temperature"],2) . " °C</p><br>";
}

if ($rpims["use_BME280_sensor"] == 1) {
    print "<p style='color:green;'><b>BME280</b></p>";
    print "<p style='color:green;'>BME280 Temperature : " . round($rpims["BME280_Temperature"],2) . " °C</p>";
    print "<p style='color:green;'>BME280 Humidity : " . round($rpims["BME280_Humidity"],2) . " %</p>";
    print "<p style='color:green;'>BME280 Pressure : " . round($rpims["BME280_Pressure"],2) . " hPa</p><br>";
}

if ($rpims["use_DHT22_sensor"] == 1) {
    print "<p style='color:green;'><b>DHT22</b></p>";
    print "<p style='color:green;'>DHT22 Temperature : " . round($rpims["DHT22_Temperature"],2) . " °C</p>";
    print "<p style='color:green;'>DHT22 Humidity : " . round($rpims["DHT22_Humidity"],2) . " %</p><br>";
}

if ($rpims["use_DS18B20_sensor"] == 1) {
    print "<p style='color:green;'><b>DS18B20</b></p>";
    foreach ($rpimskeys as $key)
    {
    $sensor_type = 'DS18B20-';
    if (strpos($key, $sensor_type)  !== false) {
        print "<p style='color:green;'>" . $key . " Temperature: " . round($rpims[$key],2) . " °C</p>";
    }
    }
    print "<br>";
}

if ($rpims["use_door_sensor"] == 1) {
    print "<p style='color:brown;'><b>Door sensors</b></p>";
    print "<p style='color:brown;'>Door sensor 1 : " . $rpims["door_sensor_1"] . "</p>";
    print "<p style='color:brown;'>Door sensor 2 : " . $rpims["door_sensor_2"] . "</p><br>";
}
#if ($rpims["use_door_sensor"] == 1) {
#    print "<p style='color:red;'><b>Door sensors</b></p>";
#    foreach ($rpimskeys as $key)
#    {
#       if (preg_match("/^door_sensor_+[1-9]{1}$/", $key)) {
#           print "<p style='color:red;'>" . $key . " : " . $rpims[$key] . "</p>";
#       }
#    }
#    print "<br>";
#}

if ($rpims["use_motion_sensor"] == 1) {
    print "<p style='color:red;'><b>Motion sensors</b></p>";
    print "<p style='color:red;'>Motion_sensor_1 : " . $rpims["motion_sensor_1"] . "</p>";
    print "<p style='color:red;'>Motion_sensor_2 : " . $rpims["motion_sensor_2"] . "</p>";
    print "<p style='color:red;'>Motion_sensor_3 : " . $rpims["motion_sensor_3"] . "</p>";
    print "<p style='color:red;'>Motion_sensor_4 : " . $rpims["motion_sensor_4"] . "</p>";
    print "<p style='color:red;'>Motion_sensor_5 : " . $rpims["motion_sensor_5"] . "</p><br>";
}
#if ($rpims["use_motion_sensor"] == 1) {
#    print "<p style='color:red;'><b>Motion sensors</b></p>";
#    foreach ($rpimskeys as $key)
#    {
#       if (preg_match("/^motion_sensor_+[1-9]{1}$/", $key)) {
#           print "<p style='color:red;'>" . $key . " : " . $rpims[$key] . "</p>";
#       }
#    }
#    print "<br>";
#}

?>
</body>
</html>
