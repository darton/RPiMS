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
    $CPUtemperature = $redis->get('CPUtemperature');

    $temperature = $redis->get('Temperature');
    $humidity = $redis->get('Humidity');
    $pressure = $redis->get('Pressure');

    $sensorslist = $redis->keys('*');

if (empty($sensorslist)) {
 print "<p style='color:red;'>You not initialise any sensors or not run sensors.sh script. <br> Connect sensor and uncomment  proper script in /etc/cron.d/rpims file. <br> </p>";
}

if (!empty($hostname)) {
    print "<p style='color:magenta;'>Hostname : " . $hostname ."</p>";
}

if (!empty($location)) {
    print "<p style='color:magenta;'>Location : " . $location ."</p>";
}

if (!empty($CPUtemperature)) {
    print "<p style='color:red;'>CPUtemperature : " . number_format($CPUtemperature,1) ." °C</p>";
}

if (!empty($temperature)) {
    print "<p style='color:red;'>Air Temperature : " . number_format($temperature,1) ." °C</p>";
}

if (!empty($humidity)) {
    print "<p style='color:blue;'>Air Humidity : " . number_format($humidity,1) ." %</p>";
}
if (!empty($pressure)) {
    print "<p style='color:green;'>Air Pressure : " . number_format($pressure,1) ." hPa</p><br>";
}
    foreach ($sensorslist as $key)
    {
    $value = $redis->get($key);
    $sensor_type = 'DS18B20-';
    if (strpos($key, $sensor_type)  !== false) {
        print "<p style='color:red;'>" . $key . " Temperature: " . $value . " °C</p>";
    }
    }

print "<br>";

    foreach ($sensorslist as $key)
    {
    $value = $redis->get($key);
    $sensor_type = 'door_sensor_';
    if (strpos($key, $sensor_type)  !== false) {
        print "<p style='color:brown;'>" . $key . " : " . $value . "</p>";
    }
    }

?>
</body>
</html>
