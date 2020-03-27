<!DOCTYPE html>
<html>
<head>
<title>RPiMS</title>
<meta http-equiv="refresh" content="30"/>
</head>
<body>
<?php
    $hostname = gethostname();

    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    $location = $redis->get('Location');
    $CPUtemperature = $redis->get('CPU_Temperature');

    $BME280_Temperature = $redis->get('BME280_Temperature');
    $BME280_Humidity = $redis->get('BME280_Humidity');
    $BME280_Pressure = $redis->get('BME280_Pressure');

    $DHT22_Temperature = $redis->get('DHT22_Temperature');
    $DHT22_Humidity = $redis->get('DHT22_Humidity');

    $sensorslist = $redis->keys('*');

if (empty($sensorslist)) {
 print "<p style='color:red;'>You not initialise any sensors or not run sensors.sh script. <br> Connect sensor and uncomment  proper script in /etc/cron.d/rpims file. <br> </p>";
}

if (!empty($hostname)) {
    print "<p style='color:blue;'>Hostname : " . $hostname ."</p>";
}

if (!empty($location)) {
    print "<p style='color:blue;'>Location : " . $location ."</p>";
}

if (!empty($CPUtemperature)) {
    print "<p style='color:blue;'>CPUtemperature : " . round($CPUtemperature,1) ." °C</p>";
}
print "<br>";


if (!empty($BME280_Temperature) && !empty($BME280_Humidity) && !empty($BME280_Pressure)) {
    print "<p style='color:green;'><b>BME280</b></p>";
    print "<p style='color:green;'>Temperature : " . round($BME280_Temperature,1) ." °C</p>";
    print "<p style='color:green;'>Humidity : " . round($BME280_Humidity,1) ." %</p>";
    print "<p style='color:green;'>Pressure : " . round($BME280_Pressure,1) ." hPa</p><br>";
}


if (!empty($DHT22_Temperature) && !empty($DHT22_Humidity)) {
    print "<p style='color:green;'><b>DHT22</b></p>";
    print "<p style='color:green;'>Temperature : " . round($DHT22_Temperature,1) ." °C</p>";
    print "<p style='color:green;'>Humidity : " . round($DHT22_Humidity,1) ." %</p><br>";
}

    foreach ($sensorslist as $key)
    {
    $value = $redis->get($key);
    $sensor_type = 'DS18B20-';
    if (strpos($key, $sensor_type)  !== false) {
        print "<p style='color:red;'><b>DS18B20</b></p>";
        print "<p style='color:red;'>" . $key . " Temperature: " . round($value,1) . " °C</p>";
    }
    }
print "<br>";


print "<p style='color:brown;'><b>Door/Window Sensors</b></p>";
    foreach ($sensorslist as $key)
    {
    $value = $redis->get($key);
    $sensor_type = 'door_sensor_';
    if (strpos($key, $sensor_type)  !== false) {
        print "<p style='color:brown;'>" . $key . " : " . $value . "</p>";
    }
    }
print "<br>";

?>
</body>
</html>
