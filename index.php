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
    $temperature = $redis->get('Temperature');
    $humidity = $redis->get('Humidity');
    $pressure = $redis->get('Pressure');
    $sensor1 = $redis->get('door_sensor_1');
    $sensor2 = $redis->get('door_sensor_2');
    $CPUtemp = $redis->get('CPUtemperature');


    print "<p style='color:magenta;'>Location: " . $location ."</p>";
    print "<p style='color:magenta;'>Hostname: " . $hostname ."</p><br>";

    print "<p style='color:red;'>Air Temperature: " . number_format($temperature,1) ." °C</p>";
    print "<p style='color:blue;'>Air Humidity...: " . number_format($humidity,1) ." %</p>";
    print "<p style='color:green;'>Air Pressure...: " . number_format($pressure,1) ." hPa</p><br>";

    print "<p style='color:brown;'>Door 1 : " . $sensor1 ."</p>";
    print "<p style='color:brown;'>Door 2 : " . $sensor2 ."</p><br>";

    print "<p style='color:red;'>CPU temperature : " . $CPUtemp ."</p>";

?>
</body>
</html>
